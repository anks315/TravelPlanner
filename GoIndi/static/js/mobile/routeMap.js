var routeMap = new Object()
var flightRouteList=new Array()
var trainRouteList=new Array()
var busRouteList=new Array()
function routeFilter(transportList,transportMode){
	if(transportList.length>0){
		if(!routeMap[transportMode]){
			routeMap[transportMode]={}
		}
	}else{
		return
	}
	
	var routeList = new Array()
	for (var i = 0; i < transportList.length;i++ ){
		var route = transportList[i].full[0].route
		if(!(route in routeMap[transportMode])){
			routeList[routeList.length]=route
			routeMap[transportMode][route]=new Array()
		} 
		routeMap[transportMode][route][routeMap[transportMode][route].length] = transportList[i]
	}
	
	if(transportMode=='flight'){
		flightRouteList=flightRouteList.concat(routeList)
	} else if(transportMode == 'train'){
		trainRouteList=trainRouteList.concat(routeList)
	} else if(transportMode == 'bus'){
		busRouteList=busRouteList.concat(routeList)
	}
	 
}