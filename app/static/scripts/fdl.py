#!/usr/bin/env python3
# pyFPL
# clubs.py

import os
import time
import sys
import json
from urllib.request import urlopen

################################### FDL #########################################
#	In this script we deal with information	about FDL							#
#	(aka Fixture Difficulty List).												#
#  -------------------------------------------------------------------  		#
#	DF = difficulty factor														#
# 	In our Fixture Difficulty List (FDL) we'll make a table of all fixtures 	#
#	Each team on 1 row. For each fixture the name location (Home/Away) and 		#
#	DF of the opponent will be shown. 											#
#																				#
#	We'll calculate the sum of opponent DF for the chosen event window.			#
#	We'll keep track of postponed and replanned games and add them to the 		#
#	new gameweek (round).														#
#																				#
#	Clubs can be selected to be compared.										#
#																				#
#	Data needed:																#
#		fplData[1]['data']	--> fixtures										#
#		fplData[2]['data'] 	--> clubs											#
#																				#
#	The event window will be dealt with in JAVA script.							#
#																				#
################################### FDL #########################################

import app.static.scripts.getData 	as mod_data
import app.static.scripts.clubs 	as mod_clb
import app.static.scripts.fixtures 	as mod_fxt

global fdl

fdl = 	[
			{"id": "evw", 	"data": []  }, #0
			{"id": "clubs", "data": []  }, #1
			{"id": "fxtrs", "data": []  }, #2
			{"id": "ppgms", "data": []  }  #3
		]

fdl_file 		= "./app/static/data/live/active/fdl.json"
pp_file 		= "./app/static/data/static/ppFxtrs.json"
clubs_df_file 	= "./app/static/data/static/clubs_df.json"


global fd_clubs
fd_clubs =	[
				{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},
				{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0}
			];

global fxtrTbl
fxtrTbl = []

def loadFDLData():
	global fdl
	fdl[0]['data']= [{"evwStart":14},{"evwEnd":16},{"evwPeriod":3},{"evwShowHddn":False },{"evwShowPP":True}];
	fdl[1]['data'] = mod_clb.getClubs('r')
	fdl[2]['data'] = mod_fxt.getFxtrs('r')
	fdl[3]['data'] = getLocalppFxtrs()
	svFDL(fdl)
	return fdl


def getLocalppFxtrs():
	global fdl
	if( os.path.exists( pp_file )):
		foppf = open( pp_file )
		data_ppFxtrs = json.load(foppf)
		foppf.close
	else:
		pass
		# print("pp_file does NOT exists !! ")

	# print("data_ppFxtrs", json.dumps(data_ppFxtrs[0]['unplanned'],indent=4))
	for clb in fdl[1]['data']:
		clb['ppgc'] = ppFxtrClubCount( data_ppFxtrs[0]['unplanned'], clb['id'] )
		clb['df'] = getLclDFData( clb['id'] )

	return data_ppFxtrs[0]

def svFDL(dict):
	flf = open( fdl_file, "w+")
	flf.write( json.dumps( dict, indent=4) )
	flf.close

def ppFxtrClubCount(ppgms, clubId):
	retval = 0
	if( len(ppgms) > 0 ):
		for pf in ppgms:
			# print("pf keys", pf.keys() )
			if( (int(pf['team_h_id']) == clubId) or (int(pf['team_a_id']) == clubId) ):
				retval +=1

	return retval

def getLclDFData(clubId):
	if( os.path.exists( clubs_df_file )):
		cdfo = open( clubs_df_file )
		data_clb_df = json.load(cdfo)
		cdfo.close
		# print("data_ppFxtrs", json.dumps(data_ppFxtrs[0]['unplanned'],indent=4))
		for clb in data_clb_df:
			if( clubId == int(clb['id']) ):
				return clb['locDF']

	else:
		pass
		# print("clubs_df_file does NOT exists !! ")

	return [0,0]
