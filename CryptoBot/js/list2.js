document.addEventListener('DOMContentLoaded', function(){
    $(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "data.txt",
        dataType: "text",
        success: function(data) {processData(data);}
     });
});

function processData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    console.log(allTextLines);
    var headers = allTextLines[0].split(',');
    console.log(headers);
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        console.log(data.length);
        console.log(headers.length);
        if (data.length == headers.length) {

            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(data[j]);
            }
            lines.push(tarr);
        }
    }

	    var content = "";
	    lines.forEach(function(row) {
        	content += "<tr>";
        	row.forEach(function(cell) {
            	content += "<td>" + cell + "</td>" ;
        });
        	content += "</tr>";
    });
    document.getElementById("cycleData").innerHTML = content;

	console.log(lines);
    // alert(lines);

}


});
