function showSortMenuMain(){
	//var sortMenuMain = "" + "<div class='btn-group btn-group-justified ' role='group' aria-label='...'><div class='btn-group' role='group'><button type='button' id='priceSort' class='btn btn-info active' >Cheapest</button></div><div class='btn-group' role='group'><button type='button' id = 'durationSort' class='btn btn-info'>Fastest</button></div></div><br/>"
	
	var modeMenuMain = "" + "<ul class='nav nav-tabs'><li class='active' id ='allDataHead'><a data-toggle='tab'  href='#allData' >&nbsp;&nbspALL&nbsp;&nbsp</a><li id ='busDataHead'><a data-toggle='tab'  href='#busData' >&nbsp;&nbsp<img src='/static/images/bus.png'/>&nbsp;&nbsp</a></li><li id ='trainDataHead'><a data-toggle='tab' href='#trainData'>&nbsp;&nbsp<img src='/static/images/train.png'/>&nbsp;&nbsp</a></li><li id ='flightDataHead'><a data-toggle='tab' href='#flightData'>&nbsp;&nbsp<img src='/static/images/flight.png'/>&nbsp;&nbsp</a></li></ul><div class='tab-content'><div class='tab-pane fade in active' id='busData'></div><div class='tab-pane fade' id='flightData'></div><div class='tab-pane fade' id='trainData' id='trainData'></div>"
	
	document.getElementById("modeMenuMain").innerHTML = modeMenuMain;
	//document.getElementById("sortMenuMain").innerHTML = sortMenuMain;
	

	
	//showBusJourneyList(busList);
	//showtransportJourneyList(trainList,"train");
	//showtransportJourneyList(flightList,"flight");
	//trainFilters();
	//flightFilters();
	//busFilters();
	
	$( "#busDataHead" ).click(function() {
				
					
				$(".flightRouteMenu").hide();
				$(".trainRouteMenu").hide();
				$(".busRouteMenu").show();
				if(busRetrieved==1){
					$("#loading").hide();
				}else{
					$("#loading").show();
				}
		});
	$( "#trainDataHead" ).click(function() {
				
		
				$(".flightRouteMenu").hide();
				$(".busRouteMenu").hide();
				$(".trainRouteMenu").show();
				if(trainRetrieved==1){
					$("#loading").hide();
				}else{
					$("#loading").show();
				}
		});
	$( "#flightDataHead" ).click(function() {
				
				$(".busRouteMenu").hide();
				$(".trainRouteMenu").hide();
				$(".flightRouteMenu").show();
				if(flightRetrieved==1){
					$("#loading").hide();
				}else{
					$("#loading").show();
				}
		});
	$( "#allDataHead" ).click(function() {
				
				$(".busRouteMenu").show();
				$(".trainRouteMenu").show();
				$(".flightRouteMenu").show();
				if(flightRetrieved==1 && trainRetrieved==1 && busRetrieved==1){
					$("#loading").hide();
				}else{
					$("#loading").show();
				}
		});
		
	$( "#priceSort" ).click(function() {
				
				document.getElementById("durationSort").classList.remove("active");
				document.getElementById("priceSort").classList.add("active");
				var routeType = document.getElementById("resultsWid").getAttribute("routeType")
				if(routeType=="flight"){
					showtransportJourneyList(newVisibleList,"flight")
				}else if(routeType=="train"){
					showtransportJourneyList(newVisibleList,"train")
				}else if(routeType=="bus"){
					showBusJourneyList(newVisibleList)
				}
				
				
		});
	$( "#durationSort" ).click(function() {
				document.getElementById("durationSort").classList.add("active");
				document.getElementById("priceSort").classList.remove("active");
				var routeType = document.getElementById("resultsWid").getAttribute("routeType")
				if(routeType=="flight"){
					showtransportJourneyList(newVisibleList,"flight")
				}else if(routeType=="train"){
					showtransportJourneyList(newVisibleList,"train")
				}else if(routeType=="bus"){
					showBusJourneyList(newVisibleList)
				}
				
				
		});
		
	
}