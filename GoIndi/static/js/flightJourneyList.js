var radionames = []
var isSelected =0
function showFlightJourneyList(transportList){
	if(transportList.length==0){
		document.getElementById("resultsWid").innerHTML = ""
				return;
	}
	if($( "#priceSort" ).hasClass("active")){
		SortListByPrice(transportList);
	} else {
		SortListByDuration(transportList);
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
	var output = "<div class='row-eq-height'><div class='col-sm-12 col-height col-middle nopaddingatall'>"+travelSplitter+"</div></div><div class='row-eq-height'><div id='flightBox' hidden><table width='100%'><tr>";
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
					var end = "&#9873;"
				}else{
					var end = "(+)"
				}
				travelSplitterParts = travelSplitterParts + "<td bgcolor='#dcdcdc' width='"+customWidth+"%' style='text-align:center'><div class='carrierLabel'>"+routeArr[q]+"</div></td><td bgcolor='#dcdcdc' width='4%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+end+"</font></b></td>";
				q=q+1
			}
			travelSplitter = travelSplitter + "<table width='100%' style = 'text-align:center'><tr><td bgcolor='#dcdcdc' width='4%'><b><font color = '#dfa158' style='white-space: nowrap;' >&#9873;</font></b></td>"+travelSplitterParts+"</tr></table>"
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
				
			var individualJourneyDetails = "<div class='detailsBox'> <table width='100%'><tr ><td ><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey'>"+stopsEle+"<br/>&nbsp;</div><div class='col-sm-9 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font></div></div></tr></table></div>"

	
		
			
				
				
				
				output = output + "<div class='flightMain' id = 'main"+transportTotalDetails.id+"'><tr><td>&nbsp;</td></tr><tr><td bgcolor='WhiteSmoke'><table width='100%' class='shadowTable'><tr><td><div class='row-eq-height' ><div style=' background-color:#dcdcdc;'><div class='col-sm-12 col-height col-middle nopaddingatall'><div>"+travelSplitter+"</div></div></div><div class='row-eq-height'><div class='col-sm-10 col-height col-middle'><br/><div>"+individualJourneyDetails+"</div></div><div class='col-sm-2 col-height col-middle'><table width='100%'><tr><td><button type='button' class='btn btn-warning sameLine'  data-toggle='modal' data-target='#details"+transportTotalDetails.id+"'>Detail & Book</button><br/><div class='sameLine'><h4 style='white-space: nowrap;'><font color='green'>&#8377 "+transportTotalDetails.price+"/-</font></h4></div></td></tr></table></div></div></td></tr></table></td></tr><tr><td>";
				
				output = output + "<div class='modal fade modal-wide' id='details"+transportTotalDetails.id+"' role='dialog'><div class='modal-dialog'><div class='modal-content'><div class='modal-body'><button type='button' class='close' data-dismiss='modal'>&times;</button>"+getModalForFlights(transportList[i].parts,transportTotalDetails.id)+"</div></div></div></div></td></tr></div>";
				
	}
	output = output + "</table></div>"
	//binding data to flights table
		$("#resultsWid").empty();
		document.getElementById("resultsWid").innerHTML = output;
		document.getElementById("resultsWid").setAttribute("route",transportList[0].full[0].route)
		document.getElementById("resultsWid").setAttribute("routeType","flight")
	for(var l=0; l<radionames.length;l++){
		$("input:radio[name='"+radionames[l]+"']").change(function(){
			var loader = $(this).attr('loader');
			 $('#'+loader).hide()
			var id = $(this).attr('class');
			var carrierType = $(this).attr('carrierType');
			if(carrierType=='train'){
				var availiablityCallId = document.getElementById($(this).attr("availiablityCallId"))
				var availiablityId = document.getElementById($(this).attr("availiablityId"))
				$(availiablityId).hide();
				$(availiablityCallId).show();
				availiablityCallId.setAttribute('trainClass',$(this).attr("trainClass"))
				availiablityCallId.setAttribute('source',$(this).attr("source"))
				availiablityCallId.setAttribute('destination',$(this).attr("destination"))
				availiablityCallId.setAttribute('trainNumber',$(this).attr("trainNumber"))
			}
			getTotalPrice(id);
		});
	}
	$(".booking").click(function() {
			var id = $(this).attr("id").split("book")[1];
			var bookingLink = $('input[name=radio'+id+']:checked').attr('bookingLink')
			var win = window.open(bookingLink, '_blank');
			win.focus();
	});
	$(".availabilityCall").click(function(){
			  
			  var source = $(this).attr('source');
			  var destination = $(this).attr('destination');
			  var trainClass = $(this).attr('trainClass');
			  var trainNumber = $(this).attr('trainNumber');
			  var id = $(this).attr('id');
			  $("#"+id).hide();
			  var loader = $(this).attr('loader');
			 $('#'+loader).show()
			  var availabilityDataId = $(this).attr("availiablityid")
			  $.getJSON('http://localhost:8000/train/availability?source='+source+'&destination='+destination+'&trainClass='+trainClass+'&trainNumber='+trainNumber+'&journeyDate='+journeyDate+'&quota=GN', function(data, err) {
					var availList = data.availability;
					if(availList.length==0){
						var availData = "Not Available"
					} else {
						var availData = availList[0].status
					}
					
					$('#'+loader).hide()
					var availabilityData = document.getElementById(availabilityDataId)
					availabilityData.innerHTML=availData;
					$("#"+availabilityDataId).show();
			  });
		});
		$("#flightBox").fadeIn();
		
		for (i = 0; i < transportList.length; i++) { 
			var transportTotalDetails = transportList[i].full[0];
			for (j = 0; j < transportList[i].parts.length;j++ ){
				var transportDetailsId = transportList[i].parts[j].id + 'divBox';
				
			}
		}
		
}