#!/usr/bin/env python3
# pyFPL
# leagues.py

import os
import time
import json
from urllib.request import urlopen

############################## LEAGUES ##################################
#	In this script we deal with information	about LEAGUES				#
#  -------------------------------------------------------------------  #
#	We have no clue how many leagues there are							#
#	Every manager is entered in 4 default General leagues:				#
#	> Overall			( leagueId = 314 )								#
#	> Country			( leagueId = 172 = NL )							#
#	> Favourite club 	( leagueId = clubId )							#
#	> entry round 		( leagueId = 276 = Week 1 )						#
#																		#
#	Every manager can join a number of leagues, be it classic or h2h.	#
#	Each league can have a cup competition. We are ignoring them ftm 	#
#																		#
#	LEAGUES are retrieved from the manager url:							#
# 	https://fantasy.premierleague.com/api/entry/{manId}/leagues/  		#
#	then "leagues". It returns the following object:					#
#	{																	#
#		"classic":[],													#
#		"h2h": [],														#
#		"cup": [],														#
#		"cup_matches": []												#
#	}																	#
#																		#
#	Within the 'classic' array we get the league data as follows:		#
#																		#
# 	{																	#
#>>>>>	"id": 11,		<<<<											#
# 		"name": "Liverpool",											#
#		"short_name": "team-11",										#
# 		"created": "2021-06-22T10:37:33.072878Z",						#
# 		"closed": false,												#
#		"rank": null,													#
# 		"max_entries": null,											#
# 		"league_type": "s",												#
#		"scoring": "c",													#
# 		"admin_entry": null,											#
# 		"start_event": 1,												#
#		"entry_can_leave": false,										#
# 		"entry_can_admin": false,										#
# 		"entry_can_invite": false,										#
# 		"has_cup": true,												#
# 		"cup_league": null,												#
# 		"cup_qualified": null,											#
# 		"entry_rank": 153229,											#
# 		"entry_last_rank": 195322										#
# 	}																	#
#																		#
# 	The "id" can then be used in the default league url: 				#
# 	"https://fantasy.premierleague.com/api/leagues-h2h/{lgId}" 	or 		#
# 	"https://fantasy.premierleague.com/api/leagues-classic/{lgId}" 		#
#																		#
#	League info is NOT stored in the main global 						#
#																		#
############################## LEAGUES ##################################

lg_cnt_fl = "./app/static/data/static/lgCnt/lg_"
lg_data_fl = "./app/static/data/live/active/lg/lg_"

global leagues
leagues = []

global testLg
testLg = 348264;
# CLASSIC:
# https://fantasy.premierleague.com/api/leagues-classic/941528/standings/?page_new_entries=1&page_standings=1&phase=1


# H2H:
# 	  https://fantasy.premierleague.com/api/leagues-h2h/348264/standings/?page_new_entries=1&page_standings=1


global testId
testId = 704118;

global testTp
testTp = 0;

global checkPg 
checkPg = 1;

global lw
lw = 1;

global manCount
manCount = 1;

global pageMax
pageMax = 250000;

global manCntHis
manCntHis = [ 1, 1, 11000000 ];

global lgCountFinished
lgCountFinished = False;

def getLeagues(manId):
	print("getLeagues(manId)", manId )

def guessLeagueCount(lgTp, lgId):
	global manCntHis, lgCountFinished, testLg, testId, testTp, lw

	# first see if we have gotten the total locally
	glolc = getLocalLgCount(lgId)
	glilc = getLiveLgCount(lgId)

	if( glolc > 0 ):
		return glolc
	elif( glilc > 0 ):
		return glilc

	max_steps  	= 12
	lw = 50
	lgCountFinished = False
	lastUpLim = 1

	# first define upper boundary in pages (so times 50 for number of teams in league)
	myTopLims = [1, 100, 500, 1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 40000, 60000, 100000, 125000, 150000, 175000, 200000 ]
	for uplim in myTopLims:
		lwr = checkNext( lgTp, lgId, uplim )
		time.sleep(0.1125)
		lw = lwr['lowest']
		hm = lwr['has_next']
		if(hm==False):
			updTop(uplim)
			updLow(lastUpLim)
			break

		lastUpLim = uplim

	# print("upper page limit now set to", uplim, manCntHis);
	for cn in range(1,max_steps):
		# print("step ", cn, "lgCountFinished", lgCountFinished , manCntHis )
		lwr = checkNext( lgTp, lgId, manCntHis[1] )
		time.sleep(0.225)
		lw = lwr['lowest']
		hm = lwr['has_next']
		lgCountFinished = lwr['found']
		if(hm):
			updLow(manCntHis[1])
		else:
			updTop(manCntHis[1])

		if lgCountFinished:
			break

	# print("myteam rank", getTeamRank(lgTp, lgId, lw) )
	if( not lgCountFinished ):
		lw = int( manCntHis[1] * 50 ) 
	
	saveLocalLgCount(lw,lgId)
	saveLiveLgCount(lw,lgId)
	return lw


