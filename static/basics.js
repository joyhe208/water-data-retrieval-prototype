var sizeCells = 13;
var heightMatrices = 12*sizeCells, widthMatrices = 31*sizeCells;
var waterYearStart = '01-01'
var toolTip = d3.select('body').append('div').attr('class','tooltip').style('opacity', 0);
var useWaterYear = true;

function createRange(start,circle,end) {
	var ret = [];
	var i = start;
	while (i <= circle) {
		ret.push(i);
		i++;		
	}
	i = 1;
	while (i <= end) {
		ret.push(i);
		i++;		
	}
	return ret;
}

function toText(data) {
	var res = '';
	var obj = data[0];
	res = Object.keys(obj).join(',');
	res += ';';
	Array.from(data).forEach(function(e) {
		res += Object.values(e).join(',') + ';';
	});
	return res;
}

function toData(text) {
	var res = [];
	var headers = text.substring(0,text.indexOf(';')).split(',');
	text = text.substring(text.indexOf(';')+1);
	var lineArray = text.split(';').forEach(function(d){
		if (d.trim().length > 0) {
			var values = d.split(',');	
			var obj = {};
			headers.forEach(function(h,i){
				obj[h] = values[i];
			});
			res.push(obj);
		}
	});
	return res;
}
