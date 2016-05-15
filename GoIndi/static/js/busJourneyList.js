function showBusJourneyList(busList){
	var output = "<br/><div id='busBox' hidden><table width='100%'><tr>";
	for (i = 0; i < busList.length; i++) { 
		var busDetails = busList[i].parts[0];
		var priceList = busDetails.price;
		var priceArr = priceList.split(",");
		var price = priceArr[0]
		var travelSpecificWid = travelSpecificsWidget(busDetails.source,busDetails.destination,busDetails.arrival,busDetails.departure,busDetails.duration);
		var startingFrom='';
		if (priceArr.length>1){
			startingFrom="Staring from&nbsp;&nbsp;"
		}
		output = output + "<tr><td bgcolor='WhiteSmoke'><div class='row-eq-height'><table width = '100%'><tr><td width = '75%' style ='text-align:left'>&nbsp;&nbsp;<font color = '#056273'><b>"+busDetails.carrierName+"</b></td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-warning' id = '"+busDetails.id+"' onmouseover='this.html=\"Select\"' onmouseout='this.html=\""+busDetails.availableSeats+" Seats\"'>"+busDetails.availableSeats+" Seats</button>&nbsp;&nbsp;</td></tr></table></div></td></tr><tr><td><br/><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey' size='1'>"+busDetails.busType+"<br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><font color='grey' size='1'>"+startingFrom+"</font><h4 style='white-space: nowrap;'><font color='green'>&#8377 "+price+"/-</font></h4></td></tr></table></div></div></td></tr>"
	}
	output = output +"</table></div>";
	$("#busData").empty();
	document.getElementById("busData").innerHTML = output;
	$("#busBox").fadeIn();	
}

