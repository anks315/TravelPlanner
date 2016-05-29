var trainLeastDuration = 0;
var trainLeastPrice = 0;
var maxPrice = 0;

var filterTrainPrice;
var filterTrainDuration;
var filterTrainMinDeparture;
var filterTrainMaxDeparture;
var filterTrainMinArrival;
var filterTrainMaxArrival;

function trainFilters(){
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='trainAmount' class='filterLabel'>Price range:</label><div id='trainAmount' class='filterValue'></div></p><div id='trainPriceRange'></div><br/><p><label for='trainTime' class='filterLabel'>Travel time range:</label><div id='trainTime' class='filterValue'></div></p><div id='trainDurationRange'></div><br/><p><label for='trainDeparture' class='filterLabel'>Departure time range:</label><div id='trainDeparture' class='filterValue'></div></p><div id='trainDepartureTimeRange'></div><br/><p><label for='trainArrival' class='filterLabel'>Arrival time range:</label><div id='trainArrival' class='filterValue'></div></p><div id='trainArrivalTimeRange'></div><br/></div></div></div>"
	
	document.getElementById("trainFilters").innerHTML = output;
	if($("#trainDataHead").hasClass("active")){
		$("#trainFilters").show();
	}
	trainLeastPrice = trainList[0].full[0].price;
	trainLeastDuration = trainList[0].full[0].duration;
	var leastDurArr = trainLeastDuration.split(":");
	trainLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	maxPrice = trainLeastPrice;
	var maxDuration = trainLeastDuration;
	for (i = 1; i < trainList.length; i++) { 
		var price = trainList[i].full[0].price;
		var duration = trainList[i].full[0].duration;
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
	var priceOffset = maxPrice-trainLeastPrice;
    $( "#trainPriceRange" ).slider({
      range: "min",
      value: priceOffset,
      min: 1,
      max: priceOffset,
      slide: function( event, ui ) {
        document.getElementById("trainAmount").innerHTML = "&#8377; " + trainLeastPrice + " - &#8377; " + (trainLeastPrice*1+ui.value*1);
		
      },
	  change: function( event, ui ) {
        filterTrainPrice=trainLeastPrice*1+ui.value*1;
		trainFilter();
      }
    });
	filterTrainPrice=maxPrice;
    document.getElementById("trainAmount").innerHTML = "&#8377; " + trainLeastPrice +
      " - &#8377; " + maxPrice ;
	  
	var durationOffset = maxDuration-trainLeastDuration;
	$( "#trainDurationRange" ).slider({
      range: "min",
      value: durationOffset,
      min: 1,
      max: durationOffset,
      slide: function( event, ui ) {
        document.getElementById("trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+minutes((trainLeastDuration%60)/100)+ " hrs - " + (((trainLeastDuration*1+ui.value*1)-((trainLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((trainLeastDuration*1+ui.value*1)%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filterTrainDuration=trainLeastDuration*1+ui.value*1;
		trainFilter();
      }
    });
	filterTrainDuration=maxDuration
    document.getElementById("trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+(trainLeastDuration%60)+" hrs - " + ((maxDuration-(maxDuration%60))/60) + ":" + minutes((maxDuration%60)/100) + " hrs";
	
	$( "#trainDepartureTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("trainDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterTrainMinDeparture=ui.values[0];
		filterTrainMaxDeparture=ui.values[1];
		trainFilter();
      }
    });
	filterTrainMinDeparture=0;
	filterTrainMaxDeparture=1440;
    document.getElementById("trainDeparture").innerHTML = "12:00 AM - 12:00 PM";
	
	$( "#trainArrivalTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("trainArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterTrainMinArrival=ui.values[0];
		filterTrainMaxArrival=ui.values[1];
		trainFilter();
      }
    });
	filterTrainMinArrival=0;
	filterTrainMaxArrival=1440;
    document.getElementById("trainArrival").innerHTML = "12:00 AM - 12:00 PM";
						
}
function trainFilter(){
	var j=0;
		 newtrainList = new Array();
		for (i = 0; i < trainList.length; i++) { 
		durationArr = trainList[i].full[0].duration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		arrivalArr = trainList[i].full[0].arrival.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		departureArr = trainList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1]
		if((trainList[i].full[0].price <=filterTrainPrice)&&(durationVal <= filterTrainDuration)&&(arrivalVal <= filterTrainMaxArrival)&&(arrivalVal >= filterTrainMinArrival)&&(departureVal <= filterTrainMaxDeparture)&&(departureVal >= filterTrainMinDeparture)){
			newtrainList[j]=trainList[i];
			j++;
		}
		}
		showtransportJourneyList(newtrainList,"train");
}
