function getModalForFlights(transportParts){
	colWidth = 12/transportParts.length;
	var output="<table width = '100%'><tr><td><div class='row-eq-height'>"
	for (var i = 0; i < transportParts.length;i++ ){
		
		var part = ""
		if(transportParts[i].mode == 'flight'){
			part=getFlightPart(transportParts[i])
		} else if(transportParts[i].mode == 'bus'){
			part=getBusPart(transportParts[i])
		}
		output = output+"<div class='col-sm-"+colWidth+" col-height col-middle'>"+part+"</div>"
		
	}
	output = output + "</div></td></tr></table>"
	return output;
}

function getFlightPart(flight){
	var details = ""
	var first = 1;
	for ( var j = 0; j < flight.subParts.length;j++ ){
			var transportDetails = flight.subParts[j];
			if(j==0){
				//source and details of begining station
				details = details + "<table width='100%' class='table table-bordered' style='color:grey' ><tr><td bgcolor='WhiteSmoke'><table width ='100%'><tr ><td style='text-align:left' width='33%' class = 'detailsCity'bgcolor='WhiteSmoke'>"+transportDetails.source+"</td><td style='text-align:center'width='33%' bgcolor='WhiteSmoke'><img src='/static/images/"+transportDetails.mode+".png'></td><td bgcolor='WhiteSmoke' style='text-align:right' width='33%' class = 'detailsCity'>"+transportDetails.destination+"</td></tr></table></td></tr><tr><td><table width='100%' style='color:grey'><tr><td><table width='100%'><tr><td width='20%' class = 'detailsCity'>"+transportDetails.source+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Dep : "+transportDetails.departure+"</td></tr></table></td></tr>";
			}

			var siteName = "";
			siteName = transportDetails.site;
			
			
			transportCarrier = "<img src='/static/images/"+transportDetails.carrierName+".png'></img><br/>";

			//details of the transportation mode
			details = details + "<tr><td><table width='100%'><td width='5%'><table><tr><td style='white-space: nowrap;'><img src='/static/images/"+transportDetails.mode+"2.png'>&nbsp;&nbsp;</td><td><div style='border-left:1px solid #808080;border-left-style:dotted;height:150px'></div></td><td style='white-space: nowrap;text-align:left;'>&nbsp;&nbsp;<b class='detailsMode'>"+transportCarrier+"</b><br/><div class='detailsPrice'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Price : </b>&#8377 "+transportDetails.price+"/-</div><div class='detailsDuration'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Duration : </b>"+transportDetails.duration+" hrs</div></td></tr></table></td><td width='95%' style='text-align:right'>"+siteName+"&nbsp;&nbsp;<button type='button' class='btn btn-success btn-arrow-right' id = 'hello'>Book</button>&nbsp;&nbsp;&nbsp;</td></tr></table></td></tr>";
			
			if(j==flight.subParts.length-1){
				//details of last station
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Arr : "+transportDetails.arrival+"</td></tr></table></td></tr></table></td></tr></table>";
			} else {
				//datails of intermediate station
				k=j+1;
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td><table><tr><td class = 'detailsTime'>  Arr : "+transportDetails.arrival+"</td></tr><tr><td class = 'detailsTime'>  Dep : "+transportDetails.departure+"</td></tr></table></td></tr></table></td></tr>"
			}
			
	
	}
	return details;
	
}
function getBusPart(bus){
	var details =  "<table width='100%' class='table table-bordered' style='color:grey' ><tr><td bgcolor='WhiteSmoke'><table width ='100%'><tr ><td style='text-align:left' width='33%' class = 'detailsCity'bgcolor='WhiteSmoke'>"+bus.source+"</td><td style='text-align:center'width='33%' bgcolor='WhiteSmoke'><img src='/static/images/"+bus.mode+".png'></td><td bgcolor='WhiteSmoke' style='text-align:right' width='33%' class = 'detailsCity'>"+bus.destination+"</td></tr></table></td></tr><tr><td><table width = '100%'><tr><th style ='text-allign:left'>Departure:</th><th style ='text-allign:center'></th><th style ='text-allign:right'>Arrival:</th></tr>"
	var first = 1;
	for ( var j = 0; j < bus.subParts.length;j++ ){
			var transportDetails = bus.subParts[j];
			details = details + "<tr><td style ='text-allign:left'><hr/>"+transportDetails.departure+"</td><td style ='text-allign:center'><hr/>"+transportDetails.carrierName+" ("+transportDetails.busType+")</td><td style ='text-allign:right'><hr/>"+transportDetails.arrival+"</td></tr>";
	
	}
	details = details+"</table></td></tr></table>";
	return details;
}