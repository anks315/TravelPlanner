var trainLeastDuration = 0;
var trainLeastPrice = 0;
var maxPrice = 0;
var trainRouteAdded=new Object()
var filtertrainPrice;
var filtertrainDuration;
var filtertrainMinDeparture;

var filtertrainMaxDeparture;
var filtertrainMinArrival;
var filtertrainMaxArrival;

function trainFilters(){
	var routeOptions =""
		for (var k =0;k<trainRouteList.length;k++){
			var route=trainRouteList[k]
			if(route in trainRouteAdded ){
				continue
			} else {
				trainRouteAdded[route]=1
			}
			var list = routeMap["train"][route]
			SortListByPrice(list);
			minPrice = list[0].full[0].price;
			SortListByDuration(list);
			minDuration = list[0].full[0].duration;
			route = route.replace(/,/g , "");
			route = route.replace(/ /g , "");
			
			trainFilterList = routeMap["train"][trainRouteList[k]];
			routeArr = trainRouteList[k].split(",")
			
			var routeContent = "<div class='routeLabel sameLine'>"+routeArr[0]+"</div>";
			for(var j =1;j<routeArr.length;j++){
				routeContent = routeContent + "<div class='sameLine'><img src='/static/images/"+routeArr[j]+"2.png'></img></div>"
				j++
				routeContent=routeContent+"<div class='routeLabel sameLine'>"+routeArr[j]+"</div>"
			}
			
			routeContent="<table width=100%><tr><td><div class='divContainer'>"+routeContent+"</div><table width='100%'><tr><td style='text-align:left'><span class='label label-success'>min price - &#8377 "+minPrice+"/-</span></td><td style='text-align:right'><span class='label label-default'>min dur - "+minDuration+" Hrs</span></td></tr></table></td><td width='5%'>&nbsp;<span class='glyphicon glyphicon-play'></span></td></tr></table>"
			
			
			var routeOption="<a href='#filter"+route+"' id='"+route+"' route='"+trainRouteList[k]+"' class='list-group-item list-group-item-success trainRouteMenu'  data-toggle='collapse' data-parent='#RouteMenu'>"+routeContent+"</a><div  class='collapse'  id='filter"+route+"' route='"+trainRouteList[k]+"'></div>"
			var loading = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading...<br/></td></tr><tr><td><br/></td></tr></table></div>'
			$("#routeMenuList").append(routeOption);
			if (!($("#allDataHead").hasClass("active")||$("#trainDataHead").hasClass("active"))){
					 $(".trainRouteMenu").hide()
				}
			$("#filter"+route).on('shown.bs.collapse', function () {
					$("#summaryBox").hide()
					document.getElementById("resultsWid").innerHTML = loading;
					visibleList = routeMap["train"][$(this).attr('route')]
					createtrainFilter(visibleList)
			});

			$("#filter"+route).on('hidden.bs.collapse', function () {
					newVisibleList = new Array();
					document.getElementById("resultsWid").setAttribute("route","")
					document.getElementById("resultsWid").innerHTML = "";
					$("#summaryBox").show()
			});
		}
}
function createtrainFilter(trainFilterList){
			
			var route=trainFilterList[0]["full"][0]["route"]
			route = route.replace(/,/g , "");
			route = route.replace(/ /g , "");
			
			var filtersForOption = "<table width='100%'><tr><td width='5%'></td><td><p><label for='"+route+"trainAmount' class='filterLabel'>Price range:</label><div id='"+route+"trainAmount' class='filterValue'></div></p><div id='"+route+"trainPriceRange'></div><br/><p><label for='"+route+"trainTime' class='filterLabel'>Travel time range:</label><div id='"+route+"trainTime' class='filterValue'></div></p><div id='"+route+"trainDurationRange'></div><br/><p><label for='"+route+"trainDeparture' class='filterLabel'>Departure time range:</label><div id='"+route+"trainDeparture' class='filterValue'></div></p><div id='"+route+"trainDepartureTimeRange'></div><br/><p><label for='"+route+"trainArrival' class='filterLabel'>Arrival time range:</label><div id='"+route+"trainArrival' class='filterValue'></div></p><div id='"+route+"trainArrivalTimeRange'></div><br/></td><td width='5%'></td></tr></table>"
			
			document.getElementById("filter"+route).innerHTML = filtersForOption
			
			var trainLeastPrice = trainFilterList[0].full[0].price;
			var trainLeastDuration = trainFilterList[0].full[0].duration;
			var leastDurArr = trainLeastDuration.split(":");
			var trainLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
			var trainMaxPrice = trainFilterList[0].full[0].price;
			var trainMaxDuration = trainFilterList[0].full[0].duration;
			var maxDurArr = trainMaxDuration.split(":");
			trainMaxDuration = maxDurArr[1]*1+maxDurArr[0]*60;
			for (i = 1; i < trainFilterList.length; i++) {
				var minPrice = trainFilterList[i].full[0].price;
				var maxPrice = trainFilterList[i].full[0].price;
				var minDuration = trainFilterList[i].full[0].duration;
				var durArr = minDuration.split(":");
				minDuration = durArr[1]*1+durArr[0]*60;
				var maxDuration = trainFilterList[i].full[0].duration;
				var durArr = maxDuration.split(":");
				maxDuration = durArr[1]*1+durArr[0]*60;

				if((minPrice*1) < (trainLeastPrice*1)){
					trainLeastPrice = minPrice;
				}
				if((maxPrice*1) > (trainMaxPrice*1)){
					trainMaxPrice = maxPrice;
				}

				if((minDuration*1) < (trainLeastDuration*1)){
					trainLeastDuration = minDuration;
				}
				if((maxDuration*1) > (trainMaxDuration*1)){
					trainMaxDuration = maxDuration;
				}
			}	;
			var priceOffset = trainMaxPrice*1-trainLeastPrice*1;
			$( "#"+route+"trainPriceRange" ).slider({
			  range: "min",
			  value: priceOffset,
			  min: 1,
			  max: priceOffset,
			  slide: function( event, ui ) {
				document.getElementById(route+"trainAmount").innerHTML = "&#8377; " + trainLeastPrice + " - &#8377; " + (trainLeastPrice*1+ui.value*1);
				
			  },
			  change: function( event, ui ) {
				filtertrainPrice=trainLeastPrice*1+ui.value*1;
				trainFilter();
			  }
			});
			filtertrainPrice=trainMaxPrice;
			document.getElementById(route+"trainAmount").innerHTML = "&#8377; " + trainLeastPrice +
			  " - &#8377; " + trainMaxPrice ;
			  
			var durationOffset = trainMaxDuration-trainLeastDuration;
			$( "#"+route+"trainDurationRange" ).slider({
			  range: "min",
			  value: durationOffset,
			  min: 1,
			  max: durationOffset,
			  slide: function( event, ui ) {
				document.getElementById(route+"trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+minutes((trainLeastDuration%60)/100)+ " hrs - " + (((trainLeastDuration*1+ui.value*1)-((trainLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((trainLeastDuration*1+ui.value*1)%60)/100) + " hrs";
			  },
			  change: function( event, ui ) {
				filtertrainDuration=trainLeastDuration*1+ui.value*1;
				trainFilter();
			  }
			});
			filtertrainDuration=trainMaxDuration
			document.getElementById(route+"trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+(trainLeastDuration%60)+" hrs - " + ((trainMaxDuration-(trainMaxDuration%60))/60) + ":" + minutes((trainMaxDuration%60)/100) + " hrs";
			
			$( "#"+route+"trainDepartureTimeRange" ).slider({
			  range: true,
			  values: [0,1440],
			  min: 0,
			  max: 1440,
			  slide: function( event, ui ) {
				document.getElementById(""+route+"trainDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
			  },
			  change: function( event, ui ) {
				filtertrainMinDeparture=ui.values[0];
				filtertrainMaxDeparture=ui.values[1];
				trainFilter();
			  }
			});
			filtertrainMinDeparture=0;
			filtertrainMaxDeparture=1440;
			document.getElementById(""+route+"trainDeparture").innerHTML = "12:00 AM - 12:00 PM";
			
			$( "#"+route+"trainArrivalTimeRange" ).slider({
			  range: true,
			  values: [0,1440],
			  min: 0,
			  max: 1440,
			  slide: function( event, ui ) {
				document.getElementById(route+"trainArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
			  },
			  change: function( event, ui ) {
				filtertrainMinArrival=ui.values[0];
				filtertrainMaxArrival=ui.values[1];
				trainFilter();
			  }
			});
			filtertrainMinArrival=0;
			filtertrainMaxArrival=1440;
			document.getElementById(route+"trainArrival").innerHTML = "12:00 AM - 12:00 PM";
			newVisibleList = trainFilterList
			showtransportJourneyList(trainFilterList,"train");
}
function trainFilter(){
	var j=0;
		newVisibleList = new Array();
		for (i = 0; i < visibleList.length; i++) { 
		durationArr = visibleList[i].full[0].minDuration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		
		departureArr = visibleList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1];
		arrivalArr = visibleList[i].full[0].maxDeparture.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		if((visibleList[i].full[0].price <=filtertrainPrice)&&(durationVal <= filtertrainDuration)&&(arrivalVal >= filtertrainMinArrival)&&(arrivalVal <= filtertrainMaxArrival)&&(departureVal >= filtertrainMinDeparture)&&(departureVal <= filtertrainMaxDeparture)){
			newVisibleList[j]=visibleList[i];
			j++;
		}
		}
		showtransportJourneyList(newVisibleList,"train");
}
