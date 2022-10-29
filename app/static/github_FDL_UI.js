let gamesOverview = {
                        fixedColumns: 3,
                        finishedRounds: 11,
                        eventWndwStart: 12,
                        currentRnd: 12,
                        rndsToShow: 5,
                        eventWndwEnd: 16,
                        userDF: false,
                        hasPP: true,
                        postponedGameIds: [],
                        postponedGames: []
                    }

showEvent = (id)=>{ for(let e=0; e < fixtures.length; e++){ if( fixtures[e].id == id ){ return fixtures[e]; }}}
getRndsToShow = ()=>{ return gamesOverview.rndsToShow; } ;
getEventWndwStart = ()=>{ return gamesOverview.eventWndwStart; } ;
getEventWndwEnd  =  ()=>{ return gamesOverview.eventWndwEnd; } ;

setEventWndwStart = (ews)=>{
    gamesOverview.eventWndwStart = parseInt(ews);
    setEventWndwEnd();
    return gamesOverview.eventWndwStart;
} ;

setRndsToShow = (rts)=>{
    gamesOverview.rndsToShow = parseInt(rts);
    setEventWndwEnd();
    return gamesOverview.rndsToShow ;
};

setEventWndwEnd = ()=>{
    let evWndw = ( (getEventWndwStart()+getRndsToShow()) > 38 )? 39:( getEventWndwStart() + getRndsToShow() -1 );
    gamesOverview.eventWndwEnd = evWndw ;
};

hideEventClmn = (rnd)=>{
    let crit = "td[evrnd=" + rnd + "]" ;
    let gms  = $(crit).get() ;
    let hdr  = $("th[evrnd=" + rnd + "]" ) ;
    $.each( hdr, function(index,gm){ $(gm).addClass("clmnHide"); } );
    $.each( gms, function(index,gm){ $(gm).addClass("clmnHide"); } );
}

showEventClmn = (rnd)=>{
    let crit = "td[evrnd=" + rnd + "]" ;
    let gms  = $(crit).get() ;
    let hdr  = $("th[evrnd=" + rnd + "]" ) ;
    $.each( hdr, function(index,gmh){ $(gmh).removeClass("clmnHide"); } );
    $.each( gms, function(index,gm){ $(gm).removeClass("clmnHide"); } );
}

showEventWindow = ()=>{
    /* Update the event window with the input selection from the page */
    setEventWndwEnd();
    let st = gamesOverview.eventWndwStart;
    let en = gamesOverview.eventWndwEnd;
    for(let p = 1; p < st ; p++){hideEventClmn(p);}
    for(let s = st; s <= en ; s++){showEventClmn(s);}
    for(let f = (en+1) ; f <= 39 ; f++){hideEventClmn(f); }
    if(gamesOverview.postponedGames.length>0){ showEventClmn(39); }
    updateTotalDF(changDFviewIdx);
    sortTable()
    showHiddenTable()
    $("#curRound").text(st.toString() );
    console.log("event window applied", st, en)
    return "event window applied"
}

changDFview = ()=>{
    if( (changDFviewIdx+1) > 2 ){
        changDFviewIdx = 0;
    }else{
        changDFviewIdx += 1;
    }
    updateTotalDF(changDFviewIdx)
}

updateTotalDF = (dfType)=>{
    let tblRows = $("#eventTable tr").get();
    $.each(
        tblRows,
        function(index, rw){
            let selDF   = 0;
            let selDFcnt= 0;
            let tmGames = $(rw).children(".evtTeamBlock");
            $.each(
                tmGames,
                function(i,gm){
                    let slctGm = $(gm).attr("evrnd");
                    /* let gmDF = parseInt(gm.getAttribute("df")) || 0; */
                    let cl = gm.classList;
                    let ignoreGmDF = false ;
                    let gmDF = 0
                    ignoreGmDF = ( $(gm).hasClass("clmnHide"))? true:false ;
                    if( ignoreGmDF == false ){
                        if( $(gm).children("span").length>0 ){
                            let spanDFaccum = 0
                            let spanCount = 0
                            $.each(
                                    $(gm).children("span").get(),
                                    function(s, spdf){
                                        if( $(spdf).attr("ppgame") == "False" ){
                                            spanDFaccum += parseInt( $(spdf).attr("df")) || 0;
                                            spanCount += 1
                                        }
                                    }
                            )
                            selDF += spanDFaccum;
                            selDFcnt += spanCount;
                        }else{
                            gmDF = parseInt( $(gm).attr("df")) || 0;
                            selDF += gmDF;
                        }
                    }
                }
            );
            let dfAvg = ( parseInt(selDF) / parseInt(selDFcnt) ).toString().slice(0,4);
            let dfStr = ""

            if(dfType==0){
                dfStr = selDF.toString()
            }else if(dfType==1){
                dfStr = selDFcnt.toString()
            }else if(dfType==2){
                dfStr = dfAvg.toString()
            }else{
                dfStr = selDF.toString()
            }

            $(rw).children("th.dfc").text(dfStr);
            $("#tmDFhdr").text(changDFviewArr[dfType])
        }
    );
    sortTable()
}

sortTable = ()=>{
    /* Sort table based on difficulty of selected next games */
    let rows = $('#fxtrTbl tbody tr').get();
    rows.sort(
        function (a, b) {
            let A = $(a).children('th.dfc').text();
            let B = $(b).children('th.dfc').text();
            /*
            if (parseInt(A) < parseInt(B)) { return -1; }
            if (parseInt(A) > parseInt(B)) { return 1; }
            */
            if (parseFloat(A) < parseFloat(B)) { return -1; }
            if (parseFloat(A) > parseFloat(B)) { return 1; }
            return 0;
        }
    );
    $.each(rows, function (index, row) {
        // console.log("index", row)
        $('#fxtrTbl').children('tbody').append(row);
    });
}

showHiddenTable = ()=>{
    let hasHidden = $('#hiddenTbl tbody tr').length;
    if( hasHidden > 0 ){
        $("#hiddenTblCnt tbody").show()
        $("#hiddenTbl tbody").show()
        $("#hiddenTbl thead").show()
    }else{
        $("#hiddenTblCnt tbody").hide()
        $("#hiddenTbl tbody").hide()
        $("#hiddenTbl thead").hide()
    }
   sortTable()
}

hideTeamRow = (tmNm)=>{
    let row = $('#eventTable tr[id='+tmNm+ ']').get();
    if( $('#eventTable tr[id='+tmNm+ ']').length == 0 ){
        $('#hiddenTbl tr[id='+tmNm+ ']')
            .detach()
            .appendTo("#eventTable");
            $('#eventTable tr[id='+tmNm+ '] > input').prop("unchecked")
    }else{
        $('#eventTable tr[id='+tmNm+ ']')
            .detach()
            .appendTo("#hiddenTbl tbody");
            $('#hiddenTbl tr[id='+tmNm+ '] > input').prop("checked")
    }
    showHiddenTable()
}

showAllTeams = ()=>{
   let mvRow = $("#hiddenTbl tbody tr" ).get();
    $.each( mvRow, (i, row)=>{ hideTeamRow( $(row).attr("id") ) })
    showHiddenTable()
}

showHiddenTable = ()=>{
    let hasHidden = $('#hiddenTbl tbody tr').length;
    if( hasHidden > 0 ){
        $("#hiddenTblCnt tbody").show()
        $("#hiddenTbl tbody").show()
        $("#hiddenTbl thead").show()
    }else{
        $("#hiddenTblCnt tbody").hide()
        $("#hiddenTbl tbody").hide()
        $("#hiddenTbl thead").hide()
    }
   sortTable()
}

showEventWindow()
