var routeMap = {}
var flightRouteList
var trainRouteList
function routeFilter(transportList,mode){
	routeMap[mode] ={}
	var routeList = new Array()
	for (var i = 0; i < transportList.length;i++ ){
		var route = transportList[i].full[0].route
		if(!(route in routeMap[mode])){
			routeList[routeList.length]=route
			routeMap[mode][route]=new Array()
		} 
		routeMap[mode][route][routeMap[mode][route].length] = transportList[i]
	}
	if(mode=='flight'){
		flightRouteList=routeList
	} else if(mode == 'train'){
		trainRouteList=routeList
	}
	 
}