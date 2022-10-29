#!/usr/bin/env python3
# pyFPL
# getData.py

import os
import time
import json
import pathlib as Path
from datetime import datetime, timedelta, date, timezone
from urllib.request import urlopen
from collections import OrderedDict
from operator import itemgetter, attrgetter

############################## STATIC DATA ##############################
#	In this script we deal with information	about STATIC DATA			#
#																		#
#  -------------------------------------------------------------------  #
#																		#
#	The STATIC DATA contains the following keys:						#
#		> 	"events"	--------> AKA rounds							#
#		> 	"game_settings"												#
#		> 	"phases"	--------> groups of events for monthly prizes	#
#		> 	"teams"		--------> AKA clubs								#
#		> 	"elements"	--------> AKA players/ballers					#
#		> 	"elements_stats"	> which data is provided for ballers	#
#		> 	"elements_types"	> rules for keepers, defenders etc.		#
#		> 	"total_players"		> overall total no of entries			#
#																		#
#	This is called static as it doesn't change during a live day.		#
#	Data is updated once weekly, usually after a deadline has passed	#
#	and before the first game of the rounds starts.						#
#																		#
#  -------------------------------------------------------------------  #
#																		#
#	STATIC provides several data items that are stored 					#
#	in the main global fplData at index: 								#
#		0	->	from module rounds.py									#
#		1	->	from module fixtures.py									#
#		2	->	from module clubs.py									#
#		3	->	from module elements.py									#
#		8	->	from module fixtures.py									#
#																		#
# 	fplData = 	[														#
#			>>>		{	"rounds": [] }, 	#0 		<<<					#
#			>>>		{	"fixtures": [] }, 	#1		<<<					#
#			>>>		{	"clubs": [] }, 		#2		<<<					#
#			>>>		{	"players": [] }, 	#3		<<<					#
#					{	"ownteam": [] }, 	#4							#
#					{ 	"oppteam": [] }, 	#5							#
#					{	"LgH2h": [] }, 		#6							#
#					{	"LgCls": [] }, 		#7							#
#			>>>		{ 	"CrrntFxtrs":[]}, #8		<<<					#
#					{  	"lgManIds": [] }, 	#9							#
#					{   "oppId":   } 		#10							#
#				]														#
#																		#
#  -------------------------------------------------------------------  #
#																		#
#	FPL returns  "STATIC" object as can be found in staticObj.py		#
#																		#
############################### CLUBS ###################################

import app.static.scripts.curRound as mod_cr

liveBallersArr 	=	[]
data_static 	=	[]
clubs 			= 	[]
rounds 			= 	[]
fixtures 		= 	[]
myTeam 			= 	[]
oppTeam 		= 	[]
fplDataTS 		= 	[1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654,1639269654]

"""
fplDataTS[] holds the timestamps of last update time of fplData equivalent
fplDataTS[11] is for live ballers

fplData =	[
				{ "id":"rounds"	,	"ts":0	, "data": mod_rnd.getRnds() 		},				#0 / daily
				{ "id":"fixtures",	"ts":0	, "data": mod_fxt.getFxtrs("r") 	},				#1 / daily
				{ "id":"clubs",		"ts":0	, "data": mod_clb.getClubs("r") 	},				#2 / daily
				{ "id":"players",	"ts":0	, "data": mod_plyr.getElmnts("r") 	},				#3 / daily
				{ "id":"ownteam",	"ts":0	, "data": [] },										#4
				{ "id":"oppteam",	"ts":0	, "data": [] },										#5
				{ "id":"LgCls",		"ts":0	, "data": mod_mng.getManagerLeagues(myTeamId,0)},	#6
				{ "id":"LgH2h",		"ts":0	, "data": mod_mng.getManagerLeagues(myTeamId,1)},	#7
				{ "id":"CrrntFxtrs","ts":0 	, "data": [] },										#8
				{ "id":"lgManIds",	"ts":0	, "data": mod_mng.getManIdsFromLeague(1,348264)},	#9 --> (0, 941528) = 'clssc', --> (1, 348264) = 'h2h'
				{ "id":"oppId",		"ts":0 	, "data": 30954 },									#10
				{ "id":"refresh",	"ts":0	, "data": 60 },										#11
				{ "id": "selLg",	"ts":0	, "data": { "id":348264, "nm":"348264"}},			#12
				{ "id": "curRound",	"ts":0	, "data": 6 }	 									#13
			]

"""
fplDataIds = 	( 
					"rounds", 		#0
					"fixtures",		#1
					"clubs",		#2
					"players",		#3
					"ownteam",		#4
					"oppteam",		#5
					"LgCls",		#6
					"LgH2h",		#7
					"CrrntFxtrs",	#8
					"lgManIds",		#9 
					"oppId",		#10
					"liveBllr",		#11
					"selLg",		#12
					"curRound" 		#13
			)

