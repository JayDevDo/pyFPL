#!/usr/bin/env python3
# pyFPL
# teams.py

import os
import sys
import time
import json
from flask import Flask, send_file, render_template, url_for, request, redirect
import urllib.request 
import urllib.error


"""
	####################################### TEAMS #######################################
	#																					#
	#	In this script we deal with information	about TEAMS								#
	#	(aka FPL contenders' PICKS for the active or finished rounds ).					#
	#	------------------------------------------------------------------				#
	#	Each manager picks 15 players (elements). Their 'position' within the			#
	#	selection defines if a player is benched, or starts. 							#
	#	4 are on the bench ( 'position' = 12, 13, 14, 15 ). 							#
	# 	11 are starters ( 'position' < 12 ).											#
	#	This module returns a html table that can be used for any manager entry.		#
	#																					#
	# 	The url = "fantasy.premierleague.com/api/entry/{manId}/event/{round}/picks/" 	#
	# 	FPL provides an object which is stored in fplData[4 and 5]						#
	#																					#
	# 		fplData = 	[																#
	#						{	"rounds": [] }, #0										#
	#						{	"fixtures": [] }, #1									#
	#						{	"clubs": [] }, #2										#
	#						{	"players": [] }, #3										#
	#		>>>>			{	"ownteam": [] }, #4		<<<<							#
	#		>>>>			{ 	"oppteam": [] }, #5		<<<<							#
	#						{	"LgH2h": [] }, #6										#
	#						{	"LgCls": [] }, #7										#
	#						{ 	"CrrntFxtrs": [] }, #8									#
	#						{  	"lgManIds": [] }, #9									#
	#						{   "oppId":   } #10										#
	#					]																#
	#																					#
	#	FPL returns the following "ENTRY" object (we call it team):						#
	# 	KEYS (default): 'active_chip', 'automatic_subs', 'entry_history', 'picks'.		#
	# 	KEYS (added): 'manager'.														#
	#	A complete team object is teamObj.py  											#
	#																					#
	# 	{																				#
	#     "active_chip": null,															#
	#     "automatic_subs": [  ---------> only available after final matchday update 	#
	#         {																			#
	#             "entry": 993831,														#
	#             "element_in": 225,													#
	#             "element_out": 78,													#
	#             "event": 15															#
	#         }																			#
	#     ],																			#
	#     "entry_history": {															#
	#         "event": 15,																#
	#         "points": 57, 	--------> without subs when matchday not closed 		#
	#         "total_points": 904, -----> before current round. 						#
	#         "rank": 911254,															#
	#         "rank_sort": 917549,														#
	#         "overall_rank": 624557,													#
	#         "bank": 0,																#
	#         "value": 1017, ---------------> actual amount is 101,7					#
	#         "event_transfers": 0,														#
	#         "event_transfers_cost": 0,												#
	#         "points_on_bench": 9 	----> does not calculate net-win for subs.			#
	#     },																			#
	#     "picks": [																	#
	#			{																		#
	#             "element": 69,														#
	#             "position": 1,														#
	#             "multiplier": 1,														#
	#             "is_captain": false,													#
	#             "is_vice_captain": false												#
	#			},#			{.....},{.....},{.....},{.....},{.....},					#
	#			{.....},{.....},{.....},{.....},										#
	#			{																		#
	#             "element": 263,														#
	#             "position": 11,														#
	#             "multiplier": 1,														#
	#             "is_captain": false,													#
	#             "is_vice_captain": false												#
	#			},																		#
	#			{																		#
	#             "element": 146,														#
	#             "position": 12,														#
	#             "multiplier": 0,														#
	#             "is_captain": false,													#
	#             "is_vice_captain": false												#
	#			},{.....},{.....}														#
	#			{																		#
	#             "element": 413,														#
	#             "position": 15,														#
	#             "multiplier": 0,														#
	#			  "is_captain": false,													#
	#          	  "is_vice_captain": false												#
	#       	}																		#
	#   	]																			#
	# 	}																				#
	#																					#
	#	We add the "MANAGER" object to the "TEAM" object as 'manager'					#
	#	see manager.py																	#
	#																					#
	####################################### TEAMS #######################################
"""

import app.static.scripts.managers 	as mod_man
import app.static.scripts.elements 	as mod_players
import app.static.scripts.rounds	as mod_rnd
import app.static.scripts.curRound  as mod_cr
import app.static.scripts.getData 	as mod_data

team_file_base_name = "./app/static/data/live/active/tm/tm_"
posArr = ["POS","GKP","DEF","MID","FWD"]

