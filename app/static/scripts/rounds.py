#!/usr/bin/env python3
# pyFPL
# rounds.py

import os
import time
import sys
import json
from urllib.request import urlopen

############################### ROUNDS ##################################
#	In this script we deal with information	about fixture ROUNDS		#
#	(aka events / matchdays / gameweek).								#
#-----------------------------------------------------------------------#
#	There are 38 rounds (rnd/rnds).										#
#	Round 39 will be used to store postponements (pp).					#
#	The FPL only sets a round as active after the deadline transpires	#
#	We consider a round as active when the previous has finished.		#
#	Rounds are stored in the main global at index 0:					#
#		fplData	[ "rounds": [], 										#
#				 ......													#
#				]														#
#																		#
#	FPL returns the following "EVENT" object							#
#		{"id": 1, 														#
#			"name": "Gameweek 1", 										#
#			"deadline_time": "2021-08-13T17:30:00Z", 					#
#			"average_entry_score": 69, 									#
#			"finished": true, 											#
#			"data_checked": true, 										#
#			"highest_scoring_entry": 5059647, 							#
#			"deadline_time_epoch": 1628875800, 							#
#			"deadline_time_game_offset": 0, 							#
#			"highest_score": 150, 										#
#			"is_previous": false, 										#
#			"is_current": false, 										#
#			"is_next": false, 											#
#			"cup_leagues_created": false, 								#
#			"h2h_ko_matches_created": false, 							#
#			"chip_plays": [												#
#				{"chip_name": "bboost", "num_played": 145658}, 			#
#				{"chip_name": "3xc", "num_played": 225749}				#
#				{"chip_name": "freehit", "num_played": 0}, 				#
#				{"chip_name": "wildcard", "num_played": 0},				#
#			],	 														#
#			"most_selected": 275, 										#
#			"most_transferred_in": 1, 									#
#			"top_element": 277, 										#
#			"top_element_info": {"id": 277, "points": 20}, 				#
#			"transfers_made": 0, 										#
#			"most_captained": 233, 										#
#			"most_vice_captained": 277									#
#	}																	#
############################### ROUNDS ##################################

import app.static.scripts.getData as mod_data

rnds_file 	= "./app/static/data/static/rounds.json"
global rounds
rounds = []

def getRnds():
	if( mod_data.infoRt(2) ):
		data_rnds = getRemoteRnds()
	else:
		data_rnds = getLocalRnds()

	global rounds
	rounds = data_rnds
	return data_rnds


def getLocalRnds():
	if( len(rounds) > 0 ):
		# print("getLocalRnds rounds size", len(rounds) )
		data_rnds = rounds
	elif( os.path.exists( rnds_file )):
		foRnds = open( rnds_file )
		data_rnds = json.load( foRnds )
		foRnds.close
	else:
		# print("rnds_file does NOT exists. using remote")
		data_rnds = getRemoteRnds()

	return data_rnds


def getRemoteRnds():
	response = mod_data.getStatic("r")
	rnf = open( rnds_file , "w+")
	rnf.write( json.dumps( response["events"], indent=4) )
	rnf.close
	mod_data.fplDataTS[0] = float(time.time())
	return rounds
