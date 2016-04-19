var bus = [{"full":[{"id":"bus1","mode":"bus","price":"1000","duration":"10:15","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"1000","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]}]
var bus2 = [{"full":[{"id":"bus1","mode":"bus","price":"7000","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"1000","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]}]
var bus3 = [{"full":[{"id":"bus1","mode":"bus","price":"1200","duration":"12:50","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"1000","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]}]

var busList = [{"full":[{"id":"bus1","mode":"bus","price":"6000","duration":"13:05","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"6000","duration":"13:05","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]},{"full":[{"id":"bus1","mode":"bus","price":"1200","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"1200","duration":"12:35","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]},{"full":[{"id":"bus1","mode":"bus","price":"7000","duration":"12:50","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"bus11","mode":"bus","price":"7000","duration":"12:50","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]}];


var trainList = [{"full":[{"id":"train1","mode":"train","price":"1200","duration":"10:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12"}],"parts":[{"id":"train11","mode":"train","price":"600","duration":"10:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Sampark Kranti"},{"id":"train12","mode":"train","price":"600","duration":"10:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Rajdhani"}]},{"full":[{"id":"train2","mode":"train","price":"1500","duration":"13:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"train21","mode":"train","price":"1000","duration":"12:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Sampark Kranti"}]},{"full":[{"id":"train3","mode":"train","price":"1100","duration":"08:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}],"parts":[{"id":"train31","mode":"train","price":"300","duration":"10:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Sampark Kranti"},{"id":"train32","mode":"train","price":"800","duration":"08:35","site":"irctc","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Rajdhani"}]}]


var flightList = [{"full":[{"id":"flight1","mode":"flight","price":"5000","duration":"10:00","site":"","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet"}],"parts":[{"id":"flight11","mode":"train","price":"300","duration":"2:30","site":"","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Sampark Kranti"},{"id":"flight12","mode":"flight","price":"4500","duration":"2:00","site":"makemytrip","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet","flightId":"GT-108"},{"id":"flight13","mode":"bus","price":"200","duration":"2:30","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]},{"full":[{"id":"flight2","mode":"flight","price":"5000","duration":"10:00","site":"","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet"}],"parts":[{"id":"flight21","mode":"flight","price":"4500","duration":"2:00","site":"makemytrip","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet","flightId":"GT-108"}]},{"full":[{"id":"flight3","mode":"flight","price":"5000","duration":"10:00","site":"","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet"}],"parts":[{"id":"flight31","mode":"train","price":"300","duration":"2:30","site":"","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Sampark Kranti"},{"id":"flight32","mode":"flight","price":"4500","duration":"2:00","site":"makemytrip","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"SpiceJet","flightId":"GT-108"},{"id":"flight33","mode":"bus","price":"200","duration":"2:30","site":"travelyaari","source":"Delhi","destination":"Mumbai","departure":"00:12","arrival":"13:12","carrierName":"Vishal Travels"}]}]

function showSummary(){
	var options = new Array();
		options[0]=busList[0];
		options[1]=trainList[0];
		options[2]=flightList[0];
	var leastPrice = options[0].full[0].price;
	var leastDuration = options[0].full[0].duration;
	for (i = 1; i < options.length; i++) { 
		var price = options[i].full[0].price;
		if(price < leastPrice){
			leastPrice = price;
		}
	}
	for (i = 1; i < options.length; i++) { 
		var duration = options[i].full[0].duration;
		var durArr = duration.split(":");
		var leastDurArr = leastDuration.split(":");
		if(durArr[0] < leastDurArr[0]){
			leastDuration = duration;
		}
		if(durArr[0] == leastDurArr[0]){
			if(durArr[1] < leastDurArr[1]){
				leastDuration = duration;
			}
		}
		
	}
	var widlist = "";
	for (i = 0; i < options.length; i++) { 

		var wid = "";
		var division = 100/options[i].parts.length;
		for(j=0; j < options[i].parts.length; j++){
			wid = wid+"<td width = \""+division+"%\"><table width = \"100%\"><tr><td width = \"10%\"><img src=\"/images/"+options[i].parts[j].mode+".png\"/></td><td width = \"90%\">&nbsp<hr width=\"100%\" style='margin-top:0em;margin-bottom:0em'/>&nbsp</td><tr></table></td>"
		}
		if(options[i].full[0].price == leastPrice){
			var priceColor = "green";
		} else {
			var priceColor = "red";
		}
		
		if(options[i].full[0].duration == leastDuration){
			var durationColor = "green";
		} else {
			var durationColor = "red";
		}
		widlist = widlist + "<tr><td   style = 'text-align: center;white-space: nowrap'><font color='"+priceColor+"'>&#8377 "+options[i].full[0].price+"/-&nbsp;&nbsp</font></td><td><table width = '100%'><tr>"+wid+"</tr></table></td><td  style = 'text-align: center;white-space: nowrap'><font color='"+durationColor+"'>&nbsp;&nbsp"+options[i].full[0].duration+" Hr</font></td></tr>";
	}
	
	 var output = "<div class='panel panel-default'><div class='panel-body'><table width = '100%'><tr><th  style = 'text-align: center'><font color='grey'>Price</font></th><th></th><th  style = 'text-align: center'><font color='grey'>Duration</font></th></tr>"+widlist+"</table></div></div>";
	 
	 document.getElementById("summary").innerHTML = output;
	
}

