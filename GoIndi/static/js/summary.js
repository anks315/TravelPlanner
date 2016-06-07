

function showSummary(){
	
	
	 var output = "<div class='panel panel-default'><div class='panel-body'><br/><table width = '100%' style='text-align:center;'><tr><td valign='top' width = '5%'><div id = busSum></div></td><td width = '70%'><div id = busSumWid ></div></td><td valign='top'><div id = busSumPrice></div></td><td valign='top'><div id = busSumDur></div></td></tr><tr><td width = '5%' valign='top'><div id = trainSum></div></td><td width = '70%'><div id = trainSumWid ></div></td><td valign='top'><div id = trainSumPrice></div></td><td valign='top'><div id = trainSumDur></div></td></tr><tr><td width = '5%' valign='top'><div id = flightSum  ></div></td><td width = '70%'><div id = flightSumWid></div></td><td valign='top'><div id = flightSumPrice></div></td><td valign='top'><div id = flightSumDur></div></td></tr></table></div></div>";
	 
	 document.getElementById("summary").innerHTML = output;
	 var progressBar = "<div class='progress'><div class='progress-bar progress-bar-warning progress-bar-striped active' role='progressbar' aria-valuenow='45' aria-valuemin='0' aria-valuemax='100' style='width: 100%'><span class='sr-only'>100% Complete</span></div></div>"
	document.getElementById("busSumWid").innerHTML = progressBar;
	document.getElementById("trainSumWid").innerHTML = progressBar;
	document.getElementById("flightSumWid").innerHTML = progressBar;
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
	setSummaryDiv(currentPrice,mode);
	
}
function setNotApplicable(mode,basedOn){
	var output = "<table width='100%' style ='text-align:center' ><tr><td width='100%' style ='padding: 0px;' class = 'summaryNA'>&nbsp;<font color = 'white'>Not Available</font></td></tr></table><br/>";
	document.getElementById(""+mode+"SumWid").innerHTML = output
}
function resetSummary(mode,basedOn){

	if(basedOn=="duration"){
		if(mode=="flight"){
			setSummaryDiv(flightDurSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainDurSum,mode);
		}else{
			setSummaryDiv(busDurSum,mode);
		}
	} else {
		if(mode=="flight"){
			setSummaryDiv(flightPriceSum,mode);
		}else if(mode=="train") {
			setSummaryDiv(trainPriceSum,mode);
		}else{
			setSummaryDiv(busPriceSum,mode);
		}
	}
	
}

function setSummaryDiv(current,mode){
	if(mode=="bus"){
		var route = current.full[0].source + "," + current.full[0].mode + "," + current.full[0].destination
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
	var internals = "<td width='"+percent+"%' style ='padding: 0px;text-align:left' class = 'summaryBar'>&nbsp;<font color = 'white' style='white-space: nowrap;'>"+routeArr[0]+"</font></td>"
	for (var j = 1 ; j < routeLen; j++){
		
		internals = internals + "<td style ='padding: 0px' class = 'summaryBar'><img  src='/static/images/"+routeArr[j]+"3.png'></td>"
		j++;
		if(j!=routeLen-1){
			internals = internals + "<td style ='padding: 0px' class = 'summaryBar'><font color = 'white' style='white-space: nowrap;'>"+routeArr[j]+"</font</td>"
		} else {
			internals = internals + "<td width='"+percent+"%' style ='padding: 0px;text-align:right' class = 'summaryBar'><font color = 'white'>"+routeArr[j]+"</font>&nbsp;</td>"
		}
	}
	var output = "<table width='100%' style ='text-align:center' ><tr>"+internals+"</tr></table><br/>"
	document.getElementById(""+mode+"SumWid").innerHTML = output
	document.getElementById(""+mode+"SumPrice").innerHTML = "<b><font color='green'>&#8377 "+price+"/-</font></b>"
	document.getElementById(""+mode+"SumDur").innerHTML = "<b><font color='grey'>"+current.full[0].duration+" Hrs</font></b>"
}