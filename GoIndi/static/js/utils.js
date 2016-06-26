function travelSpecificsWidget(source,destination,arrival,departure,duration){
	arrival = getIn12HrFormat(arrival);
	departure = getIn12HrFormat(departure);
	var out = "<table class='journeySpecifics' width = '100%' ><tr><td width='33%' style ='text-align:left'>"+source+"</td><td class = 'journeySpecificsDuration' width='34%' style ='text-align:center'>"+duration+" Hrs</td><td width='33%' style ='text-align:right'>"+destination+"</td></tr><tr><td width='33%' style ='text-align:left'>"+departure+"</td><td class = 'journeySpecificsArrow' width='34%' style ='text-align:center'>&#8594;</td><td width='34%'style ='text-align:right'>"+arrival+"</td></tr></td></tr></table>";
	return out;
}
function travelSpecificsWidget(source,destination,arrival,departure,duration,arrivalDay,departureDay){
	arrival = getIn12HrFormat(arrival);
	departure = getIn12HrFormat(departure);
	var out = "<table class='journeySpecifics' width = '100%' ><tr><td width='33%' style ='text-align:left'>"+source+"</td><td class = 'journeySpecificsDuration' width='34%' style ='text-align:center'>"+duration+" Hrs</td><td width='33%' style ='text-align:right'>"+destination+"</td></tr><tr><td width='33%' style ='text-align:left'>"+departure+", "+departureDay+"</td><td class = 'journeySpecificsArrow' width='34%' style ='text-align:center'>&#8594;</td><td width='34%'style ='text-align:right'>"+arrival+", "+arrivalDay+"</td></tr></td></tr></table>";
	return out;
}

function getIn12HrFormat(time){
	var tmHr = time.split(":")[0];
	var tmMin = time.split(":")[1];
	if ((tmHr*1)>12){
		tmHr = (tmHr*1)-12
		tmAMPM = "PM"
	} else if ((tmHr*1)==12){
		tmAMPM = "PM"
	} else if ((tmHr*1)==0){
		tmHr=12;
		tmAMPM = "AM"
	} else{
		tmAMPM = "AM"
	}
	time = tmHr + ":" + tmMin + " " + tmAMPM;
	return time
}

function minutes(num){
	if(num == 0) {
		return "00";
	}
	var str = num.toString();
	var newStr = str.split(".")[1];
	if(newStr.length==1){
		newStr=newStr+'0';
	}
	return newStr;
}

function getCheckFilterWid(list, filterName,filterLabel, attribute){
	var filterWid = "<div id='"+filterName+"Head' style = 'border-style: solid;border-top:1px' class='filterLabel'data-toggle='collapse' data-target='#"+filterName+"'>"+filterLabel+":</div><br/><div id='"+filterName+"'>";
	var filterSet = new Object();
	for (i = 0; i < list.length; i++) {
			var filter = list[i].full[0][attribute];
			if(filter in filterSet){
			}else{
				filterSet[filter] = true;
			}
			
	}
	for (var key in filterSet) {
		filterWid = filterWid + "<div class = 'checkboxLabel'><input  type='checkbox' rel='"+key+"' checked/>"+key+"</div>";
	}
	filterWid = filterWid + "</div>"
	return filterWid
}