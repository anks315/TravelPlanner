function showtransportJourneyList(transportList, mode){
	
	
	if(mode == 'flight'){
		showFlightJourneyList(transportList);
	}else{
		showTrainJourneyList(transportList);
	}
}