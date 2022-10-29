#!/usr/bin/env python3
# pyFPL
# fixtures.py

import os
import time
import sys
import json
from urllib.request import urlopen
from datetime import datetime, timedelta, date

############################# FIXTURES ##################################
#	In this script we deal with information	about FIXTURES				#
#	(aka matches / games / ).											#
#  -------------------------------------------------------------------  #
#	There are 380 fixtures (fxtr/fxtrs) in 38 rounds (rnd/rnds).		#
#	Round 39 will be used to store postponed (pp) fixtures.				#
#	Fixtures can move between rounds (pp/replan)						#
#	Each fixture involves 2 clubs (also called teams)					#
#	The FPL returns pp-fxtr with 'event': null ( rnd = null )			#
#	Fixtures are stored in the main global at index 1:					#
#																		#
# 		fplData = 	[													#
#						{	"rounds": [] }, #0 							#
#	>>>					{	"fixtures": [] }, #1				<<<		#
#						{	"clubs": [] }, #2							#
#						{	"players": [] }, #3							#
#						{	"ownteam": [] }, #4							#
#						{ 	"oppteam": [] }, #5							#
#						{	"LgH2h": [] }, #6							#
#						{	"LgCls": [] }, #7							#
#						{ 	"CrrntFxtrs": [] }, #8						#
#						{  	"lgManIds": [] }, #9						#
#						{   "oppId":   } #10							#
#					]													#
#																		#
#	FPL returns the following fixture:									#
#	{																	#
#		"code": 2210502, 												#
#		"event": null, --->	is postponed ! generates error on rnd.id	#
#		"finished": false, 												#
#		"finished_provisional": false, 									#
#		"id": 232, 														#
#		"kickoff_time": null, 											#
#		"minutes": 0, 													#
#		"provisional_start_time": false, 								#
#		"started": null, 												#
#		"team_a": 6, 	-------------------> club.id					#
#		"team_a_score": null, 											#
#		"team_h": 4, 	-------------------> club.id					#
#		"team_h_score": null, 											#
#		"stats": [], 													#
#		"team_h_difficulty": 4, (means team_a has away DF 4)			#
#		"team_a_difficulty": 3, (means team_h has home DF 3)			#
#		"pulse_id": 66573												#
# 	}																	#
#																		#
#																		#
#	To the object we add: 												#
#		> status: 'Live', 'Finished', 'Later', 'Future'					#
#																		#
#																		#
#																		#
#																		#
#																		#
############################# FIXTURES ##################################

import app.static.scripts.rounds 	as mod_rnd
import app.static.scripts.clubs 	as mod_clb
import app.static.scripts.getData 	as mod_data
import app.static.scripts.curRound 	as mod_cr
import app.static.scripts.elements 	as mod_players

fxtr_cr = mod_cr.getCurrentRnd()

fxtrs_file 	= "./app/static/data/static/fixtures.json"

global fixtures
fixtures = []

lv_fxtrs_file 	= "./app/static/data/live/active/fixtures_"+str(fxtr_cr)+"_live.json"

global live_fixtures
live_fixtures = []

ppFixture=  {
				"code": 0,
				"event": 39,
				"finished": True,
				"finished_provisional": False,
				"id": 0,
				"kickoff_time": "2023-06-30T15:00:00Z",
				"minutes": 0,
				"provisional_start_time": False,
				"started": False,
				"team_a": 0,
				"team_a_score": 0,
				"team_h": 0,
				"team_h_score": 0,
				"stats": [],
				"team_h_difficulty": 0,
				"team_a_difficulty": 0
			}

def getFxtrs(w):
	global fixtures
	if( (w =="r") or mod_data.infoRt(1) ):
		data_fxtrs = getRemoteFxtrs()
	else:
		data_fxtrs = getLocalFxtrs()

	fixtures = data_fxtrs
	return data_fxtrs


def getLocalFxtrs():
	global fixtures
	if( len(fixtures)>9 ):
		# print("len global fixtures ", len(fixtures) )
		data_fxtrs = fixtures
	elif( os.path.exists( fxtrs_file )):
		foFxtrs = open( fxtrs_file )
		data_fxtrs = json.load(foFxtrs)
		foFxtrs.close
	else:
		# print("fxtrs_file does NOT exists. using remote")
		data_fxtrs = getRemoteFxtrs()

	return data_fxtrs


