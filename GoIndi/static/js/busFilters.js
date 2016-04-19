var busLeastDuration = 0;
var busLeastPrice = 0;
var maxPrice = 0;

var filterbusPrice;
var filterbusDuration;
var filterbusMinDeparture;
var filterbusMaxDeparture;
var filterbusMinArrival;
var filterbusMaxArrival;

function busFilters(){
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='busAmount'>Price range:</label><div id='busAmount' style='border:0; color:#f6931f; font-weight:bold;'></div></p><div id='busPriceRange'></div><br/><p><label for='busTime'>Travel time range:</label><div id='busTime' style='border:0; color:#f6931f; font-weight:bold;'></div></p><div id='busDurationRange'></div><br/><p><label for='busDeparture'>Departure time range:</label><div id='busDeparture' style='border:0; color:#f6931f; font-weight:bold;'></div></p><div id='busDepartureTimeRange'></div><br/><p><label for='busArrival'>Arrival time range:</label><div id='busArrival' style='border:0; color:#f6931f; font-weight:bold;'></div></p><div id='busArrivalTimeRange'></div><br/></div></div></div>"
	
	document.getElementById("busFilters").innerHTML = output;
	if($("#busDataHead").hasClass("active")){
		$("#busFilters").show();
	}
	busLeastPrice = busList[0].full[0].price;
	busLeastDuration = busList[0].full[0].duration;
	var leastDurArr = busLeastDuration.split(":");
	busLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	maxPrice = busLeastPrice;
	var maxDuration = busLeastDuration;
	for (i = 1; i < busList.length; i++) { 
		var price = busList[i].full[0].price;
		var duration = busList[i].full[0].duration;
		var durArr = duration.split(":");
		duration = durArr[1]*1+durArr[0]*60;
		
		if((price*1) < (trainLeastPrice*1)){
			trainLeastPrice = price;
		}
		if((price*1) > (maxPrice*1)){
			maxPrice = price;
		}
		
		if((duration*1) < (trainLeastDuration*1)){
			trainLeastDuration = duration;
		}
		if((duration*1) > (maxDuration*1)){
			maxDuration = duration;
		}
	}	;
	var priceOffset = maxPrice-busLeastPrice;
    $( "#busPriceRange" ).slider({
      range: "min",
      value: priceOffset,
      min: 1,
      max: priceOffset,
      slide: function( event, ui ) {
        document.getElementById("busAmount").innerHTML = "&#8377; " + busLeastPrice + " - &#8377; " + (busLeastPrice*1+ui.value*1);
		
      },
	  change: function( event, ui ) {
        filterbusPrice=busLeastPrice*1+ui.value*1;
		busFilter();
      }
    });
	filterbusPrice=maxPrice;
    document.getElementById("busAmount").innerHTML = "&#8377; " + busLeastPrice +
      " - &#8377; " + maxPrice ;
	  
	var durationOffset = maxDuration-busLeastDuration;
	$( "#busDurationRange" ).slider({
      range: "min",
      value: durationOffset,
      min: 1,
      max: durationOffset,
      slide: function( event, ui ) {
        document.getElementById("busTime").innerHTML = ((busLeastDuration-(busLeastDuration%60))/60)+":"+minutes((busLeastDuration%60)/100)+ " hrs - " + (((busLeastDuration*1+ui.value*1)-((busLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((busLeastDuration*1+ui.value*1)%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filterbusDuration=busLeastDuration*1+ui.value*1;
		busFilter();
      }
    });
	filterbusDuration=maxDuration
    document.getElementById("busTime").innerHTML = ((busLeastDuration-(busLeastDuration%60))/60)+":"+(busLeastDuration%60)+" hrs - " + ((maxDuration-(maxDuration%60))/60) + ":" + minutes((maxDuration%60)/100) + " hrs";
	
	$( "#busDepartureTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("busDeparture").innerHTML = ((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100)+ " hrs - " + (((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filterbusMinDeparture=ui.values[0];
		filterbusMaxDeparture=ui.values[1];
		busFilter();
      }
    });
	filterbusMinDeparture=0;
	filterbusMaxDeparture=1440;
    document.getElementById("busDeparture").innerHTML = "0:00 hrs - 24:00 hrs";
	
	$( "#busArrivalTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("busArrival").innerHTML = ((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100)+ " hrs - " + (((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filterbusMinArrival=ui.values[0];
		filterbusMaxArrival=ui.values[1];
		busFilter();
      }
    });
	filterbusMinArrival=0;
	filterbusMaxArrival=1440;
    document.getElementById("busArrival").innerHTML = "0:00 hrs - 24:00 hrs";
						
}
function busFilter(){
	var j=0;
		var newbusList = new Array();
		for (i = 0; i < busList.length; i++) { 
		durationArr = busList[i].full[0].duration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		arrivalArr = busList[i].full[0].arrival.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		departureArr = busList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1]
		if((busList[i].full[0].price <=filterbusPrice)&&(durationVal <= filterbusDuration)&&(arrivalVal <= filterbusMaxArrival)&&(arrivalVal >= filterbusMinArrival)&&(departureVal <= filterbusMaxDeparture)&&(departureVal >= filterbusMinDeparture)){
			newbusList[j]=busList[i];
			j++;
		}
		}
		showBusJourneyList(newbusList);
}
function minutes(num){
	if(num == 0) {
		return "00";
	}
	var str = num.toString();
	var newStr = str.split(".")[1];
	if(newStr.length==1){
		newStr=newStr+'0';
	}
	return newStr;
}