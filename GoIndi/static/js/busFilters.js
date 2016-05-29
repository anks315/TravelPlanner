var busLeastDuration = 0;
var busLeastPrice = 0;
var maxPrice = 0;

var filterbusPrice;
var filterbusDuration;
var filterbusMinDeparture;
var filterbusMaxDeparture;
var filterbusMinArrival;
var filterbusMaxArrival;
var filterbusTypeList = new Object();

function busFilters(){
	
	var busTypeFilter = getCheckFilterWid(busList,"busTypeFilter","Bus Type","busType")
	
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='busAmount' class='filterLabel'>Price range:</label><div id='busAmount' class='filterValue'></div></p><div id='busPriceRange'></div><br/><p><label for='busTime' class='filterLabel'>Travel time range:</label><div id='busTime' class='filterValue'></div></p><div id='busDurationRange'></div><br/><p><label for='busDeparture' class='filterLabel'>Departure time range:</label><div id='busDeparture' class='filterValue'></div></p><div id='busDepartureTimeRange'></div><br/><p><label for='busArrival' class='filterLabel'>Arrival time range:</label><div id='busArrival' class='filterValue'></div></p><div id='busArrivalTimeRange'></div><br/>"+busTypeFilter+"<br/></div></div></div>"
	
	document.getElementById("busFilters").innerHTML = output;
	if($("#busDataHead").hasClass("active")){
		$("#busFilters").show();
	}
	busLeastPrice = busList[0].full[0].price.split(",")[0];
	busLeastDuration = busList[0].full[0].duration;
	var leastDurArr = busLeastDuration.split(":");
	busLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	maxPrice = busLeastPrice;
	var maxDuration = busLeastDuration;
	for (i = 1; i < busList.length; i++) { 
		var PriceList = busList[i].full[0].price.split(",");
		var firstPrice = PriceList[0];
		var lastPrice = PriceList[PriceList.length-2];
		var duration = busList[i].full[0].duration;
		var durArr = duration.split(":");
		duration = durArr[1]*1+durArr[0]*60;
		
		if((firstPrice*1) < (busLeastPrice*1)){
			busLeastPrice = firstPrice;
		}
		if((lastPrice*1) > (maxPrice*1)){
			maxPrice = lastPrice;
		}
		
		if((duration*1) < (busLeastDuration*1)){
			busLeastDuration = duration;
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
        document.getElementById("busDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterbusMinDeparture=ui.values[0];
		filterbusMaxDeparture=ui.values[1];
		busFilter();
      }
    });
	filterbusMinDeparture=0;
	filterbusMaxDeparture=1440;
    document.getElementById("busDeparture").innerHTML = "12:00 AM - 12:00 PM";
	
	$( "#busArrivalTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("busArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filterbusMinArrival=ui.values[0];
		filterbusMaxArrival=ui.values[1];
		busFilter();
      }
    });
	filterbusMinArrival=0;
	filterbusMaxArrival=1440;
    document.getElementById("busArrival").innerHTML = "12:00 AM - 12:00 PM";
	
	for (i = 0; i < busList.length; i++) {
			var busType = busList[i].full[0].busType;
			if(busType in filterbusTypeList){
			}else{
				filterbusTypeList[busType] = true;
			}
	}
	$('#busTypeFilter').on('change', 'input[type="checkbox"]', function () {
				filterbusTypeList=new Object();
                $('#busTypeFilter').find('input:checked').each(function () {
					filterbusTypeList[$(this).attr('rel')]="true"
                });
				busFilter();
            });
						
}
function busFilter(){
	var j=0;
	 newbusList = new Array();
		for (i = 0; i < busList.length; i++) { 
		busType = busList[i].full[0].busType;
		durationArr = busList[i].full[0].duration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		arrivalArr = busList[i].full[0].arrival.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		departureArr = busList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1]
		if((busList[i].full[0].price.split(",")[0] <=filterbusPrice)&&(durationVal <= filterbusDuration)&&(arrivalVal <= filterbusMaxArrival)&&(arrivalVal >= filterbusMinArrival)&&(departureVal <= filterbusMaxDeparture)&&(departureVal >= filterbusMinDeparture)&&(busType in filterbusTypeList)){
			newbusList[j]=busList[i];
			j++;
		}
		}
		showBusJourneyList(newbusList);
}
