function SortListByPrice(list){
			if(list.length==0){
				return
			}
				function SortByPrice(a,b){
					var aPrice = a.full[0].price
					if(a.full[0].mode == "bus"){
						 aPrice = aPrice.split(",")[0];
					}
					var bPrice = b.full[0].price
					if(b.full[0].mode == "bus"){
						 bPrice = bPrice.split(",")[0];
					}
					return (((aPrice*1)<(bPrice*1))?-1:(((aPrice*1)>(bPrice*1))?1:0));
				}
				list.sort(SortByPrice);
}
function SortListByDuration(list){
			if(list.length==0){
				return
			}
				function SortByDuration(a,b){
					var aDuration = a.full[0].duration;
					var bDuration = b.full[0].duration;
					var aHrs = aDuration.split(":")[0];
					var aMins = aDuration.split(":")[1];
					var bHrs = bDuration.split(":")[0];
					var bMins = bDuration.split(":")[1];
					var HrsRel = (((aHrs*1)<(bHrs*1))?-1:(((aHrs*1)>(bHrs*1))?1:0));
					var MinsRel = (((aMins*1)<(bMins*1))?-1:(((aMins*1)>(bMins*1))?1:0));
					if(HrsRel != 0){
						return HrsRel;
					} else {
						return MinsRel;
					}
				}
				list.sort(SortByDuration);
}
function SortListByArrival(list){
			if(list.length==0){
				return
			}
				function SortByArrival(a,b){
					var aArrival = a.full[0].arrival
					var bArrival = b.full[0].arrival
					var aHr = aArrival.split(":")[0];
					var aMin = aArrival.split(":")[1];
					var bHr = bArrival.split(":")[0];
					var bMin = bArrival.split(":")[1];
					result = 0
					if((aHr*1)<(bHr*1)){
						result = -1
					}else if((aHr*1)>(bHr*1)){
						result = 1
					}else{
						if((aMin*1)<(bMin*1)){
						result = -1
						}else if((aMin*1)>(bMin*1)){
							result = 1
						}
					}
					return result;
				}
				list.sort(SortByArrival);
}
function SortListByDeparture(list){
			if(list.length==0){
				return
			}
				function SortByDeparture(a,b){
					var aDeparture = a.full[0].departure
					var bDeparture = b.full[0].departure
					var aHr = aDeparture.split(":")[0];
					var aMin = aDeparture.split(":")[1];
					var bHr = bDeparture.split(":")[0];
					var bMin = bDeparture.split(":")[1];
					result = 0
					if((aHr*1)<(bHr*1)){
						result = -1
					}else if((aHr*1)>(bHr*1)){
						result = 1
					}else{
						if((aMin*1)<(bMin*1)){
						result = -1
						}else if((aMin*1)>(bMin*1)){
							result = 1
						}
					}
					return result;
				}
				list.sort(SortByDeparture);
}