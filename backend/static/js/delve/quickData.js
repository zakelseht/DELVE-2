$(document).ready(function(){
    $(function() {
        // append calls to html
        $('#graphicButton').click(function(){
            
            // var graph = getGraph(graph_idx,)
            // append to html here:
            // $('#').apend(graph)
        });
        $('#graphicButton').click(function(){
            console.log("sad");
        });
        // $('#graphicButton').click(getGraph(28,'#ex_h3'));
        $('#Refresh').click(getGlobalSearchList);

        // additionalz
        $('#SearchString').select2({
            // data: ["MCF7","Etoposide", "Merkel Cell Carcinoma"],
            tags: true,
            maximumSelectionLength: 10,
            selectOnClose: true,
            tokenSeparators: [',', ' '],
            placeholder: "Select or type keywords",
        });
        
        var originalText = $("#textContainer").html()
        $("#search").on('keyup', function () {
        $("#textContainer").html(originalText)
        var text = $("#textContainer").html()
        var val = $("#search").val()
        if(val=="") return;
        var matches = text.split(val)
        for(var i=0;i<matches.length-1;i++) {
            var ind =  matches[i].indexOf(val)
            var len = val.length
            matches[i] = matches[i] + "<span class='selected'>" + val + "</span>"
        }
        $("#textContainer").html(matches.join(""))
        })
    });
})