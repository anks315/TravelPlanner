var flightLeastDuration = 0;
var flightLeastPrice = 0;
var maxPrice = 0;
var flightRouteAdded=new Object()
var filterflightPrice;
var filterflightDuration;
var filterflightMinDeparture;

var filterflightMaxDeparture;
var filterflightMinArrival;
var filterflightMaxArrival;

function flightFilters(){
	var routeOptions =""
		for (var k =0;k<flightRouteList.length;k++){
			
			var route=flightRouteList[k]
			if(route in flightRouteAdded ){
				continue
			} else {
				flightRouteAdded[route]=1
			}
			var list = routeMap["flight"][route]
			SortListByPrice(list);
			minPrice = list[0].full[0].price;
			SortListByDuration(list);
			minDuration = list[0].full[0].duration;
			route = route.replace(/,/g , "");
			route = route.replace(/ /g , "");
			
			flightFilterList = routeMap["flight"][flightRouteList[k]];
			routeArr = flightRouteList[k].split(",")
			
			var routeContent = "<div class='routeLabel sameLine'>"+routeArr[0]+"</div>";
			for(var j =1;j<routeArr.length;j++){
				routeContent = routeContent + "<div class='sameLine'><img src='/static/images/"+routeArr[j]+"2.png'></img></div>"
				j++
				routeContent=routeContent+"<div class='routeLabel sameLine'>"+routeArr[j]+"</div>"
			}
			
			routeContent="<table width=100%><tr><td><div class='divContainer'>"+routeContent+"</div><table width='100%'><tr><td style='text-align:left'><span class='label label-success' >min price - &#8377 "+minPrice+"/-</span></td><td style='text-align:right'><span class='label label-default'>min dur - "+minDuration+" Hrs</span></td></tr></table></td><td width='5%'>&nbsp;<span class='glyphicon glyphicon-play'></span></td></tr></table>"
	
			
			
			var routeOption="<a href='#filter"+route+"' id='"+route+"' route='"+flightRouteList[k]+"' class='list-group-item list-group-item-warning flightRouteMenu'  data-toggle='collapse' data-parent='#RouteMenu' >"+routeContent+"</a><div  class='collapse '  id='filter"+route+"' route='"+flightRouteList[k]+"'></div>"
			
			var loading = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading...<br/></td></tr><tr><td><br/></td></tr></table></div>'
			
			$("#routeMenuList").append(routeOption);
			if (!($("#allDataHead").hasClass("active")||$("#flightDataHead").hasClass("active"))){
					 $(".flightRouteMenu").hide()
				}
			$("#filter"+route).on('shown.bs.collapse', function () {
					$("#summaryBox").hide()
					document.getElementById("resultsWid").innerHTML = loading;
					visibleList = routeMap["flight"][$(this).attr('route')]
					createFlightFilter(visibleList)
			});

			$("#filter"+route).on('hidden.bs.collapse', function () {
					newVisibleList = new Array();
					document.getElementById("resultsWid").setAttribute("route","")
					document.getElementById("resultsWid").innerHTML = "";
					$("#summaryBox").show()
			});
			
		}
}
function createFlightFilter(flightFilterList){
			
			var route=flightFilterList[0]["full"][0]["route"]
			route = route.replace(/,/g , "");
			route = route.replace(/ /g , "");
			
			var filtersForOption = "<table width='100%'><tr><td width='5%'></td><td><p><label for='"+route+"flightAmount' class='filterLabel'>Price range:</label><div id='"+route+"flightAmount' class='filterValue'></div></p><div id='"+route+"flightPriceRange'></div><br/><p><label for='"+route+"flightTime' class='filterLabel'>Travel time range:</label><div id='"+route+"flightTime' class='filterValue'></div></p><div id='"+route+"flightDurationRange'></div><br/><p><label for='"+route+"flightDeparture' class='filterLabel'>Departure time range:</label><div id='"+route+"flightDeparture' class='filterValue'></div></p><div id='"+route+"flightDepartureTimeRange'></div><br/><p><label for='"+route+"flightArrival' class='filterLabel'>Arrival time range:</label><div id='"+route+"flightArrival' class='filterValue'></div></p><div id='"+route+"flightArrivalTimeRange'></div><br/></td><td width='5%'></td></tr></table>"
			
			document.getElementById("filter"+route).innerHTML = filtersForOption
			
			var flightLeastPrice = flightFilterList[0].full[0].price;
			var flightLeastDuration = flightFilterList[0].full[0].duration;
			var leastDurArr = flightLeastDuration.split(":");
			var flightLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
			var flightMaxPrice = flightFilterList[0].full[0].price;
			var flightMaxDuration = flightFilterList[0].full[0].duration;
			var maxDurArr = flightMaxDuration.split(":");
			flightMaxDuration = maxDurArr[1]*1+maxDurArr[0]*60;
			for (i = 1; i < flightFilterList.length; i++) {
				var minPrice = flightFilterList[i].full[0].price;
				var maxPrice = flightFilterList[i].full[0].price;
				var minDuration = flightFilterList[i].full[0].duration;
				var durArr = minDuration.split(":");
				minDuration = durArr[1]*1+durArr[0]*60;
				var maxDuration = flightFilterList[i].full[0].duration;
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
			var priceOffset = flightMaxPrice*1-flightLeastPrice*1;
			$( "#"+route+"flightPriceRange" ).slider({
			  range: "min",
			  value: priceOffset,
			  min: 1,
			  max: priceOffset,
			  slide: function( event, ui ) {
				document.getElementById(route+"flightAmount").innerHTML = "&#8377; " + flightLeastPrice + " - &#8377; " + (flightLeastPrice*1+ui.value*1);
				
			  },
			  change: function( event, ui ) {
				filterflightPrice=flightLeastPrice*1+ui.value*1;
				flightFilter();
			  }
			});
			filterflightPrice=flightMaxPrice;
			document.getElementById(route+"flightAmount").innerHTML = "&#8377; " + flightLeastPrice +
			  " - &#8377; " + flightMaxPrice ;
			  
			var durationOffset = flightMaxDuration-flightLeastDuration;
			$( "#"+route+"flightDurationRange" ).slider({
			  range: "min",
			  value: durationOffset,
			  min: 1,
			  max: durationOffset,
			  slide: function( event, ui ) {
				document.getElementById(route+"flightTime").innerHTML = ((flightLeastDuration-(flightLeastDuration%60))/60)+":"+minutes((flightLeastDuration%60)/100)+ " hrs - " + (((flightLeastDuration*1+ui.value*1)-((flightLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((flightLeastDuration*1+ui.value*1)%60)/100) + " hrs";
			  },
			  change: function( event, ui ) {
				filterflightDuration=flightLeastDuration*1+ui.value*1;
				flightFilter();
			  }
			});
			filterflightDuration=flightMaxDuration
			document.getElementById(route+"flightTime").innerHTML = ((flightLeastDuration-(flightLeastDuration%60))/60)+":"+(flightLeastDuration%60)+" hrs - " + ((flightMaxDuration-(flightMaxDuration%60))/60) + ":" + minutes((flightMaxDuration%60)/100) + " hrs";
			
			$( "#"+route+"flightDepartureTimeRange" ).slider({
			  range: true,
			  values: [0,1440],
			  min: 0,
			  max: 1440,
			  slide: function( event, ui ) {
				document.getElementById(""+route+"flightDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
			  },
			  change: function( event, ui ) {
				filterflightMinDeparture=ui.values[0];
				filterflightMaxDeparture=ui.values[1];
				flightFilter();
			  }
			});
			filterflightMinDeparture=0;
			filterflightMaxDeparture=1440;
			document.getElementById(""+route+"flightDeparture").innerHTML = "12:00 AM - 12:00 PM";
			
			$( "#"+route+"flightArrivalTimeRange" ).slider({
			  range: true,
			  values: [0,1440],
			  min: 0,
			  max: 1440,
			  slide: function( event, ui ) {
				document.getElementById(route+"flightArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
			  },
			  change: function( event, ui ) {
				filterflightMinArrival=ui.values[0];
				filterflightMaxArrival=ui.values[1];
				flightFilter();
			  }
			});
			filterflightMinArrival=0;
			filterflightMaxArrival=1440;
			document.getElementById(route+"flightArrival").innerHTML = "12:00 AM - 12:00 PM";
			newVisibleList = flightFilterList
			showtransportJourneyList(flightFilterList,"flight");
}
function flightFilter(){
	var j=0;
		newVisibleList = new Array();
		for (i = 0; i < visibleList.length; i++) { 
		durationArr = visibleList[i].full[0].minDuration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		
		departureArr = visibleList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1];
		arrivalArr = visibleList[i].full[0].maxDeparture.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		if((visibleList[i].full[0].price <=filterflightPrice)&&(durationVal <= filterflightDuration)&&(arrivalVal >= filterflightMinArrival)&&(arrivalVal <= filterflightMaxArrival)&&(departureVal >= filterflightMinDeparture)&&(departureVal <= filterflightMaxDeparture)){
			newVisibleList[j]=visibleList[i];
			j++;
		}
		}
		showtransportJourneyList(newVisibleList,"flight");
}