# currentRnd = mod_cr.getCurrentRnd() "currentRnd",currentRnd,
currentDdln = mod_cr.getCurrentDeadline()

def infoRt(dataIdx):
	useRemote 			= 	False
	crit 				= 	""
	timeStamp			=	fplDataTS[dataIdx]
	last_update			=	datetime.fromtimestamp( timeStamp ,tz=timezone.utc)
	now_date			=	datetime.fromtimestamp( float(time.time()) ,tz=timezone.utc)
	today				=	datetime.today()
	delta				=	now_date - last_update
	days				=	delta.days
	minutes, seconds	=	divmod( delta.seconds, 60)
	hours, minutes		=	divmod( minutes, 60)

	if( dataIdx in [ 8 ] ):
		# 'fixture' data needs to less than 10 minutes old
		useRemote = (delta.seconds>600)
		crit = "10mins"
	elif( dataIdx in [ 3, 11 ] ):
		# 'live ballers'(11) data needs to less than 90 seconds old
		useRemote = (delta.seconds>90)
		crit = "90secs"
	elif( dataIdx in [ 0, 1, 2, 6, 7, 9 ] ):
		# data needs to less than 1 day old
		# 0 = rounds, 1 = fixtures, 2 = clubs, 3 = players
		useRemote = ( days > 1 )
		crit = "1 days"
	elif( dataIdx in [ 4, 5 ] ):
		# once after current round deadline
		# datetime.fromtimestamp( float(time.time()) ,tz=timezone.utc)
		delta_ddln =  datetime.utcnow() -  datetime.fromtimestamp( currentDdln  )
		ddlnPast = ( delta_ddln.seconds > 0 )
		print( "deadline:\t", currentDdln , 	"\tneeds update after ddln:\t", ddlnPast  )
		useRemote = ddlnPast
		crit = "after deadline"

	elif( dataIdx in [ 10, 13 ] ):
		# always update
		useRemote = True
		crit = "always"
	else:
		# never update. 12
		useRemote = False
		crit = "never"

	print( "useRemote is\t", useRemote, "\tfor\t", dataIdx, "\t", fplDataIds[dataIdx] , "\ton:\t", 	time.time() , "\tcrit:\t", 	crit )
	return useRemote


def getStatic(w):
	if( w =="r" ):
		data_static = getRemoteStatic()
	else:
		data_static = getLocalStatic()

	return data_static

def getLocalStatic():
	# print("getLocalStatic")
	if os.path.exists( "./app/static/data/static/static.json" ):
		foStatic = open( "./app/static/data/static/static.json" )
		data_static = json.load(foStatic)
		foStatic.close
	else:
		# print("static_file does NOT exists. using remote")
		data_static = getRemoteStatic()

	return data_static

def getRemoteStatic():
	url = "https://fantasy.premierleague.com/api/bootstrap-static/"
	response = urlopen(url)
	data_static = json.loads(response.read())
	baseTS = float(time.time())
	# base static
	stf = open( "./app/static/data/static/static.json", "w+")
	stf.write( json.dumps( data_static, indent=4) )
	stf.close

	# 0 = rounds
	rnf = open( "./app/static/data/static/rounds.json", "w+")
	rnf.write( json.dumps( data_static["events"], indent=4) )
	rnf.close
	fplDataTS[0] = baseTS

	# 2 = clubs
	rclubs = data_static["teams"]
	for c in rclubs:
		c["goalies"] =  []
		c["defenders"] =  []
		c["midfielders"] =  []
		c["forwards"] =  []
		c["df"] = [2,2]
		c["ppgc"] = 0

	clf = open( "./app/static/data/static/clubs.json", "w+")
	clf.write( json.dumps( rclubs, indent=4) )
	clf.close
	fplDataTS[2] = baseTS

	# 3 = players / elements
	elf = open( "./app/static/data/static/elements.json", "w+")
	elf.write( json.dumps( data_static["elements"], indent=4) )
	elf.close
	fplDataTS[3] = baseTS

	return data_static
