function showSummary(){
	
	
	 var output = "<div class='panel panel-default'><div class='panel-body'><table width = '100%' style='text-align:center;'><tr style='color:#056273;'><td width = '5%'></td><td width = '70%' style='text-align:left;'><h4><div id='sumHeading' class='sameLine'>Cheapest</div>&nbsp;Route Summary</h4></td><td><h4>Price</h4></td><td><h4>Duration</h4></td></tr><tr><td valign='top' width = '5%'><div id = busSum></div></td><td width = '70%'><div id = busSumWid ></div></td><td valign='top'><div id = busSumPrice></div></td><td valign='top'><div id = busSumDur></div></td></tr><tr><td width = '5%' valign='top'><div id = trainSum></div></td><td width = '70%'><div id = trainSumWid ></div></td><td valign='top'><div id = trainSumPrice></div></td><td valign='top'><div id = trainSumDur></div></td></tr><tr><td width = '5%' valign='top'><div id = flightSum  ></div></td><td width = '70%'><div id = flightSumWid></div></td><td valign='top'><div id = flightSumPrice></div></td><td valign='top'><div id = flightSumDur></div></td></tr></table></div></div>";
	 
	 document.getElementById("summary").innerHTML = output;
	 var progressBarWarning = "<div class='progress'><div class='progress-bar progress-bar-warning progress-bar-striped active' role='progressbar' aria-valuenow='45' aria-valuemin='0' aria-valuemax='100' style='width: 100%'><span class='sr-only'>100% Complete</span></div></div>"
	 var progressBarSuccess = "<div class='progress'><div class='progress-bar progress-bar-success progress-bar-striped active' role='progressbar' aria-valuenow='45' aria-valuemin='0' aria-valuemax='100' style='width: 100%'><span class='sr-only'>100% Complete</span></div></div>"
	 var progressBarDanger = "<div class='progress'><div class='progress-bar progress-bar-danger progress-bar-striped active' role='progressbar' aria-valuenow='45' aria-valuemin='0' aria-valuemax='100' style='width: 100%'><span class='sr-only'>100% Complete</span></div></div>"
	document.getElementById("busSumWid").innerHTML = progressBarDanger;
	document.getElementById("trainSumWid").innerHTML = progressBarSuccess;
	document.getElementById("flightSumWid").innerHTML = progressBarWarning;
	document.getElementById("busSum").innerHTML = "<img  src='/static/images/bus.png'>";
	document.getElementById("trainSum").innerHTML = "<img  src='/static/images/train.png'>";
	document.getElementById("flightSum").innerHTML = "<img  src='/static/images/flight.png'>";
	
}

