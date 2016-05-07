var placeFrom = "EMPTY"
var placeTo = "EMPTY"
var IsFromChange = true
var IsToChange = true
var directionsService;
var directionsDisplay;

function showPlanner(plannerContainer){
		var out ="";
			 out = out + "<nav role='navigation' class='navbar navbar-default'><div class='navbar-header'><button type='button' data-target='#navbarCollapse' data-toggle='collapse' class='navbar-toggle'><span class='sr-only'>Toggle navigation</span><span class='icon-bar'></span><span class='icon-bar'></span><span class='icon-bar'></span></button></div><div id='navbarCollapse' class='collapse navbar-collapse'><ul class='nav navbar-nav navbar-center'><li><div style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' id='from' placeholder='From:' type='text' autofocus autocomplete='off' ng-focus='disableTap()'></div></li><li><div style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' id='to' placeholder='To:' type='text' autofocus autocomplete='off'></div></li><li><div id='departure' style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' type='text' id='departureBox' class='form-control' placeholder= 'Departure'/><div></li><li><div id='return' style='padding-bottom: 15px;padding-left: 2.5px;padding-right: 2.5px;padding-top: 15px;'><input class='form-control' type='text' id='returnBox' class='form-control' placeholder= 'Return'/></div></li><li><br/><label class='radio-inline'><input type='radio' checked class='active' id='one-way'>One-Way</label><label class='radio-inline'><input type='radio' id='two-way'>Return</label></li><li><div style='padding-bottom: 15px;padding-left: 5px;padding-right: 1px;padding-top: 15px;text-align:right'><input type='submit' id='search' class='btn btn-info' value='Search'></div></li></ul></div></nav>";

		document.getElementById("planner").innerHTML = out;
		//setting min date as today
		$('#departureBox').datepicker({ minDate: 0, maxDate: "+1Y" });
		$('#returnBox').datepicker({ minDate: 0, maxDate: "+1Y" });
		var dt= new Date();
		   var yyyy = dt.getFullYear().toString();
		   var mm = (dt.getMonth()+1).toString(); // getMonth() is zero-based
		   var dd  = dt.getDate().toString();
		   var min = yyyy +'-'+ (mm[1]?mm:"0"+mm[0]) +'-'+ (dd[1]?dd:"0"+dd[0]); // padding
		//$('#departureBox').prop('min',min);
		//$('#returnBox').prop('min',min);
		$("#return").hide();
		
		
		
		$( "#one-way" ).click(function() {
				$('#one-way').attr('checked',1);
				$('#one-way').attr('class','active');
				$('#two-way').removeAttr('checked',1);
				$('#two-way').removeAttr('class','active');
				$("#return").hide();
				
		});
		$( "#two-way" ).click(function() {
				$('#two-way').attr('checked',1);
				$('#two-way').attr('class','active');
				$('#one-way').removeAttr('checked',1);
				$('#one-way').removeAttr('class','active');
				$("#return").show();
				
		});
		$( "#search" ).click(function() {
				var failure = "FALSE";
			    if(placeFrom == "EMPTY" || IsFromChange==false){
					document.getElementById("from").value="";
					failure = "TRUE"
				}
				if(placeTo == "EMPTY" || IsToChange==false){
					document.getElementById("to").value="";
					failure = "TRUE"
				}
				if(document.getElementById("departureBox").value == ""){
					document.getElementById("departureBox").value="";
					failure = "TRUE"
				}
				if(document.getElementById("two-way").checked==true&&document.getElementById("returnBox").value == ""){
					document.getElementById("returnBox").value="";
					failure = "TRUE"
				}
				if(failure == "TRUE"){
					return;
				}
				var fromStation = document.getElementById('from').value.split(",")[0];
				var toStation = document.getElementById('to').value.split(",")[0];
				var depDateArr = document.getElementById('departureBox').value.split("/");
				var depDate = depDateArr[1]+"-"+depDateArr[0]+"-"+depDateArr[2]
				$.getJSON('train?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate+'', function(data, err) {
				  if (err != "success") {
				  } else {
					  trainList = data.train
					showtransportJourneyList(trainList,"train");
					trainFilters();
				  }
				});
				$.getJSON('flight?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate, function(data, err) {
				  if (err != "success") {
				  } else {
					  flightList = data.flight
					showtransportJourneyList(flightList,"flight");
					flightFilters();
				  }
				});
			$.getJSON('bus?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate, function(data, err) {
				  if (err != "success") {
				  } else {
					  busList = data.bus
					showBusJourneyList(busList);
					busFilters();
				  }
				});
				$("#mainPanel").show();
				showSummary();
				showSortMenuMain();
				$("#summary").show();
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
		  IsFromChange = true;
      })

  var toInput = document.getElementById('to');
  var autocompleteTo = new google.maps.places.Autocomplete(toInput,options);
      google.maps.event.addListener(autocompleteTo, 'place_changed', function(){
          placeTo = autocompleteTo.getPlace();
		  IsToChange = true;
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
		
		$("#from").keydown(function () {
            IsFromChange = false;
        });
		
	$("#to").keydown(function () {
            IsToChange = false;
        });
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
	$.getJSON('train?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate, function(data, err) {
					
				  if (err != "success") {
				  } else {
					  trainList = data.train
					showtransportJourneyList(trainList,"train");
					trainFilters();
				  }
				  
				});
	$.getJSON('flight?sourcecity='+fromStation+'&sourcestate=&destinationcity='+toStation+'&destinationstate=&journeyDate='+depDate, function(data, err) {
				  if (err != "success") {
				  } else {
					  flightList = data.flight
					showtransportJourneyList(flightList,"flight");
					flightFilters();
				  }
				});
	 $.getJSON('bus?source='+fromStation+'&destination='+toStation+'&journeyDate='+depDate, function(data, err) {
				  if (err != "success") {
				  } else {
					  busList = data.bus
					showBusJourneyList(busList);
					busFilters();
				  }
				});
	initAutocomplete();
	$("#mainPanel").show();
	showSummary();
	showSortMenuMain();
	$("#summary").show();
	$("#sortMenuMain").show();
	
	$("#map").show();
	initMap();
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