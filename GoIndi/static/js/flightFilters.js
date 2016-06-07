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
	var routeOptions =""
		for (var i =0;i<flightRouteList.length;i++){
			var isChecked=''
			if (flightRouteChecked==i){
					 isChecked = 'checked';
				}
			routeOptions = routeOptions + "<input type='radio' class ='flightRoutes' name='flightRoutes' id='flight"+i+"' "+isChecked+" value = '"+flightRouteList[i]+"'>"
			routeArr = flightRouteList[i].split(",")
			routeLabel="<div class='routeLabel sameLine'>"+routeArr[0]+"</div>"
			for(var j =1;j<routeArr.length;j++){
				routeLabel = routeLabel + "&nbsp;&nbsp;<img class='sameLine' src='/static/images/"+routeArr[j]+"2.png'></img>&nbsp;&nbsp;"
				j++
				routeLabel=routeLabel+"<div class='routeLabel sameLine'>"+routeArr[j]+"</div>"
			}
			routeOptions = routeOptions + routeLabel+"</input><br/><span class='label label-success'>&#8377 "+routeMap["flight"][flightRouteList[i]][0]["full"][0]["price"]+"/-</span><br/>"
		}
	
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='routeOptions' class='filterLabel'>Route options:</label><div id='routeOptions' class='filterValue'>"+routeOptions+"</div></p><hr/><p><label for='flightAmount' class='filterLabel'>Price range:</label><div id='flightAmount' class='filterValue'></div></p><div id='flightPriceRange'></div><br/><p><label for='flightTime' class='filterLabel'>Travel time range:</label><div id='flightTime' class='filterValue'></div></p><div id='flightDurationRange'></div><br/><p><label for='flightDeparture' class='filterLabel'>Departure time range:</label><div id='flightDeparture' class='filterValue'></div></p><div id='flightDepartureTimeRange'></div><br/><p><label for='flightArrival' class='filterLabel'>Arrival time range:</label><div id='flightArrival' class='filterValue'></div></p><div id='flightArrivalTimeRange'></div><br/></div></div></div>"

	document.getElementById("flightFilters").innerHTML = output;
	if($("#flightDataHead").hasClass("active")){
		$("#flightFilters").show();
	}else{
		$("#flightFilters").hide();
	}
	flightLeastPrice = flightList[0].full[0].minPrice;
	flightLeastDuration = flightList[0].full[0].minDuration;
	var leastDurArr = flightLeastDuration.split(":");
	flightLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	flightMaxPrice = flightList[0].full[0].maxPrice;
	flightMaxDuration = flightList[0].full[0].maxDuration;
	var maxDurArr = flightMaxDuration.split(":");
	flightMaxDuration = maxDurArr[1]*1+maxDurArr[0]*60;
	for (i = 1; i < flightList.length; i++) {
		var minPrice = flightList[i].full[0].minPrice;
		var maxPrice = flightList[i].full[0].maxPrice;
		var minDuration = flightList[i].full[0].minDuration;
		var durArr = minDuration.split(":");
		minDuration = durArr[1]*1+durArr[0]*60;
		var maxDuration = flightList[i].full[0].maxDuration;
		var durArr = maxDuration.split(":");
		maxDuration = durArr[1]*1+durArr[0]*60;

		if((minPrice*1) < (flightLeastPrice*1)){
			flightLeastPrice = minPrice;
		}
		if((maxPrice*1) > (flightMaxPrice*1)){
			flightMaxPrice = maxPrice;
		}

		if((minDuration*1) < (flightLeastDuration*1)){
			flightLeastDuration = minDuration;
		}
		if((maxDuration*1) > (flightMaxDuration*1)){
			flightMaxDuration = maxDuration;
		}
	}	;
	var priceOffset = flightMaxPrice-flightLeastPrice;
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
	filterflightPrice=flightMaxPrice;
    document.getElementById("flightAmount").innerHTML = "&#8377; " + flightLeastPrice +
      " - &#8377; " + flightMaxPrice ;
	  
	var durationOffset = flightMaxDuration-flightLeastDuration;
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
	filterflightDuration=flightMaxDuration
    document.getElementById("flightTime").innerHTML = ((flightLeastDuration-(flightLeastDuration%60))/60)+":"+(flightLeastDuration%60)+" hrs - " + ((flightMaxDuration-(flightMaxDuration%60))/60) + ":" + minutes((flightMaxDuration%60)/100) + " hrs";
	
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
						
						
	$("input:radio[name='flightRoutes']").change(function(){
			var routeId = $(this).val();
			flightRouteChecked = $(this).attr('id').split("flight")[1]
			newflightList = []
			flightList = routeMap["flight"][routeId]
			newflightList = flightList
			showtransportJourneyList(flightList,"flight");
			flightFilters();
		});
}
function flightFilter(){
	var j=0;
		newflightList = new Array();
		for (i = 0; i < flightList.length; i++) { 
		durationArr = flightList[i].full[0].minDuration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		minArrivalArr = flightList[i].full[0].minArrival.split(":");
		minArrivalVal = minArrivalArr[0]*60 + 1*minArrivalArr[1];
		maxArrivalArr = flightList[i].full[0].maxArrival.split(":");
		maxArrivalVal = maxArrivalArr[0]*60 + 1*maxArrivalArr[1];
		minDepartureArr = flightList[i].full[0].minDeparture.split(":");
		minDepartureVal = minDepartureArr[0]*60 + 1*minDepartureArr[1];
		maxDepartureArr = flightList[i].full[0].maxDeparture.split(":");
		maxDepartureVal = maxDepartureArr[0]*60 + 1*maxDepartureArr[1];
		if((flightList[i].full[0].minPrice <=filterflightPrice)&&(durationVal <= filterflightDuration)&&(maxArrivalVal >= filterflightMinArrival)&&(minArrivalVal <= filterflightMaxArrival)&&(maxDepartureVal >= filterflightMinDeparture)&&(minDepartureVal <= filterflightMaxDeparture)){
			newflightList[j]=flightList[i];
			j++;
		}
		}
		showtransportJourneyList(newflightList,"flight");
}
