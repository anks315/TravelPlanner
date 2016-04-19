var placeFrom = "EMPTY"
var placeTo = "EMPTY"
var IsFromChange = false
var IsToChange = false
var directionsService;
var directionsDisplay;

function showPlanner(plannerContainer){
		var out ="";
			 out = out + "<div ng-app='myApp' ng-controller='myCtrl'><div class='panel panel-default'><div class='panel-body'><ul class='nav nav-tabs'><li role='presentation' id='one-way' class='active'><a href='#'>One-way trip</a></li><li role='presentation' id='two-way'><a href='#'>Return trip</a></li></ul><div class='row'><div class='col-sm-6 col-height col-middle'></br><div class='input-group'><input class='form-control' id='from' placeholder='From:' type='text' autofocus autocomplete='off' ng-focus='disableTap()'><span class='input-group-addon'><span class='glyphicon glyphicon-home'></span></span></div></div><div class='col-sm-6 col-height col-middle'></br><div class='input-group'><input class='form-control' id='to' placeholder='To:' type='text' autofocus autocomplete='off'><span class='input-group-addon'><span class='glyphicon glyphicon-home'></span></span></div></div></div><div class='row'><div class='col-sm-6 col-height col-middle'></br><div class='input-group' id='departure'><input class='form-control' type='text' id='departureBox' class='form-control' placeholder= 'Departure'/><span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span></div></div><div class='col-sm-6 col-height col-middle'></br><div class='input-group date' id='return'><input class='form-control' type='text' id='returnBox' class='form-control' placeholder= 'Return'/><span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span></div></div></div><div class='row'><div class='col-sm-6 col-height col-middle'></br><input type='submit' id='search' class='btn btn-info' value='Search..'></div><div class='col-sm-6 col-height col-middle'></div></div></div></div></div>";

		document.getElementById("planner").innerHTML = out;
		$('#departureBox').datepicker({ minDate: 0, maxDate: "+1Y" });
		$('#returnBox').datepicker({ minDate: 0, maxDate: "+1Y" });
		//setting min date as today
		var dt= new Date();
		   var yyyy = dt.getFullYear().toString();
		   var mm = (dt.getMonth()+1).toString(); // getMonth() is zero-based
		   var dd  = dt.getDate().toString();
		   var min = yyyy +'-'+ (mm[1]?mm:"0"+mm[0]) +'-'+ (dd[1]?dd:"0"+dd[0]); // padding
		//$('#departureBox').prop('min',min);
//$('#returnBox').prop('min',min);
		$("#return").hide();
		
		
		
		$( "#one-way" ).click(function() {
				$('#one-way').attr('class','active')
				$('#two-way').removeAttr('class','active')
				$("#return").hide();
				
		});
		$( "#two-way" ).click(function() {
				$('#two-way').attr('class','active')
				$('#one-way').removeAttr('class','active')
				$("#return").show();
				
		});
		$( "#search" ).click(function() {
				var failure = "FALSE";
			    if(placeFrom == "EMPTY" || IsFromChange==false){
					document.getElementById("from").value="From:";
					failure = "TRUE"
				}
				if(placeTo == "EMPTY" || IsToChange==false){
					document.getElementById("to").value="To:";
					failure = "TRUE"
				}
				var depDate = document.getElementById("departureBox").value;
				if(depDate == ""){
					document.getElementById("departureBox").value="";
					failure = "TRUE"
				}
				
				var retDate = document.getElementById("returnBox").value;
				if(document.getElementById("two-way").class=="active"&& retDate == ""){
					document.getElementById("returnBox").value="";
					failure = "TRUE"
				}
				if(failure == "TRUE"){
					return;
				}
				
				var fromLoc = document.getElementById("from").value;
				var toLoc = document.getElementById("to").value;
				
				window.location.href = "main?from="+fromLoc+"&to="+toLoc+"&dep="+depDate+"&ret="+retDate;
				
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
		  IsToChange = true
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



 $(document).ready(function(){
	 
	showPlanner("planner");
	initAutocomplete();
});