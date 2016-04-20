function showBusJourneyList(busList){
	var output = "<br/><div id='busBox' hidden>";
	for (i = 0; i < busList.length; i++) { 
		var busDetails = busList[i].parts[0];
		var travelSpecificWid = travelSpecificsWidget(busDetails.source,busDetails.destination,busDetails.arrival,busDetails.departure,busDetails.duration);
		output = output + "<div class='panel panel-default'><div class='panel-body'><div class='row-eq-height'><table width = '100%'><tr><td width = '75%' style ='text-align:left'><img src='/static/images/"+busDetails.site+".png' ></img></td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-success btn-arrow-right' id = '"+busDetails.id+"'>Book</button></td></tr></table></div><hr><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey'><b>"+busDetails.carrierName+"</b><br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><h4 style='white-space: nowrap;'><font color='green'>&#8377 "+busDetails.price+"/-</font><h4></td></tr></table></div></div></div></div>"
	}
	output = output +"</div>";
	$("#busData").empty();
	document.getElementById("busData").innerHTML = output;
	$("#busBox").fadeIn();	
}

