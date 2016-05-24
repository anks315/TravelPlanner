function getModalForFlights(transportParts, id){
	
	transportParts[1] = {"id":""+transportParts[0].id+"1","source":"Delhi","destination":"bangalore","mode":"bus","subParts":[{"id":""+transportParts[0].id+"11","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"500","duration":"05:15","departure":"12:40","arrival":"17:50"},{"id":""+transportParts[0].id+"12","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"600","duration":"05:15","departure":"12:40","arrival":"17:50"}]};
	colWidth = 12/transportParts.length;
	
	var partOutput=""
	var price=0
	for (var i = 0; i < transportParts.length;i++ ){
		
		var part = ""
		if(transportParts[i].mode == 'flight'){
			price = price + transportParts[i].price*1
			part=getFlightPart(transportParts[i], id)
		} else if(transportParts[i].mode == 'bus'){
			part=getBusPart(transportParts[i], id)
			price = price + transportParts[i]['subParts'][0].price*1
		}
		partOutput = partOutput+"<div class='col-sm-"+colWidth+" col-height col-middle nopadding'>"+part+"</div>"
		
	}
	var output ="<br/><table width = '100%' style='color:grey'><tr><td width='50%'><div class='journeyPriceLabel sameLine'>Journey Price&nbsp;&nbsp;</div><div class='journeyPrice sameLine'>  &#8377 <div id='totalPrice"+id+"' class='sameLine'>"+price+"</div>/-</div></td><td width='50%'></td></tr></table><br/><table width = '100%'><tr><td><div class='row-eq-height'>"+ partOutput + "</div></td></tr></table>"
	return output;
}
function getTotalPrice(id){
	var price = 0;
	$("input."+id+":radio").each(function() {
		if ($(this).prop('checked')){
			price = price + ($(this).val())*1
		}
	});
	document.getElementById("totalPrice"+id).innerHTML = price;
}
function getFlightPart(flight,id){
	var details =  "<table width='100%' class='table' style='color:grey' ><tr><td valign='center' style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke'><img src='/static/images/"+flight.mode+"2.png'>&nbsp;&nbsp;"+flight.source+"&nbsp;&#8594;&nbsp"+flight.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' class='btn btn-success'>Book</button>&nbsp;&nbsp;</td></tr></table><table width='100%'><tr><td width=50%>"
	var first = 1;
	for ( var j = 0; j < flight.subParts.length;j++ ){
			var transportDetails = flight.subParts[j];
			if(j==0){
				//source and details of begining station
				details = details + "<table width='100%' style='color:grey'><tr><td><table width='100%'><tr><td width='20%'>"+transportDetails.source+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Dep : "+getIn12HrFormat(transportDetails.departure)+"</td></tr></table></td></tr>";
			}

			var siteName = "";
			siteName = transportDetails.site;
			
			
			transportCarrier = "<img src='/static/images/"+transportDetails.carrierName+".png'></img><br/>";

			//details of the transportation mode
			details = details + "<tr><td><table width='100%'><td width='5%'><table><tr><td style='white-space: nowrap;'>&nbsp;&nbsp;&nbsp;&nbsp;</td><td><div style='border-left:1px solid #808080;border-left-style:dotted;height:150px'></div></td><td style='white-space: nowrap;text-align:left;'>&nbsp;&nbsp;<b class='detailsMode'>"+transportCarrier+"</b><div class='detailsDuration'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Duration : </b>"+transportDetails.duration+" hrs</div></td></tr></table></td><td width='95%' style='text-align:right'></td></tr></table></td></tr>";
			
			if(j==flight.subParts.length-1){
				//details of last station
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Arr : "+getIn12HrFormat(transportDetails.arrival)+"</td></tr></table></td></tr></table>";
			} else {
				//datails of intermediate station
				k=j+1;
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td><table><tr><td class = 'detailsTime'>  Arr : "+getIn12HrFormat(transportDetails.arrival)+"</td></tr><tr><td class = 'detailsTime'>  Dep : "+getIn12HrFormat(transportDetails.departure)+"</td></tr></table></td></tr></table></td></tr></td>"
			}
			
	
	}
	details=details+"<td width=50% style='text-align:center' ><input type='radio' value = '"+flight.price+"' class = '"+id+" ' name='radio"+flight.id+"' checked>&nbsp;&nbsp;<div class = 'detailsPrice sameLine'>&#8377 "+flight.price+"/-</div></tr></table>";
	return details;
	
}
function getBusPart(bus, id){
	var details =  "<table width='100%' class='table' style='color:grey' ><tr><td style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke' valign='center'><img src='/static/images/"+bus.mode+"2.png'>&nbsp;&nbsp;"+bus.source+"&nbsp;&#8594;&nbsp"+bus.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' class='btn btn-success'>Book</button>&nbsp;&nbsp;</td></tr></table><table width = '100%' style ='text-allign:left;color:grey'><tr><th ></th><th class='detailsLabel'>Departs</th><th class='detailsLabel'>Arrives</th><th>Price</th></tr>"
	var first = 1;
	for ( var j = 0; j < bus.subParts.length;j++ ){
			var isChecked = '';
			if (j==0){
				 isChecked = 'checked';
			}
			var transportDetails = bus.subParts[j];
			details = details + "<tr><td colspan = '4'><hr/></td></tr><tr><td >&nbsp;&nbsp;<input type='radio' class ='"+id+"' name='radio"+bus.id+"' "+isChecked+" value = '"+transportDetails.price+"'>&nbsp;&nbsp;<font color = '#056273'>"+transportDetails.carrierName+"</font><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color = 'grey' size='1'>("+transportDetails.busType+")</font></td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.departure)+"</td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.arrival)+"</td><td class='detailsPrice'>&#8377 "+transportDetails.price+"/-</td></tr>";
	
	}
	details = details+"</table>";
	var length =  radionames.length
	radionames[length] = "radio"+bus.id
	return details;
}