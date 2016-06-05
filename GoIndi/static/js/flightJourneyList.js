var radionames = []
var isSelected =0
function showFlightJourneyList(transportList){
	if(flightList.length==0){
		
		var noData = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Sorry! We could not find any flights on this Route<br/>Check out Train or Bus for more options</td></tr><tr><td><br/></td></tr></table></div>'
		document.getElementById("flightData").innerHTML = noData;
		return;
	}
	var output = "<br/><div id='flightBox' hidden><table width='100%'><tr>";
	for (i = 0; i < transportList.length; i++) { 
		var transportTotalDetails = transportList[i].full[0];
        var transportTotaljourney = "";
		var journeyDividerContent = "";
		var individualJourneyDetails = "";
		var summary = "<br/>";
		var fontSize = 'h4'
		if(transportList[i].parts.length>1){
			fontSize = 'h5'
			summary="<table width = '100%'><tr><td style='text-align:left;padding: 5px;'><div class='journeyPriceSumLabel'>duration starts from</div><div class='journeyDuration sameLine'> <div class='sameLine'>"+transportTotalDetails.duration+" Hrs</div></div></td><td style='text-align:right;padding: 5px;'><div class='journeyPriceSumLabel'>price starts from</div><div class='journeyPrice sameLine'>  &#8377 <div class='sameLine'>"+transportTotalDetails.price+"</div>/-</div></td></tr></table>"
		}
		
		for (j = 0; j < transportList[i].parts.length;j++ ){
			var transportDetails = transportList[i].parts[j];
			

			if(transportDetails.mode == 'flight'){
				var first = 1;
				for(var q=0;q<transportDetails.subParts.length;q++){
					
					if(first==1 ){
						transportTotaljourney = transportTotaljourney + "<img height='40' width='70' src='"+transportDetails.subParts[q].carrierName+"'></img>"
						first = 0;
					} else if(transportDetails.subParts[q].carrierName!=transportDetails.subParts[q-1].carrierName){
						transportTotaljourney = transportTotaljourney + "&nbsp;&#8594;&nbsp" + "<img height='40' width='70' src='"+transportDetails.subParts[q].carrierName+"'></img>";
					}
				}
			}
			
			if(transportDetails.mode=='flight'){
				selectedClass = 'divisionFlightSelected';
				boxTypeClass = 'divisionFlightBox';
			}else{
				selectedClass = 'divisionOtherNotSelected';
				boxTypeClass = 'divisionOtherBox';
			}
			
			//bar displaying journey division on the main widget
			
			
				 
			var carrierClass = '';
			var colspan = '';
			var hiddenProperty = '';
			if(transportDetails.mode == "flight"){
				carrierClass = '';
				var numberOfChanges = transportDetails.subParts.length-1
				if (numberOfChanges == 1){
						var numberOfChangesView = numberOfChanges + " Stop"
				} else if (numberOfChanges == 0) {
						var numberOfChangesView = "Direct"
				} else {
						var numberOfChangesView = numberOfChanges + " Stops"
				}
				if(transportList[i].parts.length==2){
					colspan = 'width="90%"';
				}else if(transportList[i].parts.length==3){
					colspan = 'width="80%"';
				}
				hiddenProperty='';
			} else {
					carrierClass = '';
					numberOfChangesView = transportDetails.carrierName
			}
			
			journeyDividerContent = journeyDividerContent + "<td class='divisionEnabled' style ='padding: 0px' "+colspan+"'><a href='#' class='"+boxTypeClass+" "+selectedClass+" box"+i+"' id='"+transportDetails.id+"divBox' style ='padding: 1px'><img src='/static/images/"+transportDetails.mode+"3.png'/></a></td>";
			
			
			//details of journey
			if(transportDetails.mode == "flight"){
				
				
				var travelSpecificWid = travelSpecificsWidget(transportDetails.source,transportDetails.destination,transportDetails.arrival,transportDetails.departure,transportDetails.duration);
				
				individualJourneyDetails = individualJourneyDetails+"<div class='"+transportDetails.id+"divBox detailsBox"+i+"'> <table width='100%'><tr ><td ><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey'>"+numberOfChangesView+"<br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><"+fontSize+" style='white-space: nowrap;'><font color='green'>&#8377 "+transportDetails.price+"/-</font><"+fontSize+"></td></tr></table></div></div></tr></table></div>"
			
			}else if (transportDetails.mode == "bus"){
				individualJourneyDetails = individualJourneyDetails + "<div class='"+transportDetails.id+"divBox detailsBox"+i+"' hidden>"
				for(k=0;k<transportDetails.subParts.length;k++){
					var transportOptionDetails = transportDetails.subParts[k];
					
					
					var priceList = transportOptionDetails.price;
					var priceArr = priceList.split(",");
					var price = priceArr[0]
					
					var startingFrom='';
					if (priceArr.length>1){
							startingFrom="Staring from&nbsp;&nbsp;"
					}
					
					var travelSpecificWid = travelSpecificsWidget(transportDetails.source,transportDetails.destination,transportOptionDetails.arrival,transportOptionDetails.departure,transportOptionDetails.duration);
					
					individualJourneyDetails = individualJourneyDetails+"<table width='100%'><tr ><td ><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = '#056273'><b>"+transportOptionDetails.carrierName+"</b>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><font color='grey' size='1'>"+startingFrom+"</font><"+fontSize+" style='white-space: nowrap;'><font color='green'>&#8377 "+price+"/-</font><"+fontSize+"></td></tr></table></div></div></tr></table>"
					if (k!=(transportDetails.subParts.length-1)){
						individualJourneyDetails = individualJourneyDetails + '<hr/>'
					}
				}
				individualJourneyDetails = individualJourneyDetails + "</div>"
			}else {
				individualJourneyDetails = individualJourneyDetails + "<div class='"+transportDetails.id+"divBox detailsBox"+i+"' hidden>"
				for(k=0;k<transportDetails.subParts.length;k++){
					var transportOptionDetails = transportDetails.subParts[k];
					
					
					var price = transportOptionDetails.price;
					
					var travelSpecificWid = travelSpecificsWidget(transportDetails.source,transportDetails.destination,transportOptionDetails.arrival,transportOptionDetails.departure,transportOptionDetails.duration);
					
					individualJourneyDetails = individualJourneyDetails+"<table width='100%'><tr ><td ><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = '#056273'><b>"+transportOptionDetails.carrierName+"</b>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><"+fontSize+" style='white-space: nowrap;'><font color='green'>&#8377 "+price+"/-</font><"+fontSize+"></td></tr></table></div></div></tr></table>"
					if (k!=(transportDetails.subParts.length-1)){
						individualJourneyDetails = individualJourneyDetails + '<hr/>'
					}
				}
				individualJourneyDetails = individualJourneyDetails + "</div>"
			}
	
		}
			
				
				var journeyDivider = summary+"<table class='table table-bordered' style ='text-align:center' ><tbody><tr>"+journeyDividerContent+"</tr><tr><td colspan='"+transportList[i].parts.length+"'>"+individualJourneyDetails+"</td></tr></tbody></table>";
				
				output = output + "<div class='flightMain' id = 'main"+transportTotalDetails.id+"'><tr><td bgcolor='WhiteSmoke'><div class='row-eq-height'><table width = '100%'><tr><td style ='text-align:left'><font color = 'grey'><b>"+transportTotaljourney+"</b></font></td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-warning'  data-toggle='modal' data-target='#details"+transportTotalDetails.id+"'>Select</button>&nbsp;&nbsp;</td></tr></table></div></td></tr><tr><td><div class='row-eq-height'>"+journeyDivider+"</div>";
				
				output = output + "<div class='modal fade modal-wide' id='details"+transportTotalDetails.id+"' role='dialog'><div class='modal-dialog'><div class='modal-content'><div class='modal-body'>"+getModalForFlights(transportList[i].parts,transportTotalDetails.id)+"</div></div></div></div></td></tr></div>";
				
	}
	output = output + "</table></div>"
	//binding data to flights tab
		$("#flightData").empty();
		document.getElementById("flightData").innerHTML = output;
	for(var l=0; l<radionames.length;l++){
		$("input:radio[name='"+radionames[l]+"']").change(function(){
			var id = $(this).attr('class');
			getTotalPrice(id);
		});
	}
		$("#flightBox").fadeIn();
		//setting action on mode menu box
		$(".divisionFlightBox").mouseover(function() {
					if($(this).hasClass("divisionFlightSelected")){
						isSelected=1;
					}else{
						isSelected=0;
					}
					$(this).removeClass('divisionFlightNotSelected');
					$(this).addClass('divisionFlightHover');
				}).mouseout(function() { 
				$(this).removeClass('divisionFlightHover');
				if(isSelected){
					$(this).addClass('divisionFlightSelected');
				} else {
					$(this).addClass('divisionFlightNotSelected');
				}
					
				});
		$(".divisionFlightBox").click(function() {
			var classList = $(this).attr('class').split(/\s+/);
			var selectedWid = '';
				for (var i = 0; i < classList.length; i++) {
					if (classList[i].substring(0, 3)=='box') {
						selectedWid = classList[i]
					}
				}
			var len = selectedWid.length;
			var num = selectedWid.substring(3, len);
			var classToBeHidden = 'detailsBox'+num;
			var id = $(this).attr('id');
			$("."+classToBeHidden).hide();
			$("."+id).fadeIn();
			$("."+selectedWid).each(function() {
				if($(this).hasClass("divisionOtherSelected")){
						$(this).removeClass('divisionOtherSelected');
						$(this).addClass('divisionOtherNotSelected');
					}else if($(this).hasClass("divisionFlightSelected")){
						$(this).removeClass('divisionFlightSelected');
						$(this).addClass('divisionFlightNotSelected');
					}
			});
			isSelected=1;
			event.preventDefault();
		});
		$(".divisionOtherBox").mouseover(function() {
					if($(this).hasClass("divisionOtherSelected")){
						isSelected=1;
					}else{
						isSelected=0;
					}
					$(this).removeClass('divisionOtherNotSelected');
					$(this).addClass('divisionOtherHover');
				}).mouseout(function() { 
				$(this).removeClass('divisionOtherHover');
				if(isSelected){
					$(this).addClass('divisionOtherSelected');
				} else {
					$(this).addClass('divisionOtherNotSelected');
				}
					
				});
		$(".divisionOtherBox").click(function() {
			var classList = $(this).attr('class').split(/\s+/);
			var selectedWid = '';
				for (var i = 0; i < classList.length; i++) {
					if (classList[i].substring(0, 3)=='box') {
						selectedWid = classList[i]
					}
				}
			var len = selectedWid.length;
			var num = selectedWid.substring(3, len);
			var classToBeHidden = 'detailsBox'+num;
			var id = $(this).attr('id');
			$("."+classToBeHidden).hide();
			$("."+id).fadeIn();
			$("."+selectedWid).each(function() {
				if($(this).hasClass("divisionOtherSelected")){
						$(this).removeClass('divisionOtherSelected');
						$(this).addClass('divisionOtherNotSelected');
					}else if($(this).hasClass("divisionFlightSelected")){
						$(this).removeClass('divisionFlightSelected');
						$(this).addClass('divisionFlightNotSelected');
					}
			});
			isSelected=1;
			event.preventDefault();
		});
		
		for (i = 0; i < transportList.length; i++) { 
			var transportTotalDetails = transportList[i].full[0];
			for (j = 0; j < transportList[i].parts.length;j++ ){
				var transportDetailsId = transportList[i].parts[j].id + 'divBox';
				
			}
		}
		
}