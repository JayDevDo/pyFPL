#!/usr/bin/env python3
# pyFPL
# rounds.py

import os
import sys
import json

############################### ROUNDS ##################################
#	In this script we deal with information	about fixture ROUNDS		#
#	(aka events / matchdays / gameweek).								#
#-----------------------------------------------------------------------#
#	There are 38 rounds (rnd/rnds).										#
#	Round 39 will be used to store postponements (pp).					#
#	The FPL only sets a round as active after the deadline transpires	#
#	We consider a round as active when the previous has finished.		#
#	Rounds are stored in the main global at index 0:					#
#																		#
#		fplData	[ "rounds": [], 										#
#				 ......													#
#				]														#
#																		#
############################### ROUNDS ##################################

import app.static.scripts.rounds as mod_rnd

rnds_file 	= "./app/static/data/static/rounds.json"

def getCurrentRnd():
	gw = 14
	if( os.path.exists( rnds_file )):
		foRnds = open( rnds_file )
		data_rnds = json.load( foRnds )
		foRnds.close
	else:
		return gw

	for r in data_rnds:
		if( r["is_current"] ):
			# print("return currentRnd", str(r["id"]) )
			gw = r["id"]
		elif( r["is_next"] and (r["id"] != 1) ):
			print("return isNext", str(r["id"]) )

	return gw



def getCurrentDeadline():
	if( os.path.exists( rnds_file )):
		foRnds = open( rnds_file )
		data_rnds = json.load( foRnds )
		foRnds.close
	else:
		return "2022-08-27T11:59:59Z"

	for r in data_rnds:
		if( r["is_current"] ):
			print("return getCurrentDeadline\t", str(r["id"]) , "\tddln time:\t", r["deadline_time"] , "\tepoch:\t", r["deadline_time_epoch"])
			return r["deadline_time_epoch"]
