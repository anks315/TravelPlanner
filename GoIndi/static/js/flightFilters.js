var flightLeastDuration = 0;
var flightLeastPrice = 0;
var maxPrice = 0;

var filterflightPrice;
var filterflightDuration;
var filterflightMinDeparture;

var filterflightMaxDeparture;
var filterflightMinArrival;
var filterflightMaxArrival;

function flightFilters(){
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='flightAmount' class='filterLabel'>Price range:</label><div id='flightAmount' class='filterValue'></div></p><div id='flightPriceRange'></div><br/><p><label for='flightTime' class='filterLabel'>Travel time range:</label><div id='flightTime' class='filterValue'></div></p><div id='flightDurationRange'></div><br/><p><label for='flightDeparture' class='filterLabel'>Departure time range:</label><div id='flightDeparture' class='filterValue'></div></p><div id='flightDepartureTimeRange'></div><br/><p><label for='flightArrival' class='filterLabel'>Arrival time range:</label><div id='flightArrival' class='filterValue'></div></p><div id='flightArrivalTimeRange'></div><br/></div></div></div>"

	document.getElementById("flightFilters").innerHTML = output;
	if($("#flightDataHead").hasClass("active")){
		$("#flightFilters").show();
	}
	flightLeastPrice = flightList[0].full[0].price;
	flightLeastDuration = flightList[0].full[0].duration;
	var leastDurArr = flightLeastDuration.split(":");
	flightLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	maxPrice = flightLeastPrice;
	var maxDuration = flightLeastDuration;
	for (i = 1; i < flightList.length; i++) {
		var price = flightList[i].full[0].price;
		var duration = flightList[i].full[0].duration;
		var durArr = duration.split(":");
		duration = durArr[1]*1+durArr[0]*60;

		if((price*1) < (flightLeastPrice*1)){
			flightLeastPrice = price;
		}
		if((price*1) > (maxPrice*1)){
			maxPrice = price;
		}

		if((duration*1) < (flightLeastDuration*1)){
			flightLeastDuration = duration;
		}
		if((duration*1) > (maxDuration*1)){
			maxDuration = duration;
		}
	}	;
	var priceOffset = maxPrice-flightLeastPrice;
    $( "#flightPriceRange" ).slider({
      range: "min",
      value: priceOffset,
      min: 1,
      max: priceOffset,
      slide: function( event, ui ) {
        document.getElementById("flightAmount").innerHTML = "&#8377; " + flightLeastPrice + " - &#8377; " + (flightLeastPrice*1+ui.value*1);
		
      },
	  change: function( event, ui ) {
        filterflightPrice=flightLeastPrice*1+ui.value*1;
		flightFilter();
      }
    });
	filterflightPrice=maxPrice;
    document.getElementById("flightAmount").innerHTML = "&#8377; " + flightLeastPrice +
      " - &#8377; " + maxPrice ;
	  
	var durationOffset = maxDuration-flightLeastDuration;
	$( "#flightDurationRange" ).slider({
      range: "min",
      value: durationOffset,
      min: 1,
      max: durationOffset,
      slide: function( event, ui ) {
        document.getElementById("flightTime").innerHTML = ((flightLeastDuration-(flightLeastDuration%60))/60)+":"+minutes((flightLeastDuration%60)/100)+ " hrs - " + (((flightLeastDuration*1+ui.value*1)-((flightLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((flightLeastDuration*1+ui.value*1)%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filterflightDuration=flightLeastDuration*1+ui.value*1;
		flightFilter();
      }
    });
	filterflightDuration=maxDuration
    document.getElementById("flightTime").innerHTML = ((flightLeastDuration-(flightLeastDuration%60))/60)+":"+(flightLeastDuration%60)+" hrs - " + ((maxDuration-(maxDuration%60))/60) + ":" + minutes((maxDuration%60)/100) + " hrs";
	
	$( "#flightDepartureTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("flightDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterflightMinDeparture=ui.values[0];
		filterflightMaxDeparture=ui.values[1];
		flightFilter();
      }
    });
	filterflightMinDeparture=0;
	filterflightMaxDeparture=1440;
    document.getElementById("flightDeparture").innerHTML = "12:00 AM - 12:00 PM";
	
	$( "#flightArrivalTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("flightArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterflightMinArrival=ui.values[0];
		filterflightMaxArrival=ui.values[1];
		flightFilter();
      }
    });
	filterflightMinArrival=0;
	filterflightMaxArrival=1440;
    document.getElementById("flightArrival").innerHTML = "12:00 AM - 12:00 PM";
						
}
function flightFilter(){
	var j=0;
		var newflightList = new Array();
		for (i = 0; i < flightList.length; i++) { 
		durationArr = flightList[i].full[0].duration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		arrivalArr = flightList[i].full[0].arrival.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		departureArr = flightList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1]
		if((flightList[i].full[0].price <=filterflightPrice)&&(durationVal <= filterflightDuration)&&(arrivalVal <= filterflightMaxArrival)&&(arrivalVal >= filterflightMinArrival)&&(departureVal <= filterflightMaxDeparture)&&(departureVal >= filterflightMinDeparture)){
			newflightList[j]=flightList[i];
			j++;
		}
		}
		showtransportJourneyList(newflightList,"flight");
}
