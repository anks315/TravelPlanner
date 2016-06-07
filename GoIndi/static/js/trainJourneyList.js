var radionames = []
var isSelected =0
function showTrainJourneyList(transportList){
	if(transportList.length==0){
		var noData = '<br/><br/><br/><br/><br/><div class="tabLoading"><table width="100%" style="text-align:center"><tr><td>Sorry! We could not find any Trains on this Route<br/>Check out Flight or Bus for more options</td></tr><tr><td><br/></td></tr></table></div>'
		document.getElementById("trainData").innerHTML = noData;
		return;
	}
	var output = "<br/><div id='trainBox' hidden><table width='100%'><tr>";
	for (i = 0; i < transportList.length; i++) { 
		var transportTotalDetails = transportList[i].full[0];
        var transportTotaljourney = "";
		
		var journeyDividerContent = "";
		var individualJourneyDetails = "";
		var summary = "<br/>";
		var fontSize = 'h4'
		var travelSplitter = ''
		if(transportList[i].parts.length>1){
			if(transportList[i].parts.length ==2){
				customWidth = 44
			} else if (transportList[i].parts.length ==3){
				customWidth = 28
			}
			travelSplitterParts = ''
			for (var q = 0; q < transportList[i].parts.length;q++ ){
				travelSplitterParts = travelSplitterParts + "<td width='"+customWidth+"%'>&nbsp;<hr/>&nbsp;</td><td width='4%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+transportList[i].parts[q].destination+"</font></b></td>";
			}
			travelSplitter = travelSplitter + "<table width='100%' style = 'text-align:center'><tr><td width='1%'><b><font color = '#dfa158' style='white-space: nowrap;'>"+transportList[i].parts[0].source+"</font></b></td>"+travelSplitterParts+"</tr></table>"
			fontSize = 'h5'
			summary="<table width = '100%'><tr><td style='text-align:left;padding: 5px;' width='20%'><div class='journeyPriceSumLabel'>duration starts from</div><div class='journeyDuration sameLine'> <div class='sameLine'>"+transportTotalDetails.duration+" Hrs</div></div></td><td width='60%'>"+travelSplitter+"</td><td style='text-align:right;padding: 5px;' width='20%'><div class='journeyPriceSumLabel'>price starts from</div><div class='journeyPrice sameLine'>  &#8377 <div class='sameLine'>"+transportTotalDetails.price+"</div>/-</div></td></tr></table>"
		}
		
		for (j = 0; j < transportList[i].parts.length;j++ ){
			var transportDetails = transportList[i].parts[j];
			if(transportDetails.mode == 'train'){
				var first = 1;
				for(var q=0;q<transportDetails.subParts.length;q++){
					
					if(first==1 ){
						transportTotaljourney = transportTotaljourney +transportDetails.subParts[q].carrierName
						first = 0;
					} else {
						transportTotaljourney = transportTotaljourney + "&nbsp;&#8594;&nbsp" +transportDetails.subParts[q].carrierName;
					}
				}
			}
			if(transportDetails.mode=='train'){
				selectedClass = 'divisionTrainSelected';
				boxTypeClass = 'divisionTrainBox';
			}else{
				selectedClass = 'divisionOtherNotSelected';
				boxTypeClass = 'divisionOtherBox';
			}
			
			//bar displaying journey division on the main widget
			
			
				 
			var carrierClass = '';
			var colspan = '';
			var hiddenProperty = '';
			if(transportDetails.mode == "train"){
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
			if(transportDetails.mode == "train"){
				
				
				var travelSpecificWid = travelSpecificsWidget(transportDetails.source,transportDetails.destination,transportDetails.arrival,transportDetails.departure,transportDetails.duration);
				
				individualJourneyDetails = individualJourneyDetails+"<div class='"+transportDetails.id+"divBox detailsBox"+i+"'> <table width='100%'><tr ><td ><div class='row-eq-height'><div class='col-sm-3 col-height col-middle' style ='text-align:left'><font color = 'grey'>"+numberOfChangesView+"<br/>&nbsp;</div><div class='col-sm-6 col-height col-middle' style ='text-align:center'>"+travelSpecificWid+"</div></font><div class='col-sm-3 col-height col-middle'><table width = '100%' style ='text-align:right'><tr><td><"+fontSize+" style='white-space: nowrap;'><font color='green'>&#8377 "+transportDetails.price+"/-</font><"+fontSize+"></td></tr></table></div></div></tr></table></div>"
			
			}else{
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
			}
	
		}
			
				
				var journeyDivider = summary+"<table class='table table-bordered' style ='text-align:center' ><tbody><tr>"+journeyDividerContent+"</tr><tr><td colspan='"+transportList[i].parts.length+"'>"+individualJourneyDetails+"</td></tr></tbody></table>";
				
				output = output + "<div class='trainMain' id = 'main"+transportTotalDetails.id+"'><tr><td bgcolor='WhiteSmoke'><div class='row-eq-height'><table width = '100%'><tr><td width = '75%' style ='text-align:left'>&nbsp;&nbsp;<font color = '#056273'><b>"+transportTotaljourney+"</b></td><td width = '25%' style ='text-align:right'><button type='button' class='btn btn-warning'  data-toggle='modal' data-target='#details"+transportTotalDetails.id+"'>Select</button>&nbsp;&nbsp;</td></tr></table></div></td></tr><tr><td><div class='row-eq-height'>"+journeyDivider+"</div>";
				
				output = output + "<div class='modal fade modal-wide' id='details"+transportTotalDetails.id+"' role='dialog'><div class='modal-dialog'><div class='modal-content'><div class='modal-body'>"+getModalForTrains(transportList[i].parts,transportTotalDetails.id)+"</div></div></div></div></td></tr></div>";
				
	}
	output = output + "</table></div>"
	//binding data to trains tab
		$("#trainData").empty();
		document.getElementById("trainData").innerHTML = output;
	for(var l=0; l<radionames.length;l++){
		$("input:radio[name='"+radionames[l]+"']").change(function(){
			var id = $(this).attr('class');
			getTotalPrice(id);
		});
	}
	
		$(".dropdown-menu li a").click(function(){
			
			  var selText = $(this).text();
			  var price = $(this).attr('price');
			  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
			  var selectedPrice = document.getElementById($(this).attr("trainClassId"))
			  selectedPrice.innerHTML = "&#8377 "+price+"/-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			  selectedPrice.setAttribute('price',price);
			  var className = selectedPrice.getAttribute('trainclass');
			  changePrice(className);
			
		});
			
		$("#trainBox").fadeIn();
		$(".bookingTrain").click(function() {
			
			var win = window.open('http://irctc.co.in', '_blank');
			win.focus();
	});
		//setting action on mode menu box
		$(".divisionTrainBox").mouseover(function() {
					if($(this).hasClass("divisionTrainSelected")){
						isSelected=1;
					}else{
						isSelected=0;
					}
					$(this).removeClass('divisionTrainNotSelected');
					$(this).addClass('divisionTrainHover');
				}).mouseout(function() { 
				$(this).removeClass('divisionTrainHover');
				if(isSelected){
					$(this).addClass('divisionTrainSelected');
				} else {
					$(this).addClass('divisionTrainNotSelected');
				}
					
				});
		$(".divisionTrainBox").click(function() {
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
					}else if($(this).hasClass("divisionTrainSelected")){
						$(this).removeClass('divisionTrainSelected');
						$(this).addClass('divisionTrainNotSelected');
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
					}else if($(this).hasClass("divisionTrainSelected")){
						$(this).removeClass('divisionTrainSelected');
						$(this).addClass('divisionTrainNotSelected');
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