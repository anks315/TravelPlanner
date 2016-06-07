var routeMap = {}
var flightRouteList
var trainRouteList
function routeFilter(transportList,mode){
	if(mode=='flight'){
		flightRouteList=0
	} else if(mode == 'train'){
		trainRouteList=0
	}
	routeMap[mode] ={}
	if(transportList.length>0){
		
	}else{
		return
	}
	
	var routeList = new Array()
	for (var i = 0; i < transportList.length;i++ ){
		var route = transportList[i].full[0].route
		if(!(route in routeMap[mode])){
			routeList[routeList.length]=route
			routeMap[mode][route]=new Array()
		} 
		routeMap[mode][route][routeMap[mode][route].length] = transportList[i]
	}
	for(var route in routeMap[mode]){
		SortListByPrice(routeMap[mode][route])
	}
	if(mode=='flight'){
		flightRouteList=routeList
	} else if(mode == 'train'){
		trainRouteList=routeList
	}
	 
}