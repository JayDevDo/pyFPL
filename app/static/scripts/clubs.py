#!/usr/bin/env python3
# pyFPL
# clubs.py

import os
import time
import sys
import json
from urllib.request import urlopen

############################### CLUBS ###################################
#	In this script we deal with information	about CLUBS					#
#	(aka teams).														#
#  -------------------------------------------------------------------  #
#	There are 20 clubs 													#
#	Clubs are stored in the main global at index 2:						#
#																		#
# 		fplData = 	[													#
#						{	"rounds": [] }, #0 							#
#						{	"fixtures": [] }, #1						#
#	>>>					{	"clubs": [] }, #2					<<<		#
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
#	FPL returns the following "TEAM" object (we call it CLUB):			#
#																		#
#	{																	#
#		"code": 3,														#
#		"draw": 0,														#
#		"form": null,													#
#		"id": 1,														#
#		"loss": 0,														#
#		"name": "Arsenal",												#
#		"played": 0,													#
#		"points": 0,													#
#		"position": 0,													#
#		"short_name": "ARS",											#
#		"strength": 4,													#
#		"team_division": null,											#
#		"unavailable": false,											#
#		"win": 0,														#
#		"strength_overall_home": 1190,									#
#		"strength_overall_away": 1250,									#
#		"strength_attack_home": 1110,									#
#		"strength_attack_away": 1140,									#
#		"strength_defence_home": 1110,									#
#		"strength_defence_away": 1170,									#
#		"pulse_id": 1													#
#	}																	#
#																		#
#	The object has room for, but does not provide data for:				#
#		> draw															#
#		> form															#
#		> loss															#
#		> played														#
#		> points														#
#		> position														#
#		> win															#
#																		#
#	DF = difficulty factor												#
#	Additional data will be stored in CLUB								#
#		> ownDF: []	-> storing the DF for the opponents for each round	#
#		> oppDF: []	-> storing the DF of the opponents for each round	#
#		> nickname: in above club "The Gunners"							#
#		> ballerIds: [] -> 	storing id's of elements (ballers)			#
#							in this club.								#
#																		#
############################### CLUBS ###################################

import app.static.scripts.getData as mod_data
import app.static.scripts.elements as mod_players

clubs_file 	= "./app/static/data/static/clubs.json"
global clubs
clubs = []

def getClubs(w):
	if( w =="r" or mod_data.infoRt(2) ):
		data_clubs = getRemoteClubs()
	else:
		data_clubs = getLocalClubs()

	global clubs
	clubs = data_clubs	
	return data_clubs

def getLocalClubs():
	global clubs
	if( len(clubs)>10 ):
		data_clubs = clubs
	elif( os.path.exists( clubs_file )):
		foclubs = open( clubs_file )
		data_clubs = json.load(foclubs)
		foclubs.close
	else:
		# print("clubs_file does NOT exists. using remote")
		data_clubs = getRemoteClubs()

	return data_clubs


def getRemoteClubs():
	response = mod_data.getStatic("r")
	rclubs = response["teams"]
	for c in rclubs:
		c["goalies"] =  [] 
		c["defenders"] =  [] 
		c["midfielders"] =  [] 
		c["forwards"] =  [] 
		c["df"] = [2,2]
		c["ppgc"] = 0

	clf = open( clubs_file, "w+")
	clf.write( json.dumps( rclubs, indent=4) )
	clf.close
	mod_data.fplDataTS[2] = float(time.time())
	return rclubs


def getClubData(clubId):
	global clubs
	if( clubs ):
		# print( "getClubData", len( clubs ) )
		clubs_static = clubs
	elif ( os.path.exists( clubs_file ) ):
		foclb = open( clubs_file )
		clubs_static = json.load( foclb )
		foclb.close
	else:
		clubs_static = getClubs("r")

	if( len(clubs_static) > 0 ):
		for c in clubs_static:
			if( c["id"] == clubId ):
				# print("elmnts_static", str(elId),"b", b)
				return c


def getClubName(clubId):
	return getClubData(clubId)["name"]

def getClubShNm(clubId):
	return getClubData(clubId)["short_name"]

def addLvBllrInfo(bllr):
	global clubs
	# print("adding baller", bllr["id"])
	baller = mod_players.getBaller( bllr["id"])
	# print("team", bllr["team"],"clubnm", mod_players.getBallerClub( bllr["id"] ) ,"elmt type", baller["element_type"] )
	# print("global clubs", len(clubs) )
	# print("global clubs gkp", clubs[ (clubId-1) ]["goalies"]  		)
	# print("global clubs def", clubs[ (clubId-1) ]["defenders"] 		)
	# print("global clubs mid", clubs[ (clubId-1) ]["midfielders"]	)
	# print("global clubs fwd", clubs[ (clubId-1) ]["forwards"]		)
	"""
		check if baller exists in club[position], then remove->insert
		else insert
	"""

