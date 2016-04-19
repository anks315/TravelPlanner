function travelSpecificsWidget(source,destination,arrival,departure,duration){
	var out = "<table class='journeySpecifics' width = '100%' ><tr><td width='33%' style ='text-align:left'>"+source+"</td><td class = 'journeySpecificsDuration' width='34%' style ='text-align:center'>"+duration+" Hr</td><td width='33%' style ='text-align:right'>"+destination+"</td></tr><tr><td width='33%' style ='text-align:left'>"+departure+"</td><td class = 'journeySpecificsArrow' width='34%' style ='text-align:center'>&#8594;</td><td width='34%'style ='text-align:right'>"+arrival+"</td></tr></td></tr></table>";
	return out;
}