def getTeam(w, t, teamId):
	# w=where, accepts [l/r]="Local/Remote"
	# t=team, accepts [4/5]="fplData[4/5]"
	# print( "getTeam. For ", teamId, "own4/opp5:", t, "called with:", w)
	if( w =="r" ):
		data_team = getRemoteTeam(teamId, t)
	else:
		data_team = getLocalTeam(teamId, t)

	tmPicks = {}
	tmPicks["manager"] = mod_man.getManagerData(teamId)
	tmPicks["roundDash"] = data_team["entry_history"] 
	tmPicks["strtrs"] = []
	tmPicks["bnch"]= []
	tmPicks["gkp"] = []
	tmPicks["def"] = []
	tmPicks["mid"] = []
	tmPicks["fwd"] = []
	unsortedBench = []

	liveBallerArr = mod_players.getRemoteLiveBallers()

	# print("getting team of", teamId , tmPicks["manager"]["name"])
	for p in data_team["picks"]:
		p["web_name"] = mod_players.getBallerName( p["element"] )
		p["ballerData"] = mod_players.getBaller( p["element"] )
		p["liveBallerData"] = mod_players.getLiveBaller( p["element"] )
		p["posNm"] = posArr[ p["ballerData"]["element_type"] ]
		p["liveBallerData"]["potentialSub"] = mod_players.potentialSub( p["element"] )
		if( len(data_team["automatic_subs"])>0 ):
			for autosub in data_team["automatic_subs"]:
				p["element_out"] = autosub["element_out"]
				p["element_in"] = autosub["element_in"]
				if( autosub["element_in"]==p["element"] ):
					p["autosubbed"] = True
				elif( autosub["element_out"]==p["element"] ):
					p["autosubbed"] = True
				else:
					p["autosubbed"] = False

		if( p["position"]>11 ):
			tmPicks["bnch"].append( p )
		else:
			tmPicks["strtrs"].append( p )
			if(p["ballerData"]["element_type"] == 1):
				# print("add goalkeeper", p["web_name"])
				tmPicks["gkp"].append( p )
			elif( p["ballerData"]["element_type"] == 2):
				# print("add defender", p["web_name"])
				tmPicks["def"].append( p )
			elif( p["ballerData"]["element_type"] == 3):
				# print("add midfielder", p["web_name"])
				tmPicks["mid"].append( p )
			elif( p["ballerData"]["element_type"] == 4):
				# print("add forward", p["web_name"])
				tmPicks["fwd"].append( p )

	# print("data_histeam['picks'] bnch", len(tmPicks["bnch"]))
	unsortedBench = tmPicks['bnch']
	sortedBench = sorted( unsortedBench, key=lambda unsortedBench: unsortedBench["position"] )
	tmPicks['bnch'].clear()
	tmPicks['bnch'] = sortedBench
	tmPicks["liveTeam"] = data_team["picks"]
	# print("getRemoteMyTeam returns", json.dumps( data_histeam, indent=4) )
	return tmPicks


def getLocalTeam(teamId, t):
	if(mod_data.infoRt(t)):
		data_team = getRemoteTeam(teamId, t)
	elif (os.path.exists( team_file_base_name + str(teamId) + ".json" )):
		foteam = open( team_file_base_name + str(teamId) + ".json" )
		data_team = json.load(foteam)
		foteam.close
	else:
		# print("team_file_base_name + teamId does NOT exists. using remote")
		data_team = getRemoteTeam(teamId, t)

	return data_team


def getRemoteTeam(teamId, t):
	""" 
		Gets and returns the team(teamId) picks of the current GW . t is either 4 (OwnTeam) or 5 (OppTeam) (not used atm) 
	"""
	currentGW = mod_cr.getCurrentRnd()
	print("getRemoteTeam -tmId:\t",teamId,"\tcurrentGW:\t", currentGW )
	data_team = ""

	if( currentGW > 0 ):
		# After the start of Game 1 gameweek 1, picks should be available.
		url = "https://fantasy.premierleague.com/api/entry/" + str(teamId)+ "/event/" + str( currentGW ) + "/picks/"
		print("post-opening, using team/gw/pick. GW:\t", currentGW , "\nURL:\t", url )
		response = urllib.request.urlopen(url)
		data_team = json.loads(response.read())
		print("getRemoteTeam data_team:\t", data_team )	

	else:
		# Before the first game has started, no team picks available, so using own Team.
		print("pre-opening, using local file")
		foteam = open( "app/static/data/live/active/PreSeason_704118.json" )
		data_team = json.load(foteam)
		foteam.close
		print("getRemoteTeam data_team:\t", data_team )	

	stf = open( team_file_base_name + str(teamId) + ".json", "w+")
	stf.write( json.dumps( data_team, indent=4 ) )
	stf.close
	mod_data.fplDataTS[t] = float( time.time() )
	return data_team

