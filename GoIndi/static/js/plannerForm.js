var placeFrom = "EMPTY"
var placeTo = "EMPTY"
var IsFromChange = true
var IsToChange = true
var directionsService;
var directionsDisplay;
var flightRouteChecked=0;
var trainRouteChecked=0;
var busRouteChecked=0;
var persons = 1;
var flightClassSelected="";
var trainClassSelected="";
var flightList=new Array()
var flightDirect = 0
var flightBiggest = 0
var flightBigToNear = 0
var flightNearToBig = 0

function showPlanner(plannerContainer){
		var flightClass = "<div class='btn-group'><a class='btn btn-default dropdown-toggle'  data-toggle='dropdown' href='#'>"+flightClassSelected+"&nbsp<span class='caret'></span></a><ul class='dropdown-menu'><li><a href='#' value='economy' type='flightClass'>Economy&nbsp</a></li><li><a href='#' value='Business' type='flightClass'>Business&nbsp</a></li></ul></div>"
		var trainClass = "<div class='btn-group'><a class='btn btn-default dropdown-toggle'  data-toggle='dropdown' href='#'>"+trainClassSelected+"&nbsp<span class='caret'></span></a><ul class='dropdown-menu'><li><a href='#' value='SL' type='trainClass'>SL&nbsp</a></li><li><a href='#' value='3A' type='trainClass'>3A&nbsp</a></li><li><a href='#' value='3E' type='trainClass'>3E&nbsp</a></li><li><a href='#' value='2A' type='trainClass'>2A&nbsp</a></li><li><a href='#' value='1A' type='trainClass'>1A&nbsp</a></li><li><a href='#' value='FA' type='trainClass'>FA&nbsp</a></li><li><a href='#' value='CC' type='trainClass'>CC&nbsp</a></li></ul></div>"
		
		var out ="";
			 out = out + "<nav role='navigation' class='navbar navbar-default'><div class='navbar-header' style='padding-bottom: 15px;'><a class='navbar-brand' href='/'><img src='/static/images/logo-main.png' class='sameLine'></a><button type='button' data-target='#navbarCollapse' data-toggle='collapse' class='navbar-toggle'><span class='sr-only'>Toggle navigation</span><span class='icon-bar'></span><span class='icon-bar'></span><span class='icon-bar'></span></button></div></img><div id='navbarCollapse' class='collapse navbar-collapse'><ul class='nav navbar-nav navbar-center'><li><div style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' id='from' placeholder='From:' type='text' autofocus autocomplete='off' ng-focus='disableTap()'></div></li><li><div style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' id='to' placeholder='To:' type='text' autofocus autocomplete='off'></div></li><li><div id='departure' style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' type='text' id='departureBox' class='form-control' placeholder= 'Departure'/><div></li><li><table><tr><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><label class='mainLabel' >Persons</label></td><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><div class='input-group'><input type='number' id ='persons' value='"+persons+"' min='1' max='6' class='form-control' style='width:60px;'/></div></td></tr></table></li><li><table><tr><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><label class='mainLabel'>Flight Class</label></td><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'>"+flightClass+"</td></tr></table></li><li><table><tr><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><label class='mainLabel'>Train Class</label></td><td style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'>"+trainClass+"</td></tr></table></li><li><div style='padding-bottom: 15px;padding-left: 5px;padding-right: 1px;padding-top: 15px;text-align:right'><input type='submit' id='search' class='btn btn-info' value='Search'></div></li></ul></div></nav>";

		document.getElementById("planner").innerHTML = out;
		//setting min date as today
		$('#departureBox').datepicker({ minDate: 0, maxDate: "+1Y" });
		var dt= new Date();
		   var yyyy = dt.getFullYear().toString();
		   var mm = (dt.getMonth()+1).toString(); // getMonth() is zero-based
		   var dd  = dt.getDate().toString();
		   var min = yyyy +'-'+ (mm[1]?mm:"0"+mm[0]) +'-'+ (dd[1]?dd:"0"+dd[0]); // padding
		//$('#departureBox').prop('min',min);
		//$('#returnBox').prop('min',min);
		
		
		$(".dropdown-menu li a").click(function(){
			
			  var selText = $(this).text();
			  var value = $(this).attr('value');
			  var type = $(this).attr('type');
			  if(type=="flightClass"){
				  flightClassSelected = value;
			  } else if (type=="trainClass"){
				  trainClassSelected = value;
			  }
			  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
			
		});
		document.getElementById("persons").oninput = function () {
			if (this.value.length > 1) {
				this.value = this.value.slice(0,1); 
			}else if (this.value*1 > 6) {
				this.value = 6; 
			}
		}
		
		$( "#search" ).click(function() {
				var failure = "FALSE";
			    if(placeFrom == "EMPTY" || IsFromChange==false){
					document.getElementById("from").value="";
					$('#from').css('border-color', 'red');
					failure = "TRUE"
				}
				if(placeTo == "EMPTY" || IsToChange==false){
					document.getElementById("to").value="";
					$('#to').css('border-color', 'red');
					failure = "TRUE"
				}
				if(document.getElementById("departureBox").value == ""){
					document.getElementById("departureBox").value="";
					$('#departureBox').css('border-color', 'red');
					failure = "TRUE"
				}
				
				if(failure == "TRUE"){
					return;
				}
				var fromStation = document.getElementById('from').value.split(",")[0];
				var toStation = document.getElementById('to').value.split(",")[0];
				var depDateArr = document.getElementById('departureBox').value.split("/");
				var depDate = depDateArr[1]+"-"+depDateArr[0]+"-"+depDateArr[2];
					document.getElementById("routeMenuList").innerHTML=""
					
					 routeMap = new Object()
					 flightRouteList=new Array()
					 trainRouteList=new Array()
					 busRouteList=new Array()
					 flightList=new Array()
					 trainList=new Array()
					 busList=new Array()
					 flightDirect = 0
					 flightBiggest = 0
					 flightBigToNear = 0
					 flightNearToBig = 0
					 flightRouteAdded=new Object()
					 trainRouteAdded=new Object()
					 $("#summaryBox").show()
					document.getElementById("resultsWid").innerHTML = "";
				// change in documeent ready as well, if changed here
				makeAsyncCalls(fromStation,toStation,depDate,flightClassSelected,trainClassSelected,document.getElementById('persons').value)
				$("#mainPanel").show();
				showSummary();
				showSortMenuMain();
				$("#sortMenuMain").show();
				
				$("#map").show();
				initMap();
				calculateAndDisplayRoute(directionsService, directionsDisplay);
		});
   }
 function initAutocomplete() {
	 
	  var options = {
  types: ['(cities)'],
  componentRestrictions: {country: "ind"}
 };

  // Create the search box and link it to the UI element.
  var fromInput = document.getElementById('from');
  var autocompleteFrom = new google.maps.places.Autocomplete(fromInput,options);
      google.maps.event.addListener(autocompleteFrom, 'place_changed', function(){
          placeFrom = autocompleteFrom.getPlace();
		  if (!placeFrom.geometry) {
            IsFromChange = false;
          } else {
			  IsFromChange = true;
		  }
      })

  var toInput = document.getElementById('to');
  var autocompleteTo = new google.maps.places.Autocomplete(toInput,options);
      google.maps.event.addListener(autocompleteTo, 'place_changed', function(){
          placeTo = autocompleteTo.getPlace();
		  if (!placeTo.geometry) {
            IsToChange = false;
          } else {
			  IsToChange = true;
		  }
      });
	  
	 var app = angular.module('myApp', []);
		app.controller('MyCtrl', function($scope) {
		  $scope.disableTap = function(){
			container = document.getElementsByClassName('pac-container');
			// disable ionic data tab
			angular.element(container).attr('data-tap-disabled', 'true');
			// leave input field if google-address-entry is selected
			angular.element(container).on("click", function(){
				document.getElementById('from').blur();
			});
		  };
		})
		
} 

