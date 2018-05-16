document.addEventListener('DOMContentLoaded', function(){
    $(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "transactions.txt",
        dataType: "text",
        success: function(data) {processData(data);}
     });
});

function processData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
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
    document.getElementById("transactionBody").innerHTML = content;

	console.log(lines);
    // alert(lines);

}


});
