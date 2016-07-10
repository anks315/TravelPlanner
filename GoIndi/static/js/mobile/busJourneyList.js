function showBusJourneyList(busList){
	if(busList.length==0){
		
		return;
	}
	if($( "#priceSort" ).hasClass("active")){
		SortListByPrice(busList);
	} else {
		SortListByDuration(busList);
	}
	
	var output = "<br/><div id='busBox' hidden>";
	for (i = 0; i < busList.length; i++) { 
		var busDetails = busList[i].parts[0];
		var priceList = busDetails.price;
		var priceArr = priceList.split(",");
		var price = priceArr[0]
		var travelSpecificWid = travelSpecificsWidget(busDetails.source,busDetails.destination,busDetails.arrival,busDetails.departure,busDetails.duration,busDetails.arrivalDay,busDetails.departureDay);
		var startingFrom='';
		if (priceArr.length>1){
			startingFrom="Staring from&nbsp;&nbsp;"
		}
		output = output + "<div>&nbsp;</div><a href="+busDetails.bookingLink+"><table width='100%'><tr><td bgcolor='#dcdcdc'><div class='row-eq-height'><table width = '100%'><tr><td width = '75%' style ='text-align:left;padding: 7px;'><div class='carrierLabel'>&nbsp;&nbsp;"+busDetails.carrierName+"</td><td width = '25%' style ='text-align:right'></td></tr></table></div></td></tr><tr><td bgcolor='WhiteSmoke'><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><br/><font color = '#79b9e1' size='1'>"+busDetails.busType+"</font></div></div><div class='row-eq-height'><div class='col-sm-12 col-height col-middle' style ='text-align:center'><table width='100%'><tr><td width='75%'>"+travelSpecificWid+"</td><td width='25%' style='text-align:right'><table width = '100%' style ='text-align:right'><tr><td><div class='sameLine'><h5 style='white-space: nowrap;'><font color='green'>&#8377 "+price+"/-</font></h5></div><div class='sameLine'><font color='grey'><span class='glyphicon glyphicon glyphicon-chevron-right'></span></font></div></td></tr></table></td></tr></table></div></div></td><td width='1%'></td></tr></table></a>"
	}
	output = output +"</div>";
	$("#resultsWid").empty();
	document.getElementById("resultsWid").innerHTML = output;
	document.getElementById("resultsWid").setAttribute("route",busList[0].full[0].route)
	document.getElementById("resultsWid").setAttribute("routeType","bus")
	$("#busBox").fadeIn();	
	$(".onlyBus").click(function() {
			var bookingLink = $(this).attr('bookingLink')
			var win = window.open(bookingLink, '_blank');
			win.focus();
	});
}

