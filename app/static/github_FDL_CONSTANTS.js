let changDFviewArr = ["sum", "count", "avg"];
let changDFviewIdx = 0

let myFPLTeamIds = [];

let FPLTeamsFull = [
        {       shortNm: "TFL",
                id: 0,
                locDF: [1,1] ,// [HOME,AWAY]
                ownDFhis: [] ,// from events
                oppDFhis: [] ,// from events
                longNm: "TeamsFull",
                altNm: "placeholder",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "ARS",
                id: 1,
                locDF: [4,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0  ] ,// from events
                longNm: "Arsenal",
                altNm: "Gunners",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "AVL",
                id: 2,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Aston Villa",
                altNm: "Villains",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "BRE",
                id: 3,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Brentford",
                altNm: "Bees",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "BHA",
                id: 4,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Brighton",
                altNm: "Seagulls",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "BUR",
                id: 5,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Burnley",
                altNm: "Clarets",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "CHE",
                id: 6,
                locDF: [5,4] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Chelsea",
                altNm: "Blues",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "CRY",
                id: 7,
                locDF: [3,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Crystal Palace",
                altNm: "Eagles",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "EVE",
                id: 8,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Everton",
                altNm: "Toffees",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "LEI",
                id: 9,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Leicester",
                altNm: "Foxes",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "LEE",
                id: 10,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Leeds",
                altNm: "Peacocks",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "LIV",
                id: 11,
                locDF: [5,4] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Liverpool",
                altNm: "Reds",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "MNC",
                id: 12,
                locDF: [5,4] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Man city",
                altNm: "Citizens",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "MUN",
                id: 13,
                locDF: [4,4] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Man utd",
                altNm: "Red Devils",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "NEW",
                id: 14,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Newcastle",
                altNm: "Magpies",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "NOR",
                id: 15,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Norwich",
                altNm: "Canaries",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "SOU",
                id: 16,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Southampton",
                altNm: "Saints",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "TOT",
                id: 17,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0] ,// from events
                longNm: "Tottenham",
                altNm: "Spurs",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "WAT",
                id: 18,
                locDF: [2,2] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Watford",
                altNm: "Hornets",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "WHU",
                id: 19,
                locDF: [4,4] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "West Ham",
                altNm: "Hammers",
                players: [],
                ppgames: [] 
        },
        {       shortNm: "WOL",
                id: 20,
                locDF: [3,3] ,// [HOME,AWAY]
                ownDFhis: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,
                oppDFhis: [   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,// from events
                longNm: "Wanderers",
                altNm: "Wolves",
                players: [],
                ppgames: [] 
        }
];