def getRemoteFxtrs():
	print("getRemoteFxtrs")
	url = "https://fantasy.premierleague.com/api/fixtures/?events>0"
	response = urlopen(url)
	data_fxtrs = json.loads(response.read())

	for f in data_fxtrs:
		f["team_h_nm"] = mod_clb.getClubShNm(f["team_h"])
		f["team_a_nm"] = mod_clb.getClubShNm(f["team_a"])
		if(f['event'] is None):
			f['event']=39

	fxf = open( fxtrs_file, "w+")
	fxf.write( json.dumps( data_fxtrs, indent=4) )
	fxf.close
	mod_data.fplDataTS[1] = float(time.time())
	return data_fxtrs


def getFixture(fxtrId):
	if( fxtrId == 0 ):
		return ppFixture
	else:
		if( len(fixtures) == 0 ):
			tmpFxtrs = getFxtrs("l")
		else:
			tmpFxtrs = fixtures

	for fxtr in tmpFxtrs:
		if( fxtr["id"] == fxtrId ):
			return fxtr


def getLiveFxtrData():
	global live_fixtures, fxtr_cr
	if( mod_data.infoRt(8) or (True) ):
		if( type(fxtr_cr) == type(None) ):
			print("getLiveFxtrData NO current Round" )
			fxtr_cr = 0
		else:
			print("getLiveFxtrData. Using remote live_fixtures of gw:\t", fxtr_cr )

		url = "https://fantasy.premierleague.com/api/fixtures/?event=" + str(fxtr_cr)
		response = urlopen( url)
		gld = json.loads(response.read())
		mod_data.fplDataTS[8] = float(time.time())


	else:	
		if( len(live_fixtures) > 0 ):
			# print("len global live fixtures ", len(live_fixtures) )
			gld = live_fixtures
		elif( os.path.exists( lv_fxtrs_file )):
			foLvFxtrs = open( lv_fxtrs_file )
			gld = json.load(foLvFxtrs)
			foLvFxtrs.close
		else:
			# print("NO local live fixtures. using remote")
			url = "https://fantasy.premierleague.com/api/fixtures/?event=" + str(fxtr_cr)
			response = urlopen( url )
			gld = json.loads(response.read())
			mod_data.fplDataTS[8] = float(time.time())


	# print("gld size", len(gld) )
	retDict = []
	for e in gld:
		f_date = datetime.utcnow().replace(tzinfo=None)
		l_date = datetime.strptime(e["kickoff_time"][:-1], '%Y-%m-%dT%H:%M:%S') 
		l_date = l_date +  timedelta(hours=1)
		delta =  f_date - l_date
		days = delta.days
		minutes, seconds = divmod( delta.seconds, 60)
		hours, minutes = divmod( minutes, 60)
		today = datetime.today()
		later = today + timedelta(hours=14)
		e["team_h_nm"] = mod_clb.getClubName(e["team_h"])
		e["team_a_nm"] = mod_clb.getClubName(e["team_a"])
		# print("elif( days==0 and (l_date>f_date) )=later", l_date - f_date )
		if( not e["finished"] and e["started"] ):
			e["status"] = "live"
			e["event_bonus"] = dictFxtrBonus(e)
		elif(e["finished"]):
			e["status"] = "finished"
			e["event_bonus"] = dictFxtrBonus(e)
		elif( l_date < later ):
			e["status"] = "later"
		elif( l_date > f_date ):
			e["status"] = "future"

		retDict.append(e)
		# print("added live fixture ", e['id'],"date", l_date, "with status", e['status'])

	lfxf = open( lv_fxtrs_file, "w+")
	lfxf.write( json.dumps( retDict, indent=4) )
	lfxf.close
	live_fixtures = retDict
	return retDict

def dictFxtrBonus(fxtr):
	bnsArr = []
	retArr = []
	bnsArr +=  fxtr["stats"][9]['a']
	bnsArr +=  fxtr["stats"][9]['h'] 
	bnsSrtd = sorted(bnsArr, key = lambda bonus : bonus["value"], reverse = True )
	i=0
	lastVal = 0

	for b in bnsSrtd:
		b["web_name"] = mod_players.getBallerName( b["element"] )
		if( b["value"] == lastVal ):
			b["bns_rank"] = lastRank
			b["bns_pts"] = (4-lastRank)			
		else:
			lastVal = b["value"]
			lastRank = (1+i)
			b["bns_rank"] = lastRank
			if( (4 - lastRank ) > 0 ):
				b["bns_pts"] = (4-lastRank)
			else:
				b["bns_pts"] = 0
	
		if(i<6):
			retArr.append(b)
			i += 1

	# for bb in bnsSrtd: print("bb in bnsSrtd nm", mod_players.getBallerName(bb["element"]) ,json.dumps(bb) )
	return retArr
