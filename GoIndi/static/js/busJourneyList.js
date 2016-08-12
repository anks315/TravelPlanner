function showBusJourneyList(busList){
	if(busList.length==0){
		document.getElementById("resultsWid").innerHTML = ""
		return;
	}
	if($( "#priceSort" ).hasClass("active")){
		SortListByPrice(busList);
	} else if ($( "#durationSort" ).hasClass("active")){
		SortListByDuration(busList);
	}else if ($( "#arrivalSort" ).hasClass("active")){
		SortListByArrival(busList);
	}else if ($( "#departureSort" ).hasClass("active")){
		SortListByDeparture(busList);
	}
	
	var output = "<div id='busBox' hidden><table width='100%'><tr>";
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
		output = output + "<tr ><td>&nbsp;</td></tr><tr><td bgcolor='#dcdcdc'><table width='100%' class='shadowTable'><tr><td><div class='row-eq-height'><table width = '100%'><tr><td width = '75%' style ='text-align:left'><div class='carrierLabel'>&nbsp;&nbsp;"+busDetails.carrierName+"</td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-warning onlyBus' id = '"+busDetails.id+"'bookingLink='"+busDetails.bookingLink+"'>Book</button>&nbsp;&nbsp;</td></tr></table></div></td></tr><tr><td bgcolor='WhiteSmoke'><br/><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey' size='1'>"+busDetails.busType+"<br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><font color='grey' size='1'>"+startingFrom+"</font><h4 style='white-space: nowrap;'><font color='green'>&#8377 "+price+"/-</font></h4></td></tr></table></div></div></td></tr></table></td></tr>"
	}
	output = output +"</table></div>";
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

