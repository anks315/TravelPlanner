function showtransportJourneyList(transportList, mode){
	if(transportList.length>0){
		SortListByPrice(transportList);
	}
	
	if(mode == 'flight'){
		showFlightJourneyList(transportList);
	}else{
		showTrainJourneyList(transportList);
	}
}