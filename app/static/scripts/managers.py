#!/usr/bin/env python3
# pyFPL
# managers.py

import os
import sys
import json
from urllib.request import urlopen

################################ MANAGERS #######################################
#	In this script we deal with information	about MANAGERS						#
#	(aka FPL contenders ).														#
#  ------------------------------------------------------------------- 		 	#
#	There are nearly 9 mln manager entries, and still growing.					#
#	Only the ids of managers that are in a selected league (fplData[6/7])		#
#	(h2h,classic,global) will be stored in the main global at index 9:			#
#	The info of a manager will be stored, as is, 								#
# 	under fplData[4/own team].manager and fplData[5/opponent].manager 			#
#																				#
# 		fplData = 	[															#
#						{	"rounds": [] }, #0 									#
#						{	"fixtures": [] }, #1								#
#						{	"clubs": [] }, #2									#
#						{	"players": [] }, #3									#
#	>>>					{	"ownteam": [] }, #4			<<<						#
#	>>>					{ 	"oppteam": [] }, #5			<<<						#
#						{	"LgH2h": [] }, #6									#
#						{	"LgCls": [] }, #7									#
#						{ 	"CurrentFxtrs": [] }, #8							#
#	>>>					{  	"lgManIds": [] }, #9			<<<					#
#						{   "oppId":   } #10									#
#					]															#
#																				#
# 	From 'fantasy.premierleague.com/api/entry/{manId}/' 						#
#	FPL returns the following "ENTRY" object (we call it MANAGER):				#
#	A complete manager object is managerObj.py									#
#																				#
#	{																			#
# 		"id":993831,															#
# 		"joined_time":"2021-07-12T11:31:29.607544Z",							#
# 		"started_event":1,														#
# 		"favourite_team":11,													#
# 		"player_first_name":"Jay",												#
# 		"player_last_name":"Vando",												#
# 		"player_region_id":152,													#
# 		"player_region_name":"Netherlands",										#
# 		"player_region_iso_code_short":"NL",									#
# 		"player_region_iso_code_long":"NLD",									#
# 		"summary_overall_points":981,											#
# 		"summary_overall_rank":552624,											#
# 		"summary_event_points":16,												#
# 		"summary_event_rank":1118186,											#
# 		"current_event":17,														#
#		"name":"Bielsabub's Demons",											#
#		"name_change_blocked":false,											#
#		"kit": "",																#
#		"last_deadline_bank":16,												#
#		"last_deadline_value":1018,												#
#		"last_deadline_total_transfers":21										#
# 		"leagues":{																#
#			"classic":[															#
#					{"id",														#
#					"name":"Liverpool",											#
#					"short_name":"team-11",										#
#					"created":"2021-06-22T10:37:33.072878Z",					#
#					"closed":false,												#
#					"rank":null,												#
#					"max_entries":null,											#
#					"league_type":"s",											#
#					"scoring":"c",												#
#					"admin_entry":null,											#
#					"start_event":1,											#
#					"entry_can_leave":false,									#
#					"entry_can_admin":false,									#
#					"entry_can_invite":false,									#
#					"has_cup":true,												#
#					"cup_league":null,											#
#					"cup_qualified":null,										#
#					"entry_rank":195322,										#
#					"entry_last_rank":195322									#
#			},																	#
#			{...........}														#
#			],																	#
#			"h2h":[																#
#					{"id":436866,												#
#					"name":"League 436866",										#
#					"short_name":null,											#
#					"created":"2021-07-31T14:36:59.598134Z",					#
#					"closed":true,												#
#					"rank":null,												#
#					"max_entries":null,											#
#					"league_type":"c",											#
#					"scoring":"h",												#
#					"admin_entry":null,											#
#					"start_event":1,											#
#					"entry_can_leave":false,									#
#					"entry_can_admin":false,									#
#					"entry_can_invite":false,									#
#					"has_cup":false,											#
#					"cup_league":null,											#
#					"cup_qualified":null,										#
#					"entry_rank":3,												#
#					"entry_last_rank":3											#
#			},																	#
#			{ ......... }														#
#			],																	#
#			"cup":{																#
#				"matches":[],													#
#				"status":{														#
#					"qualification_event":null,									#
#					"qualification_numbers":null,								#
#					"qualification_rank":null,									#
#					"qualification_state":null									#
#					},															#
#			"cup_league":315													#
#			},																	#
#			"cup_matches":[{}],													#
#		},																		#
#	}																			#
#																				#
################################## MANAGERS #####################################

import app.static.scripts.leagues as mod_lgs

url_page = 1
lgTypeArr = ("classic","h2h","cup_matches")
lgStanFile = "./app/static/data/live/active/lg/lg_"


def getManagerData(manId):
	man = urlopen("https://fantasy.premierleague.com/api/entry/" + str(manId) + "/")
	# print("getManagerData url:\t", "https://fantasy.premierleague.com/api/entry/" + str(manId) + "/"  )

	managerData = json.loads(man.read())
	# time.sleep(1)
	# print("getManagerData returns", str(managerData["name"]) )
	return managerData

def getManagerLeagues( manId, lgType ):
	man = getManagerData(manId)
	if( lgType > 2 ):
		# print ("getManagerLeagues(", str(manId), ", lgType>2). Only 0/1/2  are accepted. Changing inout lgType to 0")
		lgType = 0 

	man_lgs = man['leagues'];
	# print("getManagerLeagues:\t", man_lgs[ lgTypeArr[lgType] ] )
	return man_lgs[ lgTypeArr[lgType] ]

def getManIdsFromLeague(lgType, lgId):
	"""
		0=classic, 1=head2head, 3=cup
	"""
	lgCount = mod_lgs.guessLeagueCount(lgType, lgId)

	maxRes = 50
	if( lgType == 0 ):
		url= "https://fantasy.premierleague.com/api/leagues-classic/" + str( lgId ) + "/standings/?page_new_entries=1&page_standings=1&phase=1"
	elif( lgType == 1 ):
		url= "https://fantasy.premierleague.com/api/leagues-h2h/" + str( lgId ) + "/standings/?page_new_entries=1&page_standings=1&phase=1"
		"""	
		elif( lgType == 2 ):
			# liverpool cup league = 2400372
			cupId = 2400372 
			url="https://fantasy.premierleague.com/api/leagues-h2h-matches/league/" + str(cupId) + "/?page=1&entry=" + str(myTeamId)
		"""
	else:
		pass
		# print("lgType not recognised")

	print("getting type=", lgType ,"lg", lgId, url)
	response = urlopen( url )
	lg = json.loads( response.read() )
	lg["league"]['lgCount'] = lgCount
	lgIds = lg["standings"]["results"]
	lfxf = open( lgStanFile+str(lgId)+".json", "w+")
	lfxf.write( json.dumps( lg, indent=4) )
	lfxf.close
	lgIdArr = []
	# print("getManIdsFromLeague() returning " , json.dumps( lgIds, indent=4 ) )
	return lgIds 

def getLgNm(lgId):
	lgStanFile = "./app/static/data/live/active/lg/lg_"+str(lgId)+".json"
	if os.path.exists( lgStanFile ):
		folg = open(lgStanFile)
		data_league = json.load(folg)
		folg.close
	else:
		pass
		# print("team_file_base_name + teamId does NOT exists. using remote")

	tmNm = data_league['league']['name']
	return tmNm