def checkNext(lgTp, lgId, pg):
	global lgCountFinished
	# works with lgTp=0
	if( (lgTp==0) and (pg>0) ):
		# 		https://fantasy.premierleague.com/api/leagues-classic/941528/standings/?page_new_entries=1&page_standings=1&phase=1
		url=   "https://fantasy.premierleague.com/api/leagues-classic/" + str( lgId ) + "/standings/?page_new_entries=1&phase=1&page_standings=" + str(pg) 
	elif( (lgTp==1) and (pg>0) ):
		# 	  https://fantasy.premierleague.com/api/leagues-h2h/348264/standings/?page_new_entries=1&page_standings=1
		url= "https://fantasy.premierleague.com/api/leagues-h2h/" + str( lgId ) + "/standings/?page_new_entries=1&page_standings=" + str(pg)
	else:
		retval = {"has_next": False, "lowest": 0,"resCount": 0, "page": pg }
		return retval 

	print("checkNext-url:\t", url)
	res = urlopen(url)
	resData = json.loads(res.read())
	
	hn = resData['standings']['has_next'];
	lpg = resData['standings']['page'];
	resCount = len(resData['standings']['results']);
	lwst = 0
	if( resCount>0 ):
		lwst = getLowestRank( resData['standings']['results'] );

	if( hn ):
		retval = { "page": pg, "has_next": True, "lowest": lwst, "resCount": resCount, "found": False }
	else:
		if(( resCount > 0 ) and ( resCount <= 50 )):
			lgCountFinished = True
			lwst = ( ( int(lpg)-1 ) * 50 ) + resCount
			# print("lgCountFinished now is TRUE =", lwst);
			retval = { "page": pg, "has_next": False, "lowest": lwst, "resCount": resCount, "found": True }
		elif(resCount == 0):
			retval = { "page": pg, "has_next": False, "lowest": 0, "resCount": resCount , "found": False }

	# print("****checkNext****", retval)		
	return retval 

def getLowestRank(resData):
	lowest = resData[0]['rank']
	for r in resData:
		if( ( r['last_rank'] > lowest ) ):
			lowest = r['last_rank']

	# print("getLowestRank", lowest)
	return int(lowest)

def updLow(pg):
	global manCntHis
	if(int(pg) in [0,1] ):
		pg += 1

	manCntHis[0] = pg;
	updCur(pg)

def updCur(pg):
	global manCntHis, pageMax
	if( int(pg) > pageMax ):
		pg = pageMax
	elif( int(pg) < 1 ):
		pg = 1
	else:
		pg = (( int(manCntHis[2]) - int(manCntHis[0]) ) / 2 ) + int(manCntHis[0])  

	manCntHis[1] = int(pg);
	# printmch()

def updTop(pg):
	global manCntHis, pageMax
	if( int(pg) > pageMax ):
		pg = pageMax

	manCntHis[2] = pg;
	updCur(pg)

def printmch():
	print("manCntHis", manCntHis);

def getLocalLgCount(lgId):
	if os.path.exists(lg_cnt_fl + str(lgId) + ".json"):
		olgf = open( lg_cnt_fl + str(lgId) + ".json");
		data_lgs = json.load(olgf)
		olgf.close
		return data_lgs
	else:
		return 0

def saveLocalLgCount(cnt,lgId):
	slc = open(  lg_cnt_fl + str(lgId) + ".json", "w+");
	slc.write( str(cnt) )
	slc.close

def delLocalLgCount(lgId):
	os.remove( lg_cnt_fl + str(lgId) + ".json");

def getLiveLgCount(lgId):
	if os.path.exists(lg_data_fl + str(lgId) + ".json"):
		olgf = open(  lg_data_fl + str(lgId) + ".json");
		data_lgs = json.loads( olgf.read() )
		olgf.close
		# print("getLiveLgCount", str(lgId), 'lgCount' in data_lgs['league'].keys() )
		if( 'lgCount' in data_lgs['league'].keys() ):
			return data_lgs['league']['lgCount'];
		else:
			return 0

	else:
		return 0


def saveLiveLgCount(cnt,lgId):
	if os.path.exists( lg_data_fl + str(lgId) + ".json" ):
		slic = 	 open( lg_data_fl + str(lgId) + ".json" );
		data_liLg = json.load(olgf)
		slic.close
	else:
		return 0

	print("saveLiveLgCount", str(lgId), " cnt", cnt , data_liLg['league'] )
	if( data_liLg['league']['lgCount'] ):
		data_liLg['league']['lgCount'] = cnt
	else:
		data_liLg['league'].append( { "lgCount": cnt } )

	slic2 = open( lg_data_fl + str(lgId) + ".json", "w+");
	slic2.write( json.dumps(data_liLg, indent=4 ) )
	slic2.close
