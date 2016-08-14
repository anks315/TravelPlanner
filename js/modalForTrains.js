function getModalForTrains(transportParts, id){
	
	//transportParts[1] = {"id":""+transportParts[0].id+"1","source":"Delhi","destination":"bangalore","mode":"bus","subParts":[{"id":""+transportParts[0].id+"11","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"500","duration":"05:15","departure":"12:40","arrival":"17:50"},{"id":""+transportParts[0].id+"12","source":"Delhi","destination":"bangalore","carrierName":"srs travels","busType":"AC Sleeper","price":"600","duration":"05:15","departure":"12:40","arrival":"17:50"}]};
	colWidth = 12/transportParts.length;
	
	var partOutput=""
	var price=0
	for (var i = 0; i < transportParts.length;i++ ){
		
		var part = ""
		if(transportParts[i].mode == 'train'){
			price = price + transportParts[i].price*1
			part=getTrainPart(transportParts[i], id)
		} else if(transportParts[i].mode == 'bus'){
			part=getBusPart(transportParts[i], id)
			var priceList = transportParts[i]['subParts'][0].price;
			var priceArr = priceList.split(",");
			var subprice = priceArr[0]
			price = price + subprice*1
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
function changePrice(trainClass){
	var price = 0;
	$("."+trainClass+"").each(function() {
			price = price + ($(this).attr('price'))*1
	});
	inputId = "radio"+trainClass.split("trainClass")[1]
	var inputElement = document.getElementById(inputId)
	var className = inputElement.className
	inputElement.value = price
	getTotalPrice(className)
}
function getTrainPart(train,id){
	var details =  "<table width='100%' class='table' style='color:grey' ><tr><td valign='center' style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke'><img src='/static/images/"+train.mode+"2.png'>&nbsp;&nbsp;"+train.source+"&nbsp;&#8594;&nbsp"+train.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' class='btn btn-success bookingTrain'>Book</button>&nbsp;&nbsp;</td></tr></table><table width='100%'><tr><td width=50%>"
	var first = 1;
	for ( var j = 0; j < train.subParts.length;j++ ){
		if(train.subParts.length==1){
				var journeyLineWidth = 250
			} else {
				var journeyLineWidth = 150
			}
			var transportDetails = train.subParts[j];
			if(j==0){
				//source and details of begining station
				details = details + "<table width='100%' style='color:grey'><tr><td><table width='100%'><tr><td width='20%'>"+transportDetails.source+"("+transportDetails.sourceStation+")&nbsp;&nbsp;</td><td class = 'detailsTime'>  Dep : "+getIn12HrFormat(transportDetails.departure)+", "+transportDetails.departureDay+"</td></tr></table></td></tr>";
			}

			var siteName = "";
			siteName = transportDetails.site;
			
			
			transportCarrier = "<font color = '#056273'><b>"+transportDetails.carrierName+"</b></font><br/>";
			var classList = ''
			for (var prop in transportDetails.prices) {
				if(transportDetails.prices[prop]!=0){
					classList =classList+"<li><a href='#' price='"+transportDetails.prices[prop]+"' trainClassId='"+j+"trainClass"+train.id+"' availiablityCallId='"+j+"availabilityCall"+train.id+"' availiablityId='"+j+"availabilityData"+train.id+"' loader='loader"+j+train.id+"'>"+prop+"</a></li><li>"
				}
			}
			
			var classSelector = "<font color='grey'>Class: </font><div class='btn-group'><a class='btn dropdown-toggle trainModalClass'  data-toggle='dropdown' href='#'>"+transportDetails.priceClass+"<span class='caret'></span></a><ul class='dropdown-menu'>"+classList+"</ul></div><br/>"

			//details of the transportation mode
			details = details + "<tr><td><table width='100%'><td width='5%'><table><tr><td style='white-space: nowrap;'>&nbsp;&nbsp;&nbsp;&nbsp;</td><td><div class='journeyLine' style='height:"+journeyLineWidth+"px'></div></td><td style='white-space: nowrap;text-align:left;'>&nbsp;&nbsp;<b class='detailsMode'>"+transportCarrier+"</b><div class='detailsDuration'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Duration : </b>"+transportDetails.duration+" hrs</div></td></tr></table></td><td width='95%' style='text-align:right'>"+classSelector+"<div class = 'detailsPrice sameLine trainClass"+train.id+"' id='"+j+"trainClass"+train.id+"' price="+transportDetails.price+" trainClass='trainClass"+train.id+"'>&#8377 "+transportDetails.price+"/-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><br/><table class='table table-bordered shadowTable' style='width: auto;float:right;'><tr><td><div class=''id='"+j+"availability"+train.id+"' ><a href='#' class = 'availabilityCall' id='"+j+"availabilityCall"+train.id+"' availiablityId='"+j+"availabilityData"+train.id+"' source='"+transportDetails.sourceStation+"' destination='"+transportDetails.destinationStation+"' trainNumber='"+transportDetails.trainNumber+"' trainClass='"+transportDetails.priceClass+"' loader='loader"+j+train.id+"' class='availabilityFont'>Show Availability</a><div id='"+j+"availabilityData"+train.id+"' class='availabilityFont availabilityColor'></div></div><div id = 'loader"+j+train.id+"' hidden>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='glyphicon glyphicon-refresh glyphicon-refresh-animate' ></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></td></tr></table></td></tr></table></td></tr>";
			
			if(j==train.subParts.length-1){
				//details of last station
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"("+transportDetails.destinationStation+")&nbsp;&nbsp;</td><td class = 'detailsTime'>  Arr : "+getIn12HrFormat(transportDetails.arrival)+", "+transportDetails.arrivalDay+"</td></tr></table></td></tr></table>";
			} else {
				//datails of intermediate station
				k=j+1;
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsStation'>"+transportDetails.destination+"("+transportDetails.destinationStation+")&nbsp;&nbsp;</td><td><table><tr><td class = 'detailsTime'>  Arr : "+getIn12HrFormat(transportDetails.arrival)+", "+transportDetails.arrivalDay+"</td></tr><tr><td class = 'detailsTime'>  Waiting Time : "+transportDetails.waitingTime+" Hrs</td></tr><tr><td class = 'detailsTime'>  Dep : "+getIn12HrFormat(train.subParts[j+1].departure)+", "+train.subParts[j+1].departureDay+"</td></tr></table></td></tr></table></td></tr></td>"
			}
			
	
	}

	details=details+"<td width=10% style='text-align:center' ><input type='radio' value = '"+train.price+"' class = '"+id+"' name='radio"+train.id+"' id='radio"+train.id+"' checked hidden></input></tr></table>";
	return details;
	
}
function getBusPart(bus, id){
	var details =  "<table width='100%' class='table' style='color:grey' ><tr><td style='text-align:left' class = 'detailsCity'bgcolor='WhiteSmoke' valign='center'><img src='/static/images/"+bus.mode+"2.png'>&nbsp;&nbsp;"+bus.source+"&nbsp;&#8594;&nbsp"+bus.destination+"</td><td style='text-align:right;padding: 0px' bgcolor='WhiteSmoke'><button type='button' class='btn btn-success booking'id='book"+bus.id+"''>Book</button>&nbsp;&nbsp;</td></tr></table><table width = '100%' style ='text-allign:left;color:grey'><tr><th ></th><th class='detailsLabel'>Departs</th><th class='detailsLabel'>Arrives</th><th>Price</th></tr>"
	var first = 1;
	for ( var j = 0; j < bus.subParts.length;j++ ){
			var isChecked = '';
			if (j==0){
				 isChecked = 'checked';
			}
			var transportDetails = bus.subParts[j];
			
			var priceList = transportDetails.price;
			var priceArr = priceList.split(",");
			var price = priceArr[0]
			
			details = details + "<tr><td colspan = '4'><hr/></td></tr><tr><td width='40%'>&nbsp;&nbsp;<input type='radio' class ='"+id+"' name='radio"+bus.id+"' "+isChecked+" value = '"+price+"' bookingLink='"+transportDetails.bookingLink+"'>&nbsp;&nbsp;<font color = '#056273'>"+transportDetails.carrierName+"</font><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color = 'grey' size='1'>("+transportDetails.busType+")</font></td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.departure)+", "+transportDetails.departureDay+"</td><td class='detailsDuration'>"+getIn12HrFormat(transportDetails.arrival)+", "+transportDetails.arrivalDay+"</td><td class='detailsPrice'>&#8377 "+price+"/-</td></tr><tr><td bgcolor='#C5EFFD' colspan = '4' style='text-align:center' class='detailsDuration'>Waiting Time : "+transportDetails.waitingTime+" Hrs</td></tr>";
	
	}
	details = details+"</table>";
	var length =  radionames.length
	radionames[length] = "radio"+bus.id
	return details;
}