function setSummary(list,mode,basedOn){
	if(list.length==0){
		setNotApplicable(mode,basedOn)
		return
	}
	SortListByPrice(list);
	var currentPrice =''
	if(mode=="flight"){
		flightPriceSum = list[0]
		currentPrice = flightPriceSum
	}else if(mode=="train") {
		trainPriceSum = list[0]
		currentPrice = trainPriceSum
	}else{
		busPriceSum = list[0]
		currentPrice = busPriceSum
	}
	var currentDur =''
	SortListByDuration(list);
	if(mode=="flight"){
		flightDurSum = list[0]
		currentDur = flightDurSum
	}else if(mode=="train") {
		trainDurSum = list[0]
		currentDur = trainDurSum
	}else{
		busDurSum = list[0]
		currentDur = busDurSum
	}
	SortListByDeparture(list);
	if(mode=="flight"){
		flightDepSum = list[0]
		currentDep = flightDepSum
	}else if(mode=="train") {
		trainDepSum = list[0]
		currentDep = trainDepSum
	}else{
		busDepSum = list[0]
		currentDep = busDepSum
	}
	SortListByArrival(list);
	if(mode=="flight"){
		flightArrSum = list[0]
		currentArr = flightArrSum
	}else if(mode=="train") {
		trainArrSum = list[0]
		currentArr = trainArrSum
	}else{
		busArrSum = list[0]
		currentArr = busArrSum
	}
	setSummaryDiv(currentPrice,mode);
	
}
function setNotApplicable(mode,basedOn){
	var output = "<table width='100%' style ='text-align:center' class='shadowTable'><tr><td width='100%' style ='padding: 0px;' class = 'summaryNA'>&nbsp;<font color = 'white'>Not Available</font></td></tr></table><br/>";
	document.getElementById(""+mode+"SumWid").innerHTML = output
}
function resetSummary(mode,basedOn){

	if(basedOn=="duration"){
		document.getElementById("sumHeading").innerHTML = "Fastest"
		if(mode=="flight"){
			setSummaryDiv(flightDurSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainDurSum,mode);
		}else{
			setSummaryDiv(busDurSum,mode);
		}
	} else if(basedOn=="price"){
		document.getElementById("sumHeading").innerHTML = "Cheapest"
		if(mode=="flight"){
			setSummaryDiv(flightPriceSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainPriceSum,mode);
		}else{
			setSummaryDiv(busPriceSum,mode);
		}
	}else if(basedOn=="arrival"){
		document.getElementById("sumHeading").innerHTML = "Earliest Arrival"
		if(mode=="flight"){
			setSummaryDiv(flightArrSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainArrSum,mode);
		}else{
			setSummaryDiv(busArrSum,mode);
		}
	}else if(basedOn=="departure"){
		document.getElementById("sumHeading").innerHTML = "Earliest Departure"
		if(mode=="flight"){
			setSummaryDiv(flightDepSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainDepSum,mode);
		}else{
			setSummaryDiv(busDepSum,mode);
		}
	}
	
}

function setSummaryDiv(current,mode){
	if(mode=="bus"){
		var route = busRouteList[0]
		var price = current.full[0].price.split(",")[0]
	} else {
		var route = current.full[0].route
		var price = current.full[0].price
	}
	var routeArr = route.split(",")
	var routeLen = routeArr.length;
	if(routeLen==7){
		var percent = 12
	} else if (routeLen==5){
		var percent = 17
	} else {
		var percent = 1
	}
	var internals = "<td width='"+percent+"%' style ='padding: 0px;text-align:left' class = 'summaryBar"+mode+"'>&nbsp;<font color = 'white' style='white-space: nowrap;'>"+routeArr[0]+"</font></td>"
	for (var j = 1 ; j < routeLen; j++){
		
		internals = internals + "<td style ='padding: 0px' class = 'summaryBar"+mode+"'><img  src='/static/images/"+routeArr[j]+"3.png'></td>"
		j++;
		if(j!=routeLen-1){
			internals = internals + "<td style ='padding: 0px' class = 'summaryBar"+mode+"'><font color = 'white' style='white-space: nowrap;'>"+routeArr[j]+"</font</td>"
		} else {
			internals = internals + "<td width='"+percent+"%' style ='padding: 0px;text-align:right' class = 'summaryBar"+mode+"'><font color = 'white' style='white-space: nowrap;'>"+routeArr[j]+"</font>&nbsp;</td>"
		}
	}
	route = route.replace(/,/g , "");
	route = route.replace(/ /g , "");
	var output = "<a href='#' class= 'summaryClick removedDeco' route='"+route+"'><table width='100%' style ='text-align:center' class='shadowTable' ><tr>"+internals+"</tr></table><br/></a>"
	document.getElementById(""+mode+"SumWid").innerHTML = output
	document.getElementById(""+mode+"SumPrice").innerHTML = "<b><font color='green'>&#8377 "+price+"/-</font></b>"
	document.getElementById(""+mode+"SumDur").innerHTML = "<b><font color='grey'>"+current.full[0].duration+" Hrs</font></b>"
	$(".summaryClick").click(function() {
			var route = $(this).attr('route')
			$("#"+route).trigger('click');
	});
}