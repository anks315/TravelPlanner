var trainLeastDuration = 0;
var trainLeastPrice = 0;
var maxPrice = 0;

var filtertrainPrice;
var filtertrainDuration;
var filtertrainMinDeparture;

var filtertrainMaxDeparture;
var filtertrainMinArrival;
var filtertrainMaxArrival;

function trainFilters(){
	var routeOptions =""
		for (var i =0;i<trainRouteList.length;i++){
			var isChecked=''
			if (trainRouteChecked==i){
					 isChecked = 'checked';
				}
			routeOptions = routeOptions + "<input type='radio' class ='trainRoutes' name='trainRoutes' id='train"+i+"' "+isChecked+" value = '"+trainRouteList[i]+"'>"
			routeArr = trainRouteList[i].split(",")
			routeLabel="<div class='journeyPriceLabel sameLine'>"+routeArr[0]+"</div>"
			for(var j =1;j<routeArr.length;j++){
				routeLabel = routeLabel + "&nbsp;&nbsp;<img class='sameLine' src='/static/images/"+routeArr[j]+"2.png'></img>&nbsp;&nbsp;"
				j++
				routeLabel=routeLabel+"<div class='journeyPriceLabel sameLine'>"+routeArr[j]+"</div>"
			}
			routeOptions = routeOptions + routeLabel+"</input><br/><span class='label label-success'>Rs 500/-</span><br/>"
		}
	
	var output = "<div class='panel panel-default'><div class='panel-body'><p><label for='routeOptions' class='filterLabel'>Route options:</label><div id='routeOptions' class='filterValue'>"+routeOptions+"</div></p><hr/><p><label for='trainAmount' class='filterLabel'>Price range:</label><div id='trainAmount' class='filterValue'></div></p><div id='trainPriceRange'></div><br/><p><label for='trainTime' class='filterLabel'>Travel time range:</label><div id='trainTime' class='filterValue'></div></p><div id='trainDurationRange'></div><br/><p><label for='trainDeparture' class='filterLabel'>Departure time range:</label><div id='trainDeparture' class='filterValue'></div></p><div id='trainDepartureTimeRange'></div><br/><p><label for='trainArrival' class='filterLabel'>Arrival time range:</label><div id='trainArrival' class='filterValue'></div></p><div id='trainArrivalTimeRange'></div><br/></div></div></div>"

	document.getElementById("trainFilters").innerHTML = output;
	if($("#trainDataHead").hasClass("active")){
		$("#trainFilters").show();
	}
	trainLeastPrice = trainList[0].full[0].minPrice;
	trainLeastDuration = trainList[0].full[0].minDuration;
	var leastDurArr = trainLeastDuration.split(":");
	trainLeastDuration = leastDurArr[1]*1+leastDurArr[0]*60;
	trainMaxPrice = trainList[0].full[0].maxPrice;
	trainMaxDuration = trainList[0].full[0].maxDuration;
	var maxDurArr = trainMaxDuration.split(":");
	trainMaxDuration = maxDurArr[1]*1+maxDurArr[0]*60;
	for (i = 1; i < trainList.length; i++) {
		var minPrice = trainList[i].full[0].minPrice;
		var maxPrice = trainList[i].full[0].maxPrice;
		var minDuration = trainList[i].full[0].minDuration;
		var durArr = minDuration.split(":");
		minDuration = durArr[1]*1+durArr[0]*60;
		var maxDuration = trainList[i].full[0].maxDuration;
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
	var priceOffset = trainMaxPrice-trainLeastPrice;
    $( "#trainPriceRange" ).slider({
      range: "min",
      value: priceOffset,
      min: 1,
      max: priceOffset,
      slide: function( event, ui ) {
        document.getElementById("trainAmount").innerHTML = "&#8377; " + trainLeastPrice + " - &#8377; " + (trainLeastPrice*1+ui.value*1);
		
      },
	  change: function( event, ui ) {
        filtertrainPrice=trainLeastPrice*1+ui.value*1;
		trainFilter();
      }
    });
	filtertrainPrice=trainMaxPrice;
    document.getElementById("trainAmount").innerHTML = "&#8377; " + trainLeastPrice +
      " - &#8377; " + trainMaxPrice ;
	  
	var durationOffset = trainMaxDuration-trainLeastDuration;
	$( "#trainDurationRange" ).slider({
      range: "min",
      value: durationOffset,
      min: 1,
      max: durationOffset,
      slide: function( event, ui ) {
        document.getElementById("trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+minutes((trainLeastDuration%60)/100)+ " hrs - " + (((trainLeastDuration*1+ui.value*1)-((trainLeastDuration*1+ui.value*1)%60))/60)+":"+minutes(((trainLeastDuration*1+ui.value*1)%60)/100) + " hrs";
      },
	  change: function( event, ui ) {
        filtertrainDuration=trainLeastDuration*1+ui.value*1;
		trainFilter();
      }
    });
	filtertrainDuration=trainMaxDuration
    document.getElementById("trainTime").innerHTML = ((trainLeastDuration-(trainLeastDuration%60))/60)+":"+(trainLeastDuration%60)+" hrs - " + ((trainMaxDuration-(trainMaxDuration%60))/60) + ":" + minutes((trainMaxDuration%60)/100) + " hrs";
	
	$( "#trainDepartureTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("trainDeparture").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filtertrainMinDeparture=ui.values[0];
		filtertrainMaxDeparture=ui.values[1];
		trainFilter();
      }
    });
	filtertrainMinDeparture=0;
	filtertrainMaxDeparture=1440;
    document.getElementById("trainDeparture").innerHTML = "12:00 AM - 12:00 PM";
	
	$( "#trainArrivalTimeRange" ).slider({
      range: true,
      values: [0,1440],
      min: 0,
      max: 1440,
      slide: function( event, ui ) {
        document.getElementById("trainArrival").innerHTML = getIn12HrFormat(((ui.values[0]-(ui.values[0]%60))/60)+":"+minutes((ui.values[0]%60)/100))+ " - " + getIn12HrFormat((((ui.values[1])-((ui.values[1])%60))/60)+":"+minutes(((ui.values[1])%60)/100));
      },
	  change: function( event, ui ) {
        filtertrainMinArrival=ui.values[0];
		filtertrainMaxArrival=ui.values[1];
		trainFilter();
      }
    });
	filtertrainMinArrival=0;
	filtertrainMaxArrival=1440;
    document.getElementById("trainArrival").innerHTML = "12:00 AM - 12:00 PM";
						
						
	$("input:radio[name='trainRoutes']").change(function(){
			var routeId = $(this).val();
			trainRouteChecked = $(this).attr('id').split("train")[1]
			newtrainList = []
			trainList = routeMap["train"][routeId]
			newtrainList = trainList
			showtransportJourneyList(trainList,"train");
			trainFilters();
		});
}
function trainFilter(){
	var j=0;
		newtrainList = new Array();
		for (i = 0; i < trainList.length; i++) { 
		durationArr = trainList[i].full[0].minDuration.split(":");
		durationVal = durationArr[0]*60 + 1*durationArr[1];
		minArrivalArr = trainList[i].full[0].minArrival.split(":");
		minArrivalVal = minArrivalArr[0]*60 + 1*minArrivalArr[1];
		maxArrivalArr = trainList[i].full[0].maxArrival.split(":");
		maxArrivalVal = maxArrivalArr[0]*60 + 1*maxArrivalArr[1];
		minDepartureArr = trainList[i].full[0].minDeparture.split(":");
		minDepartureVal = minDepartureArr[0]*60 + 1*minDepartureArr[1];
		maxDepartureArr = trainList[i].full[0].maxDeparture.split(":");
		maxDepartureVal = maxDepartureArr[0]*60 + 1*maxDepartureArr[1];
		if((trainList[i].full[0].minPrice <=filtertrainPrice)&&(durationVal <= filtertrainDuration)&&(maxArrivalVal >= filtertrainMinArrival)&&(minArrivalVal <= filtertrainMaxArrival)&&(maxDepartureVal >= filtertrainMinDeparture)&&(minDepartureVal <= filtertrainMaxDeparture)){
			newtrainList[j]=trainList[i];
			j++;
		}
		}
		showtransportJourneyList(newtrainList,"train");
}
