function getModalForFlights(transportParts, id){
	
	//transportParts[1] = {"id":""+transportParts[0].id+"1","source":"Delhi","destination":"bangalore","mode":"bus","subParts":[{"id":""+transportParts[0].id+"11","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"500","duration":"05:15","departure":"12:40","arrival":"17:50"},{"id":""+transportParts[0].id+"12","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"600","duration":"05:15","departure":"12:40","arrival":"17:50"}]};
	colWidth = 12/transportParts.length;
	
	var partOutput=""
	var price=0
	for (var i = 0; i < transportParts.length;i++ ){
		
		var part = ""
		if(transportParts[i].mode == 'flight'){
			price = price + transportParts[i].price*1
			part=getFlightPart(transportParts[i], id)
		} else if(transportParts[i].mode == 'bus'){
			part=getOtherPart(transportParts[i], id)
			var priceList = transportParts[i]['subParts'][0].price;
			var priceArr = priceList.split(",");
			var subprice = priceArr[0]
			price = price + subprice*1
		} else{
			part=getTrainOptionsPart(transportParts[i], id)

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
	var details =  "<table width='100%' class='table shadowTable' style='color:grey' ><tr><td valign='center' style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke'><img src='/static/images/"+flight.mode+"2.png'>&nbsp;&nbsp;"+flight.source+"&nbsp;&#8594;&nbsp"+flight.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' data-role='none' class='btn btn-success booking' id='book"+flight.id+"'>Book</button>&nbsp;&nbsp;</td></tr></table><table width='100%'><tr><td width=50%>"
	var first = 1;
	for ( var j = 0; j < flight.subParts.length;j++ ){
			var transportDetails = flight.subParts[j];
			if(flight.subParts.length==1){
				var journeyLineWidth = 250
			} else {
				var journeyLineWidth = 150
			}
			if(j==0){
				//source and details of begining station
				details = details + "<table width='100%' style='color:grey'><tr><td><table width='100%'><tr><td width='20%'><b>"+transportDetails.source+"&nbsp;&nbsp;</b></td><td class = 'detailsTime'>  Dep : "+getIn12HrFormat(flight.departure)+", "+flight.departureDay+"</td></tr></table></td></tr>";
			}

			var siteName = "";
			siteName = transportDetails.site;
			
			
			transportCarrier = "<img src='"+transportDetails.carrierName+"'></img><br/>";
			flightnumber = "<font color='grey'>"+transportDetails.flightNumber+"</font>"

			//details of the transportation mode
			details = details + "<tr><td><table width='100%'><td width='5%'><table><tr><td style='white-space: nowrap;'>&nbsp;&nbsp;&nbsp;&nbsp;</td><td><div class='journeyLine' style='height:"+journeyLineWidth+"px'></div></td><td style='white-space: nowrap;text-align:left;'>&nbsp;&nbsp;"+transportCarrier+"Flight:"+flightnumber+"</td></tr></table></td><td width='95%' style='text-align:right'></td></tr></table></td></tr>";
			
			if(j==flight.subParts.length-1){
				//details of last station
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'><b>"+transportDetails.destination+"&nbsp;&nbsp;</b></td><td class = 'detailsTime'>  Arr : "+getIn12HrFormat(flight.arrival)+", "+flight.arrivalDay+"</td></tr></table></td></tr></table>";
			} else {
				//datails of intermediate station
				k=j+1;
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'><b>"+transportDetails.destination+"&nbsp;&nbsp;</b></td><td><table><tr><td></td></tr></table></td></tr></table></td></tr></td>"
			}
			
	
	}
	var pricesWid = "<table class='table table-striped' style='text-align:left'>"
	var noOfOptions = flight.bookingOptions.length
	if(noOfOptions>4){
		noOfOptions=4
	}
	for(var z =0;z<noOfOptions;z++){
		var bookingOption = flight.bookingOptions[z];
		var isCheckedPrice = ''
		var agent = bookingOption.Agents
		if(z==0){
			isCheckedPrice='checked'
			//var agent = "<img src='"+bookingOption.AgentsImg+"'></img>"
		}
		
		pricesWid = pricesWid + "<tr><td><div class='agent'>"+agent+"</div></td></tr><tr><td>" +"<input type='radio' data-role='none' value = '"+bookingOption.Price+"' bookingLink='"+bookingOption.DeeplinkUrl+"' class = '"+id+"' name='radio"+flight.id+"' "+isCheckedPrice+">&nbsp;&nbsp;<div class = 'detailsPrice sameLine'>&#8377 "+bookingOption.Price+"/-</div></td></tr>"
	}
	pricesWid = pricesWid + "</table>";
	details=details+"<td width=50% style='text-align:center' >"+pricesWid+"</td></tr></table>";
	var length =  radionames.length
	radionames[length] = "radio"+flight.id
	return details;
	
}
function getOtherPart(other, id){
	var details =  "<table width='100%' class='table shadowTable' style='color:grey' ><tr><td style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke' valign='center'><img src='/static/images/"+other.mode+"2.png'>&nbsp;&nbsp;"+other.source+"&nbsp;&#8594;&nbsp"+other.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button'data-role='none' class='btn btn-success booking'id='book"+other.id+"''>Book</button>&nbsp;&nbsp;</td></tr></table><table width = '100%' style ='text-allign:left;color:grey'><tr><th ></th><th class='detailsLabel'>Departs</th><th class='detailsLabel'>Arrives</th><th>Price</th></tr>"
	var first = 1;
	for ( var j = 0; j < other.subParts.length;j++ ){
			var isChecked = '';
			if (j==0){
				 isChecked = 'checked';
			}
			var transportDetails = other.subParts[j];
			
			var priceList = transportDetails.price;
			var priceArr = priceList.split(",");
			var price = priceArr[0]
				details = details + "<tr><td colspan = '4'><hr/></td></tr><tr><td width='40%'>&nbsp;&nbsp;<input type='radio' data-role='none' class ='"+id+"' name='radio"+other.id+"' "+isChecked+" value = '"+price+"' bookingLink='"+transportDetails.bookingLink+"' carrierType='bus'>&nbsp;&nbsp;<font color = '#056273'>"+transportDetails.carrierName+"</font><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color = 'grey' size='1'>("+transportDetails.busType+")</font></td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.departure)+", "+transportDetails.departureDay+"</td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.arrival)+", "+transportDetails.arrivalDay+"</td><td class='detailsPrice'>&#8377 "+price+"/-</td></tr><tr><td colspan = '4' style='text-align:center' class='detailsDuration' bgcolor='#C5EFFD'>Waiting Time : "+transportDetails.waitingTime+" Hrs</td></tr>";
		
	}
	details = details+"</table>";
	var length =  radionames.length
	radionames[length] = "radio"+other.id
	return details;
}

function getTrainOptionsPart(train, id){
	var details =  "<table width='100%' class='table shadowTable' style='color:grey' ><tr><td style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke' valign='center'><img src='/static/images/"+train.mode+"2.png'>&nbsp;&nbsp;"+train.source+"&nbsp;&#8594;&nbsp"+train.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' data-role='none' class='btn btn-success booking'id='book"+train.id+"'>Book</button>&nbsp;&nbsp;</td></tr></table><table width = '100%' style ='text-allign:left;color:grey'><tr><th ></th><th class='detailsLabel'>Departs</th><th class='detailsLabel'>Arrives</th><th>Price</th></tr>"
	var first = 1;
	for ( var j = 0; j < train.subParts.length;j++ ){
			var isChecked = '';
			if (j==0){
				 isChecked = 'checked';
			}
			var transportDetails = train.subParts[j];
			
			var price = transportDetails.price;
			

				details = details + "<tr><td colspan = '4'><hr/></td></tr><tr><td width='40%'>&nbsp;&nbsp;<input type='radio'  data-role='none' class ='"+id+"' name='radio"+train.id+"' "+isChecked+" value = '"+price+"' bookingLink='http://irctc.co.in'  source='"+transportDetails.sourceStation+"' destination='"+transportDetails.destinationStation+"' trainNumber='"+transportDetails.trainNumber+"' trainClass='"+transportDetails.priceClass+"' availiablityCallId='availabilityCall"+train.id+"' availiablityId='availabilityData"+train.id+"' carrierType='train' loader = 'loader"+train.id+"'>&nbsp;&nbsp;<font color = '#056273'>"+transportDetails.carrierName+"</font><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color = 'grey' size='1'>("+transportDetails.trainNumber+")</font></td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.departure)+", "+transportDetails.departureDay+"<br/>"+transportDetails.sourceStation+"</td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.arrival)+", "+transportDetails.arrivalDay+"<br/>"+transportDetails.destinationStation+"</td><td class='detailsPrice'>&#8377 "+price+"/-</td></tr><tr><td colspan = '4' style='text-align:center' class='detailsDuration' bgcolor='#C5EFFD'>Waiting Time : "+transportDetails.waitingTime+" Hrs</td></tr>";
			
	}
	var transportDetails = train.subParts[0];
	details = details+"</table><br/><table class='table' style='width: auto;'><tr><td><div id='availability"+train.id+"' ><a href='#' class = 'availabilityCall' id='availabilityCall"+train.id+"' availiablityId='availabilityData"+train.id+"' source='"+transportDetails.sourceStation+"' destination='"+transportDetails.destinationStation+"' trainNumber='"+transportDetails.trainNumber+"' trainClass='"+transportDetails.priceClass+"' loader = 'loader"+train.id+"'class='availabilityFont'>Show Availability</a><div id='availabilityData"+train.id+"' class='availabilityFont availabilityColor'></div><div id='loader"+train.id+"' hidden>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></div></td></tr></table>";
	var length =  radionames.length
	radionames[length] = "radio"+train.id
	return details;
}