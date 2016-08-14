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
	
	var route=busRouteList[0]
	var list = routeMap["bus"][route]
	SortListByPrice(list);
	minPrice = list[0].full[0].price;
	SortListByDuration(list);
	minDuration = list[0].full[0].duration;
	route = route.replace(/,/g , "");
	route = route.replace(/ /g , "");
	
	busFilterList = routeMap["bus"][busRouteList[0]];
	routeArr = busRouteList[0].split(",")
	
	var routeContent = "<div class='routeLabel sameLine'>"+routeArr[0]+"</div>";
	for(var j =1;j<routeArr.length;j++){
		routeContent = routeContent + "<div class='sameLine'><img src='/static/images/"+routeArr[j]+"2.png'></img></div>"
		j++
		routeContent=routeContent+"<div class='routeLabel sameLine'>"+routeArr[j]+"</div>"
	}
	
	routeContent="<table width=100%><tr><td><div class='divContainer'>"+routeContent+"</div><table width='100%'><tr><td style='text-align:left'><span class='label label-success'>min price - &#8377 "+minPrice.split(',')[0]+"/-</span></td><td style='text-align:right'><span class='label label-default'>min dur - "+minDuration+" Hrs</span></td></tr></table></td><td width='5%'>&nbsp;<span class='glyphicon glyphicon-play'></span></td></tr></table>"

	
	var loading = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading...<br/></td></tr><tr><td><br/></td></tr></table></div>'
	var routeOption="<a href='#pagetwo' data-transition='slide' id='"+route+"' route='"+busRouteList[0]+"' class='list-group-item list-group-item-danger busRouteMenu' data-parent='#RouteMenu'>"+routeContent+"</a>"

	$("#routeMenuList").append(routeOption);
	if (!($("#allDataHead").hasClass("active")||$("#busDataHead").hasClass("active"))){
					 $(".busRouteMenu").hide()
				}
	
			$("#"+route).on('tap', function () {
					document.getElementById("resultsWid").innerHTML = loading;
					visibleList = routeMap["bus"][$(this).attr('route')]
					createbusFilter(visibleList)
			});

	filterbusTypeList=new Object()
	
						
}
function createbusFilter(busFilterList){
	var route=busFilterList[0]["full"][0]["route"]
			route = route.replace(/,/g , "");
			route = route.replace(/ /g , "");
	var filtersForOption = "<table width='100%'><tr><td width='5%'></td><td><p><label for='busAmount' class='filterLabel'>Price range:</label><div id='busAmount' class='filterValue'></div></p><div id='busPriceRange'></div><br/><p><label for='busTime' class='filterLabel'>Travel time range:</label><div id='busTime' class='filterValue'></div></p><div id='busDurationRange'></div><br/><p><label for='busDeparture' class='filterLabel'>Departure time range:</label><div id='busDeparture' class='filterValue'></div></p><div id='busDepartureTimeRange'></div><br/><p><label for='busArrival' class='filterLabel'>Arrival time range:</label><div id='busArrival' class='filterValue'></div></p><div id='busArrivalTimeRange'></div><br/></td><td width='5%'></td></tr><tr><td width='5%'></td><td colspan=2 style='color:grey;'><div id='busTypeFilter'><label for='busAmount' class='filterLabel'>Bus Type:</label><br/><input type='checkbox' data-role='none' value='A/C,Seater' checked>&nbsp;A/C-Seater<br/><input type='checkbox' data-role='none' value='A/C,Sleeper' checked>&nbsp;A/C-Sleeper<br/><input type='checkbox' data-role='none' value='Non,Seater' checked>&nbsp;Non A/C-Seater<br/><input type='checkbox' data-role='none' value='Non,Sleeper' checked>&nbsp;Non A/C-Sleeper</div></td></tr></table>"
	
	document.getElementById("selectedFilter").innerHTML = filtersForOption
		
	busLeastPrice = busFilterList[0].full[0].price.split(",")[0];
	busLeastDuration = busFilterList[0].full[0].duration;
	var leastDurArr = busLeastDuration.split(":");
	busLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	maxPrice = busLeastPrice;
	var maxDuration = busLeastDuration;
	for (i = 1; i < busFilterList.length; i++) { 
		var PriceList = busFilterList[i].full[0].price.split(",");
		var firstPrice = PriceList[0];
		var lastPrice = PriceList[PriceList.length-2];
		var duration = busFilterList[i].full[0].duration;
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
	$('#busTypeFilter').on('change', 'input[type="checkbox"]', function () {
				filterbusTypeList=new Object();
                $('#busTypeFilter').find('input:checkbox:not(:checked)').each(function () {
					filterbusTypeList[$(this).attr('value')]="true"
                });
				busFilter();
            })
	filterbusMinArrival=0;
	filterbusMaxArrival=1440;
    document.getElementById("busArrival").innerHTML = "12:00 AM - 12:00 PM";
	newVisibleList = busFilterList
	showBusJourneyList(busFilterList);
}
function busFilter(){
	var j=0;
	 newVisibleList = new Array();
		for (i = 0; i < visibleList.length; i++) { 
		busType = visibleList[i].full[0].busType;
		durationArr = visibleList[i].full[0].duration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		arrivalArr = visibleList[i].full[0].arrival.split(":");
		arrivalVal = arrivalArr[0]*60 + 1*arrivalArr[1];
		departureArr = visibleList[i].full[0].departure.split(":");
		departureVal = departureArr[0]*60 + 1*departureArr[1]
		if((visibleList[i].full[0].price.split(",")[0] <=filterbusPrice)&&(durationVal <= filterbusDuration)&&(arrivalVal <= filterbusMaxArrival)&&(arrivalVal >= filterbusMinArrival)&&(departureVal <= filterbusMaxDeparture)&&(departureVal >= filterbusMinDeparture)){
			 var skip=false
			for(key in filterbusTypeList){
				if(key == 'A/C,Sleeper' && busType.indexOf('A/C') != -1 && (busType.indexOf('Sleeper') != -1 ||
				busType.indexOf('sleeper') != -1) && busType.indexOf('Non') == -1){
					skip=true
				} else if(key == 'A/C,Seater' && busType.indexOf('A/C') != -1 && (busType.indexOf('Seater') != -1 ||
				busType.indexOf('seater') != -1 )&& busType.indexOf('Non') == -1){
					skip=true
				} else if(key == 'Non,Sleeper' && busType.indexOf('A/C') != -1 && (busType.indexOf('Sleeper') != -1 ||
				busType.indexOf('sleeper') != -1) && busType.indexOf('Non') != -1){
					skip=true
				} else if(key == 'Non,Sleater' && busType.indexOf('A/C') != -1 && (busType.indexOf('Seater') != -1 ||
				busType.indexOf('seater') != -1) && busType.indexOf('Non') == -1){
					skip=true
				}
			}
			if(skip == false){
				newVisibleList[j]=visibleList[i];
				j++;
			}
		}
		}
		showBusJourneyList(newVisibleList);
		//&&(busType in filterbusTypeList)
}
