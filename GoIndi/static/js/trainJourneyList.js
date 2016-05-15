function showTrainJourneyList(transportList, mode){
	var output = "<br/><div id='trainBox' hidden>";
	for (i = 0; i < transportList.length; i++) { 
		var transportTotalDetails = transportList[i].full[0];
        var transportTotaljourney = "";
		var details = "";
		var first = 1;
		var journeyDividerContent = "";
		for (j = 0; j < transportList[i].parts.length;j++ ){
			var transportDetails = transportList[i].parts[j];
			if(j==0){
				//source and details of begining station
				details = details + "<table width='100%' style='color:grey'><tr><td><table width='100%'><tr><td width='20%' class = 'detailsCity'>"+transportDetails.source+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Dep : "+transportDetails.departure+"</td></tr></table></td></tr>";
			}
			if(first == 1 && transportDetails.mode == 'train'){

					transportTotaljourney = transportDetails.carrierName;
					first = 0;
			} else if (transportDetails.mode == 'train'){

					transportTotaljourney = transportTotaljourney + "&nbsp;&#8594;&nbsp" + transportDetails.carrierName;
			}
			var siteName = "";

			

			transportCarrier = transportDetails.carrierName;
			//details of the transportation mode
			details = details + "<tr><td><table width='100%'><tr><td width='5%'><table><tr><td style='white-space: nowrap;'><img src='/static/images/"+transportDetails.mode+"2.png'>&nbsp;&nbsp;</td><td><div style='border-left:1px solid #808080;border-left-style:dotted;height:150px'></div></td><td style='white-space: nowrap;text-align:left;'>&nbsp;&nbsp;<b class='detailsMode'>"+transportCarrier+"</b><br/><div class='detailsPrice'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Price : </b>&#8377 "+transportDetails.price+"/-</div><div class='detailsDuration'>&nbsp;&nbsp;&nbsp;<b class='detailsLabel'>Duration : </b>"+transportDetails.duration+" hrs</div></td></tr></table></td><td width='95%' style='text-align:right'>"+siteName+"&nbsp;&nbsp;<button type='button' class='btn btn-success btn-arrow-right' id = 'hello'>Book</button>&nbsp;&nbsp;&nbsp;</td></tr></table></td></tr>";
			
			if(j==transportList[i].parts.length-1){
				//details of last station
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsCity'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td class = 'detailsTime'>  Arr : "+transportDetails.arrival+"</td></tr></table></td></tr></table>";
			} else {
				//datails of intermediate station
				k=j+1;
				details = details + "<tr><td><table width='100%'><tr><td width='20%' class = 'detailsCity'>"+transportDetails.destination+"&nbsp;&nbsp;</td><td><table><tr><td class = 'detailsTime'>  Arr : "+transportDetails.arrival+"</td></tr><tr><td class = 'detailsTime'>  Dep : "+transportList[i].parts[j].departure+"</td></tr></table></td></tr></table></td></tr>"
			}
			
			//bar displaying journey division on the main widget
			var journeyDividerContent = journeyDividerContent + "<td style ='padding: 1px'><img src='/static/images/"+transportDetails.mode+"2.png'/></td>";
		}
			var travelSpecificWid = travelSpecificsWidget(transportTotalDetails.source,transportTotalDetails.destination,transportTotalDetails.arrival,transportTotalDetails.departure,transportTotalDetails.duration);
			
			var journeyDivider = "<br/><table class='table table-bordered' style ='text-align:center'><tbody><tr>"+journeyDividerContent+"</tr></tbody></table>"

				
				var numberOfChanges = transportList[i].parts.length-1
				if (numberOfChanges == 1){
					var numberOfChangesView = numberOfChanges + " Stop"
				} else if (numberOfChanges == 0) {
					var numberOfChangesView = "Direct"
				} else {
					var numberOfChangesView = numberOfChanges + " Stops"
				}
				output = output + "<div class='trainMain' id = 'main"+transportTotalDetails.id+"'><div class='panel panel-default'><div class='panel-body'><div class='row-eq-height'><table width = '100%'><tr><td style ='text-align:left'><font color = 'grey'><b>"+transportTotaljourney+"</b></font></td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-warning'  data-toggle='modal' data-target='#details"+transportTotalDetails.id+"'>Select</button></td></tr></table></div><div class='row-eq-height'>"+journeyDivider+"</div><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey'>"+numberOfChangesView+"<br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><h4 style='white-space: nowrap;'><font color='green'>&#8377 "+transportTotalDetails.price+"/-</font><h4></td></tr></table></div></div></div></div></div>";
				
				output = output + "<div class='modal fade' id='details"+transportTotalDetails.id+"' role='dialog'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'><button type='button' class='close' data-dismiss='modal'>&times;</button></div><div class='modal-body'>"+details+"</div><div class='modal-footer'><button type='button' class='btn btn-default' data-dismiss='modal'>Close</button></div></div></div></div>";
				
	}
	output = output + "</div>"
	 //binding data to trains tab
	    $("#trainData").empty();
		document.getElementById("trainData").innerHTML = output;
		$("#trainBox").fadeIn();
	
}