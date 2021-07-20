$(document).ready(function(){
    $(function() {
        bsCustomFileInput.init()
        var ticket_count = 0;
        reload_ml_report_table();
        $('#ml-report-refresh').on('click',reload_ml_report_table)
        
        $('#M1-running').hide()
        $('#M1-Status').mask("Processing request, Please wait...");
        var stage = 0;
        // General
        // $('.selected-SMILE').innerHtml = 'CCN(CC)CCCC(C)NC1=C2C=C(C=CC2=NC3=C1C=CC(=C3)Cl)OC';
        
        $('#SMILE-GO').click(Identify);
        $('#SMILE-ENTER').keydown(function(event){
            if (event.which == 13)
                Identify()  
        });
        
        $('#SMILE-Select').ready(function(){
            getSMILESlist(function(data){
                var drug_lst = data.drugList;
                var SMILES_lst = data.smilesList;
                var i;
                for (i = 0; i < SMILES_lst.length; i++)
                $('#SMILE-Select').append('<option value='+SMILES_lst[i]+'>'+drug_lst[i]+" - "+SMILES_lst[i]+'</option>')
            });
        })
        $('#SMILE-Select').on('change', function() {
            $(this).siblings("#SMILE-Submit > button").attr('smiles', $('#SMILE-Select').val());
        })

        $('#GCVA-Select').ready(function(){
            
        })
        
    });
    $('.add-model-to-queue').click(function(){
        var model_selected = $(this).attr("model-type"); 
        var req_num = $('.model-ticket').length;
        var fd = new FormData();
        fd.append('selected_model', model_selected);
        function CSVToArray( strData, strDelimiter ){
            // Check to see if the delimiter is defined. If not,
            // then default to comma.
            strDelimiter = (strDelimiter || ",");
    
            // Create a regular expression to parse the CSV values.
            var objPattern = new RegExp(
                (
                    // Delimiters.
                    "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +
    
                    // Quoted fields.
                    "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
    
                    // Standard fields.
                    "([^\"\\" + strDelimiter + "\\r\\n]*))"
                ),
                "gi"
                );
    
    
            // Create an array to hold our data. Give the array
            // a default empty first row.
            var arrData = [[]];
    
            // Create an array to hold our individual pattern
            // matching groups.
            var arrMatches = null;
    
    
            // Keep looping over the regular expression matches
            // until we can no longer find a match.
            while (arrMatches = objPattern.exec( strData )){
    
                // Get the delimiter that was found.
                var strMatchedDelimiter = arrMatches[ 1 ];
    
                // Check to see if the given delimiter has a length
                // (is not the start of string) and if it matches
                // field delimiter. If id does not, then we know
                // that this delimiter is a row delimiter.
                if (
                    strMatchedDelimiter.length &&
                    strMatchedDelimiter !== strDelimiter
                    ){
    
                    // Since we have reached a new row of data,
                    // add an empty row to our data array.
                    arrData.push( [] );
    
                }
    
                var strMatchedValue;
    
                // Now that we have our delimiter out of the way,
                // let's check to see which kind of value we
                // captured (quoted or unquoted).
                if (arrMatches[ 2 ]){
    
                    // We found a quoted value. When we capture
                    // this value, unescape any double quotes.
                    strMatchedValue = arrMatches[ 2 ].replace(
                        new RegExp( "\"\"", "g" ),
                        "\""
                        );
    
                } else {
    
                    // We found a non-quoted value.
                    strMatchedValue = arrMatches[ 3 ];
    
                }
    
    
                // Now that we have our value string, let's add
                // it to the data array.
                arrData[ arrData.length - 1 ].push( strMatchedValue );
            }
    
            // Return the parsed data.
            return( arrData );
        }
    

        if(req_num > -5){
        // if(req_num < 5){
            // Update interface
            addQueue(model_selected, $('.model-ticket').length );
            
            // Get model-specific data
            switch(model_selected){
                case 'GCVA':
                    fd.append('gcvaType',       $('#gcva-specific-model').val());
                    fd.append('gcvaParameters', 'not     implemented');
                    fd.append('ic50Data',       $("#ic50Data")[0].files[0]);
                    fd.append('ccleData',       $("#ccleData")[0].files[0]);
                    fd.append('genomicData',    $("#genomicData")[0].files[0]);

                    break;

                case 'M2M':
                    break;  

                case 'BBBA':
                    fd.append('smiles', 'smiles');
                    break;    

                case 'TTA':
                    break;                    
                    }

            // Make Request
            runMachineModel(fd, function(data){createReportModal(data, req_num)})
        }
        else{
            console.log('Max tickets reached, please wait a moment')
        }
    });
    $('td').each(function() {
        if (this.innerHTML.toLowerCase().indexOf("cyto") != -1) {
            $(this).parent('tr').addClass('highlight');
            $(this).parent('tr').removeClass('table-dark');
            console.log("class added");
        }
    });
    $("#selectable").selectable({
        stop: function () {
            var all = $("td.ui-selected").map(function() {
              return this.innerHTML;
              }).get();
              console.log(all.join());                  
            }
        });

    $('#selectable').addClass(" tftable table-striped ml-5 mb-4 table table-bordered table-responsive-md table-striped text-center ")
    

// ================================================
// ==================== DEMO ======================
// ================================================

    function Identify() {
        $(".SMILES").text($("#SMILE-Select").children("option:selected").html());
        $(".data-card").removeClass('cc-inactive');
        return
    }
    function addQueue(model, details='') {
        var elem1 = $("<div></div>");  
        elem1.addClass("model-ticket btn-outline-primary rounded shadow p-2 mr-2");
        elem1.css("width: 200px");
        // elem1.attr({hidden:'True', 'ticket-num':details})

        var elem2 = $("<h3></h3>").text(model+" Ticket: #"+details);
        elem2.addClass("align-items-center");
        elem2.css("text-align", "center");
        
        var elem3 = $("<div></div>"); 
        elem3.addClass("row align-items-center px-2");
        
        var elem4 = $("<button></button>").html('Pending...'); 
        elem4.addClass("btn btn-secondary mx-auto row");
        elem4.attr('id', 'ticket_num_'+details);
        
        
        var elem5 = $("<span></span>"); 
        elem5.attr({class:'spinner-border spinner-border-sm', role:'status','aria-hidden':'true'})
        
        var elem6 = $("<button></button>").text('stop'); 
        elem6.addClass("btn btn-danger mx-auto cancel-btn");
        elem6.click(function() {
            stopTicket(elem1)
        });

        $("#model-queue").append(elem1.append(elem2.append(elem3.append([elem4.prepend(elem5), elem6]))));
        // $('#box').fadeIn('slow').delay(1000).hide(0);
        return
    }
    function Model_Status(){
        var countup = this;
        var completeClasses = '';
        var runningClasses = '';
        var pendingClasses = '';

        var newNode = document.createElement('div');
        newNode.className = 'textNode news content';
        newNode.innerHTML = 'this created div contains a class while created!!!';
        document.getElementById('dd').appendChild(newNode);
    }

    function updateQueue(req_num, sucess){
        if( sucess == true){
            var ticket = $('#ticket_num_'+req_num);
            ticket.text('Complete');
            ticket.attr('class','btn btn-success mx-auto');
            ticket.siblings('.cancel-btn').hide();
        }
        else{
            var ticket = $('#ticket_num_'+req_num);
            ticket.text('Failed');
            ticket.attr('class','btn btn-danger mx-auto');
            ticket.siblings('.cancel-btn').hide();
        }
    }


    function createReportModal(data, req_num){
        var ifError = '';
        console.log('DEBUG MSG') 
        console.log(data)   
        if('Error' in data){    
            updateQueue(req_num, false)
            ifError = ' <b>('+'Error'+')</b>';
        }
        else if('response error' in data){    
            updateQueue(req_num, false)
            ifError = ' <b>('+'Error'+')</b>';
        }
        else{
             updateQueue(req_num, true)
        }

            // generate report for returned output
        var elem1 = $("<button></button>");
        elem1.attr({class:'btn btn-primary ml-0 mr-2', type:'button', 'data-toggle':'modal', 'data-target':("#model-report-"+req_num)})
        elem1.html("<i>Report "+req_num+' SUMMARY</i>'+ifError)

        var elem2 = $("#model-report-base").clone();
        var report_content = "Report content here";
        elem2.attr({id:'model-report-'+req_num,'tabindex':'-1','aria-labelledby':'exampleModalCenterTitle'});
        elem2.find('.modal-body').append(report_content);
        $('#model-output-card').append(elem2);
        $('#result-body').append(elem1);

        // update queue
        // Model_Status()
    }
    
    function stopTicket(ticket) {
        $(ticket).remove() 
    }

    function reload_ml_report_table() {

        // Get data via ajax
        getMLResults(function(data){
            $('#report-body').html('')
            var i = 0;
            for (i = 0; i < data.length; i++) {
                row = data[i] 
                var td_elemnts = [
                    '<td>'+row[0]+'</td>',
                    '<td>'+row[1]+'</td>',
                    '<td>'+row[2]+'</td>',
                    '<td>'+row[3]+'</td>',
                    '<td>'+row[4]+'</td>',
                    '<td>'+row[5]+'</td>'
                ]
    
                $('#report-body').append('<tr>'+td_elemnts.join('')+'</tr>')
            }
        })

    }

})