function initMap() {
  directionsService = new google.maps.DirectionsService;
  directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 7,
    center: {lat: 41.85, lng: -87.65}
  });
  directionsDisplay.setMap(map);
 

}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
  directionsService.route({
    origin: document.getElementById('from').value,
    destination: document.getElementById('to').value,
    travelMode: google.maps.TravelMode.DRIVING
  }, function(response, status) {
    if (status === google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}
 $(document).ready(function(){
	 
	$("#mainPanel").hide();
	var urlParams = getUrlVars();
	flightClassSelected=urlParams.flightClass;
	trainClassSelected = urlParams.trainClass;
	persons = urlParams.persons;
	showPlanner("planner");
	document.getElementById('from').value = urlParams.from.replace(/\%20/g, " ");
	document.getElementById('to').value = urlParams.to.replace(/\%20/g, " ");
	placeFrom = document.getElementById('from').value;
	placeTo = document.getElementById('to').value;
	document.getElementById('departureBox').value = urlParams.dep;
	var retDate=urlParams.ret;
	if(retDate!=""){
		document.getElementById('returnBox').value = urlParams.ret;
		$('#two-way').attr('checked',1);
		$('#two-way').attr('class','active');
		$('#one-way').removeAttr('checked',1);
		$('#one-way').removeAttr('class','active');
	}
	var fromStation = document.getElementById('from').value.split(",")[0];
	var toStation = document.getElementById('to').value.split(",")[0];
	var depDateArr = document.getElementById('departureBox').value.split("/");
	var depDate = depDateArr[1]+"-"+depDateArr[0]+"-"+depDateArr[2]
	//change in the search click as well if changed here
	makeAsyncCalls(fromStation,toStation,depDate,flightClassSelected,trainClassSelected,persons);
	initAutocomplete();
	showSortMenuMain();
	showSummary();
	$("#mainPanel").show();	
	//initMap();
	calculateAndDisplayRoute(directionsService, directionsDisplay);
});

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
    function(m,key,value) {
      vars[key] = value;
    });
    return vars;
  }
  
 function makeAsyncCalls(fromStation,toStation,depDate,flightClassSelected,trainClassSelected,persons) {

	 $.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/flight/direct?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate+"&flightClass="+flightClassSelected+"&trainClass="+trainClassSelected+"&adults="+persons, function(data, err) {

				  flightDirect = 1
				  if (err != "success") {
					  
				  } else {
					  var flightRouteTemp = data.flight
					  flightList = flightList.concat(flightRouteTemp)
				  
					  if(flightRouteTemp.length>0){

					  routeFilter(flightRouteTemp,"flight")
						setSummary(flightList,"flight","price")
					  }
					  flightFilters();
					  if(flightDirect == 1&&flightBiggest==1&&flightBigToNear==1&&flightNearToBig==1){
						setSummary(flightList,"flight","price")
												
					  }
					}
				});

	$.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/flight/biggest?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate+"&flightClass="+flightClassSelected+"&trainClass="+trainClassSelected+"&adults="+persons, function(data, err) {
				  flightBiggest = 1
				  if (err != "success") {
					  
				  } else {
					  var flightRouteTemp = data.flight
					  flightList = flightList.concat(flightRouteTemp)
				  
					  if(flightRouteTemp.length>0){

					  routeFilter(flightRouteTemp,"flight")
						setSummary(flightList,"flight","price")
					  }
					  flightFilters();
					  if(flightDirect == 1&&flightBiggest==1&&flightBigToNear==1&&flightNearToBig==1){
						setSummary(flightList,"flight","price")
												
					  }
					}
				});

	$.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/flight/bigtonear?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate+"&flightClass="+flightClassSelected+"&trainClass="+trainClassSelected+"&adults="+persons, function(data, err) {
				  flightBigToNear =1
				  if (err != "success") {
					  
				  } else {
					  var flightRouteTemp = data.flight
					  flightList = flightList.concat(flightRouteTemp)
				  
					  if(flightRouteTemp.length>0){

					  routeFilter(flightRouteTemp,"flight")
						setSummary(flightList,"flight","price")
					 
					  }
					  flightFilters();
					  if(flightDirect == 1&&flightBiggest==1&&flightBigToNear==1&&flightNearToBig==1){
						setSummary(flightList,"flight","price")
												
					  }
				  }
				});

	$.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/flight/neartobig?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate+"&flightClass="+flightClassSelected+"&trainClass="+trainClassSelected+"&adults="+persons, function(data, err) {

				  flightNearToBig=1
				  if (err != "success") {
					  flightList = []
				  } else {
					  var flightRouteTemp = data.flight
					  flightList = flightList.concat(flightRouteTemp)
				  
				  	
					  if(flightRouteTemp.length>0){

					  routeFilter(flightRouteTemp,"flight")
					  setSummary(flightList,"flight","price")
					
					  }
					  flightFilters();
					  if(flightDirect == 1&&flightBiggest==1&&flightBigToNear==1&&flightNearToBig==1){
						setSummary(flightList,"flight","price")
												
					  }
				  }
				});			
	$.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/train?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate+"&trainClass="+trainClassSelected+"&adults="+persons, function(data, err) {
					
				  if (err != "success") {
					  trainList=[]
				  } else {
					  trainList = data.train
				  }
				   setSummary(trainList,"train","price")
					 if(trainList!=0){ 
					 
					  routeFilter(trainList,"train")
						trainFilters();
					}
				  
				});
	
	 $.getJSON('https://q21sw0b7ai.execute-api.ap-southeast-1.amazonaws.com/dev/bus?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate+"&adults="+persons, function(data, err) {
				  if (err != "success") {
					  busList=[]
				  } else {
					  busList = data.bus
				  } setSummary(busList,"bus","price")
					if(busList.length!=0){
					  for(var t=0;t<busList.length;t++){
						  busList[t]["full"][0]["route"]=fromStation+",bus,"+toStation
					  }
					  
					  routeFilter(busList,"bus")
					
						busFilters();
					}
				  
				});
 }
