var radionames = []
var isSelected =0
function showFlightJourneyList(transportList){
	if(transportList.length==0){
		
				return;
	}
	if($( "#priceSort" ).hasClass("active")){
		SortListByPrice(transportList);
	} else {
		SortListByDuration(transportList);
	}
	if(transportList.length==0){
		
		return;
	}
	if($( "#priceSort" ).hasClass("active")){
		SortListByPrice(transportList);
	} else {
		SortListByDuration(transportList);
	}
    var routeForMain = transportList[0].full[0].route
	var routeForArrayMain = routeForMain.split(",")
	var travelSplitter = ''
		if(routeForArrayMain.length>3){
			if(routeForArrayMain.length ==5){
				customWidth = 44
			} else if (routeForArrayMain.length ==7){
				customWidth = 28
			}
			travelSplitterParts = ''
			for (var q = 1; q < routeForArrayMain.length;q++ ){
				travelSplitterParts = travelSplitterParts + "<td width='"+customWidth+"%' style='text-align:center'><img src='/static/images/"+routeForArrayMain[q]+".png'/></td><td width='4%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+routeForArrayMain[q+1]+"</font></b></td>";
				q=q+1
			}
			travelSplitter = travelSplitter + "<table width='100%' style = 'text-align:center'><tr><td width='1%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+routeForArrayMain[0]+"</font></b></td>"+travelSplitterParts+"</tr></table>"
		}
		var outputModal=''
	var output = "<br/><br/><div class='row-eq-height'><div class='col-sm-12 col-height col-middle nopaddingatall'>"+travelSplitter+"</div></div><div class='row-eq-height'><div id='flightBox' hidden>";
	for (i = 0; i < transportList.length; i++) { 
		var transportTotalDetails = transportList[i].full[0];
        var transportTotaljourney = "";
		
		var journeyDividerContent = "";
		var individualJourneyDetails = "";
		var summary = "<br/>";
		var fontSize = 'h4'
		var routeInd = ' ,'
		var stops=0
		
		for ( var j = 0; j < transportList[i].parts.length;j++ ){
			if(transportList[i].parts[j].mode =="flight"){
				for ( var t = 0; t < transportList[i].parts[j].subParts.length;t++ ){
					routeInd = routeInd + "<img src='"+transportList[i].parts[j].subParts[t].carrierName+"'/>"
					if(t!=transportList[i].parts[j].subParts.length-1){
						routeInd = routeInd+"+"
					}
				}
				routeInd = routeInd +", ,"
				if(transportList[i].parts[j].subParts.length>1){
					stops = transportList[i].parts[j].subParts.length-1
				}
			} else {
				routeInd = routeInd + transportList[i].parts[j].subParts[0].carrierName +", ,"
			}
		}
		var routeArr = routeInd.split(",")
		var travelSplitter = ''
		
		if(routeArr.length>4){
			if(routeArr.length ==6){
				customWidth = 44
				stops = stops+1
			} else if (routeArr.length ==8){
				customWidth = 28
				stops = stops+2
			}
			travelSplitterParts = ''
			for (var q = 1; q < routeArr.length-1;q++ ){
				if(q==routeArr.length-3){
					var end = "&#8855;"
				}else{
					var end = "(+)"
				}
				travelSplitterParts = travelSplitterParts + "<td bgcolor='#dcdcdc' width='"+customWidth+"%' style='text-align:center'><div class='carrierLabel'>"+routeArr[q]+"</div></td><td bgcolor='#dcdcdc' width='4%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+end+"</font></b></td>";
				q=q+1
			}
			travelSplitter = travelSplitter + "<table width='100%' style = 'text-align:center'><tr><td bgcolor='#dcdcdc' width='4%'><b><font color = '#dfa158' style='white-space: nowrap;' >&#8855;</font></b></td>"+travelSplitterParts+"</tr></table>"
		} else {
			travelSplitter = "<table width='100%' style = 'text-align:left'><tr><td bgcolor='#dcdcdc'><div class='carrierLabel'>&nbsp;&nbsp;" + routeArr[1] + "</div></td></tr></table>"
		}
		
		if(stops == 0){
			var stopsEle = "Direct"
		} else if (stops == 1){
			var stopsEle = "1 Stop"
		}else{
			var stopsEle = stops+" Stops"
		}
			
			//details of journey
			var travelSpecificWid = travelSpecificsWidget(routeForArrayMain[0],routeForArrayMain[routeForArrayMain.length-1],transportTotalDetails.arrival,transportTotalDetails.departure,transportTotalDetails.duration,transportTotalDetails.arrivalDay,transportTotalDetails.departureDay);
				
			var individualJourneyDetails = "<div class='detailsBox'>"+travelSpecificWid+"</div>"

	
		
			
				
				
				
				output = output + "<div>&nbsp;</div><a href='#pagefour' data-transition='slide' id='link"+transportTotalDetails.id+"' targetId='details"+transportTotalDetails.id+"'><div class='trainMain' id = 'main"+transportTotalDetails.id+"'><table width='100%' class='rcorners'><tr><td bgcolor='WhiteSmoke'><div class='row-eq-height'><div class='col-sm-12 col-height col-middle nopaddingatall'><div>"+travelSplitter+"</div></div></div><div class='row-eq-height'><div class='col-sm-12 col-height col-middle'><br/><table width='100%'><tr><td width='75%'>"+individualJourneyDetails+"</td><td width='25%' style='text-align:right'><div class='sameLine'><h5 style='white-space: nowrap;'><font color='green'>&#8377 "+transportTotalDetails.price+"/- </font></h6></div><div class='sameLine'><font color='grey'><span class='glyphicon glyphicon glyphicon-chevron-right'></span></font></div></td></tr></table></div></div></td></tr></table></div></a>";
				
				
				outputModal = outputModal + "<div hidden class='modalView' id='details"+transportTotalDetails.id+"'>"+getModalForFlights(transportList[i].parts,transportTotalDetails.id)+"</div>";
				
	}
	output = output + "</div></div>"
	//binding data to flights table
		$("#resultsWid").empty();
		document.getElementById("modal").innerHTML = outputModal;
		document.getElementById("resultsWid").innerHTML = output;
		document.getElementById("resultsWid").setAttribute("route",transportList[0].full[0].route)
		document.getElementById("resultsWid").setAttribute("routeType","flight")
	for(var l=0; l<radionames.length;l++){
		$("input:radio[name='"+radionames[l]+"']").change(function(){
			var id = $(this).attr('class');
			getTotalPrice(id);
		});
	}
	$(".booking").click(function() {
			var id = $(this).attr("id").split("book")[1];
			var bookingLink = $('input[name=radio'+id+']:checked').attr('bookingLink')
			var win = window.open(bookingLink, '_blank');
			win.focus();
	});
		$("#flightBox").fadeIn();
		
		for (i = 0; i < transportList.length; i++) { 
			var transportTotalDetails = transportList[i].full[0];
			$("#link"+transportTotalDetails.id).click(function() {
				var targetIdStr = $(this).attr("targetId");
				
				$(".modalView").hide();
				$("#"+targetIdStr).show();
				
			});
			for (j = 0; j < transportList[i].parts.length;j++ ){
				var transportDetailsId = transportList[i].parts[j].id + 'divBox';
				
			}
		}
		
}