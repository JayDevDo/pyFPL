#!/usr/bin/env python3
# clubsCls.py


class Club():

	ballerIds 	= 	[]
	clubId 		= 	0
	dfFPL 		= 	[ {'df':0, 'attack': 0, 'defence': 0 , 'overall': 0 },	{'df':0, 'attack': 0, 'defence': 0 , 'overall': 0 } ]
	dfUSR 		= 	[ {'df':0, 'attack': 0, 'defence': 0 , 'overall': 0 },	{'df':0, 'attack': 0, 'defence': 0 , 'overall': 0 } ]
	draws 		= 	0
	lastUpdGW 	= 	0
	longName 	= 	"lName"
	losses 		= 	0
	nickName 	= 	"nName"
	posPoints 	= 	[0,0,0,0]
	pointsTtl 	= 	0
	shortName 	= 	"sName"
	wins 		= 	0


	def __init__(self, *args, **kwds):
		print("--New club class--\nArgs:\t", args, "\nKwds:\t", kwds )
		self.clubId = int(kwds['id'])


	def toString(self):
		return "".join([	"--Club class.toString --\nArgs:\n", 
					"\nclubId:\t", 		str(self.clubId),
					"\nlongName:\t", 	self.longName,
					"\nshortName:\t", 	self.shortName,
					"\nnickName:\t", 	self.nickName,
					"\nballerIds:\t", 	str(self.ballerIds),
					"\nwins:\t", 		str(self.wins),
					"\nlosses:\t", 		str(self.losses),
					"\ndraws:\t", 		str(self.draws),
					"\nposPoints:\t", 	str(self.posPoints),
					"\npointsTtl:\t", 	str(self.pointsTtl),
					"\ndfFPL:\t", 		str(self.dfFPL),
					"\ndfUSR:\t", 		str(self.dfUSR),
					"\nlastUpdGW:\t", 	str(self.lastUpdGW)
		])

	"""
	Getters :
	"""	

	def getClubId(self):
		return self.clubId

	def getClubSNm(self):
		return self.shortName

	def getClubLNm(self):
		return self.longName

	def getClubNNm(self):
		return self.nickName

	def getClubDF(self, userDF=False, loc="H"):
		lc = 0
		if ( loc == "A" ):
			lc = 1

		if(userDF):
			return self.dfUSR[lc]['df']
		else:
			return self.dfFPL[lc]['df']


	def getLastGWUpdate(self):
		return self.lastUpdGW

	def getPosPoints(self, pos):
		return self.posPoints[pos]


	"""
	Setters :
	"""	

	def setLastGWUpdate(self, gw):
		self.lastUpdGW = gw

	def setPosPoints(self, pos, points):
		self.posPoints[pos] = points




testClub = Club(id=1)
print("Test clubClass:\t", testClub.toString() )
print("\n\nTest club id:\t", testClub.getClubId() )

print("\n\n\nTest club names:", 
		"\ngetClubSNm\t", testClub.getClubSNm() ,
		"\ngetClubLNm\t", testClub.getClubLNm() ,
		"\ngetClubNNm\t", testClub.getClubNNm() 
)

print("Test club getClubDF(F-H):\t", testClub.getClubDF(False,"H")  )
print("Test club getClubDF(T-H):\t", testClub.getClubDF(True,"H")  )
print("Test club getClubDF(F-A):\t", testClub.getClubDF(False,"A")  )
print("Test club getClubDF(T-A):\t", testClub.getClubDF(True,"A")  )

