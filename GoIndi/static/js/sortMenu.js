function showSortMenuMain(){
	var sortMenuMain = "" + "<br/><div class='btn-group btn-group-justified' role='group' aria-label='...'><div class='btn-group' role='group'><button type='button' id='priceSort' class='btn btn-default'>Pocket Friendly</button></div><div class='btn-group' role='group'><button type='button' id = 'durationSort' class='btn btn-default'>Time is Money</button></div></div><br/>"
	
	var modeMenuMain = "" + "<ul class='nav nav-tabs'><li class='active' id ='busDataHead'><a data-toggle='tab'  href='#busData' >&nbsp;&nbsp<img src='/static/images/bus.png'/>&nbsp;&nbsp</a></li><li id ='trainDataHead'><a data-toggle='tab' href='#trainData'>&nbsp;&nbsp<img src='/static/images/train.png'/>&nbsp;&nbsp</a></li><li id ='flightDataHead'><a data-toggle='tab' href='#flightData'>&nbsp;&nbsp<img src='/static/images/flight.png'/>&nbsp;&nbsp</a></li></ul><div class='tab-content'><div class='tab-pane fade in active' id='busData'></div><div class='tab-pane fade' id='flightData'></div><div class='tab-pane fade' id='trainData' id='trainData'></div>"
	
	document.getElementById("sortMenuMain").innerHTML = sortMenuMain;
	document.getElementById("modeMenuMain").innerHTML = modeMenuMain;
	
	var loadingBus = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading best bus options<br/></td></tr><tr><td><br/><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span></td></tr></table></div>'
	document.getElementById("busData").innerHTML = loadingBus;
	
	var loadingTrain = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading best train options<br/></td></tr><tr><td><br/><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span></td></tr></table></div>'
	document.getElementById("trainData").innerHTML = loadingTrain;
	
	var loadingFlight = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Loading best flight options<br/></td></tr><tr><td><br/><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span></td></tr></table></div>'
	document.getElementById("flightData").innerHTML = loadingFlight;
	
	//showBusJourneyList(busList);
	//showtransportJourneyList(trainList,"train");
	//showtransportJourneyList(flightList,"flight");
	//trainFilters();
	//flightFilters();
	//busFilters();
	
	$( "#busDataHead" ).click(function() {
				$("#flightFilters").hide();
				$("#trainFilters").hide();
				$("#busFilters").show();
		});
	$( "#trainDataHead" ).click(function() {
				$("#flightFilters").hide();
				$("#busFilters").hide();
				$("#trainFilters").show();
		});
	$( "#flightDataHead" ).click(function() {
				$("#busFilters").hide();
				$("#trainFilters").hide();
				$("#flightFilters").show();
		});
		
	$( "#priceSort" ).click(function() {
				SortListByPrice(busList);
				showBusJourneyList(busList);
				SortListByPrice(trainList);
				showtransportJourneyList(trainList,"train");
				SortListByPrice(flightList);
				showtransportJourneyList(flightList,"flight");
				showSummary();
		});
	$( "#durationSort" ).click(function() {
				SortListByDuration(busList);
				showBusJourneyList(busList);
				SortListByDuration(trainList);
				showtransportJourneyList(trainList,"train");
				SortListByDuration(flightList);
				showtransportJourneyList(flightList,"flight");
				showSummary();
		});
		
	SortListByDuration
	
}