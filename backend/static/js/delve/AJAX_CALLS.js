// Ajax secuirty setup
// ########################################################################################################################
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue; 
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// ########################################################################################################################

// AJAX CALLS
// ########################################################################################################################
function getGlobalSearchList(){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/nav/options",
        dataType: "json",
        traditional: true,
        success : function(response){
            // console.log(response)
            var data = {};
            response.forEach(function(element,key) {
                data = {
                    id: key,
                    text: element
                };
                var newOption = new Option(data.text, data.id, false, false);
                $('#SearchString').append(newOption);
            });
            },
        error: function(){
            return 'Error retreiving data'
            }
    });
    return results;
}
// ########################################################################################################################
// function getGraph(graphic_idx, addTo){
function getGraph(){
        var results;
    $.ajax({
        type: "GET",
        url: "/API/graphicRequest",
        dataType: "json",
        traditional: true,
        // cache: false,
        timeout: 30000,
        data: {'graph_index':28},
        success : function(response){
            var graph = response['graph_ex'];
            $('.graphic-modal-body').append(graph);
            // $(addTo).append(graph);
            // console.log(graph);
            var data = {};
            },
        error: function(){
            console.log("Error retreiving data:")
            return 'Error retreiving data'
            }
    });
    return results;
}



function getSMILESlist(callback){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/SMILESRequest",
        dataType: "JSON",
        traditional: true,
        // cache: false,
        timeout: 30000,
        data: {},
        success : function(response){
            results = response;
            callback(results);
        },
        error: function(){
            console.log("Error retreiving data:")
            callback('Error retreiving data');
            }
    });
    return results;
}

// ==============================  END  ==========================================================
        // ########################################################################################################################

    // AJAX CALLS
    // ########################################################################################################################
    function getGlobalSearchList(){
        var results;
        $.ajax({
            type: "GET",
            url: "/API/nav/options",
            dataType: "json",
            traditional: true,
            success : function(response){
                // console.log(response)
                var data = {};
                response.forEach(function(element,key) {
                    data = {
                        id: key,
                        text: element
                    };
                    var newOption = new Option(data.text, data.id, false, false);
                    $('#SearchString').append(newOption);
                });
                },
            error: function(){
                return 'Error retreiving data'
                }
        });
        return results;
    }
    // ########################################################################################################################
    // function getGraph(graphic_idx,addTo)
    // function getGraph(){
        
    //     var results;
    //     $.ajax({
    //         type: "GET",
    //         url: "/API/graphicRequest",
    //         dataType: "json",
    //         traditional: true,
    //         // cache: false,
    //         timeout: 30000,
            
    //         data: {'graph_index':28},
    //         success : function(response){
    //             var graph = response['graph_ex'];
    //             $('#graphic-modal-body').append(graph);
    //             console.log(graph);
    //             var data = {};
    //             },
    //         error: function(){
    //             console.log("Error retreiving data:")
    //             return 'Error retreiving data'
    //             }
    //     });
    //     return results;
    // }

    function getGraphic(graphic_idx){
        // var graphic_idx=$("#g_id").val();
        // var id=$("#value").val();
        var results;
        $.ajax({
            type: "GET",
            url: "/API/graphicRequest",
            dataType: "json",

            traditional: true,
            // cache: false,
            timeout: 30000,
            
            data: {'graph_index': graphic_idx},
            success : function(response){
                var graph = response['graph_ex'];
                $('#graphic-modal-body').append(graph);
                console.log(graph);
                var data = {};
                },
            error: function(){
                console.log("Error retreiving data:")
                return 'Error retreiving data'
                }
        });
        return results;
    }
    function getIc50(s) {
        console.log("hello")
        $.ajax({
            type: "GET",
            url: "/API/ic50search/",
            traditional: true,
            timeout: 30000,
            data: { 'search': s},
            success: function(data) {
                console.log("inside function")
                $('#search-results').append(data);
                console.log("successfully displayed")
                console.log(data)
            },
            error: function () {
                console.log("Error retreiving data:")
                return 'Error retreiving data'
            }
        });
    }
    //leading drugs for the entered cell line name
function getCellLine(cell_name,score){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/cellLineRequest",
        dataType: "json",

        traditional: true,
        // cache: false,
        timeout: 30000,
        
        data: {'c_name': cell_name,'score':score},
        success : function(response){
            console.log("success");
            var g = response['cell_response'];
            $('#cell-graphic-modal-body').append(g);

            console.log(g);
            var data = {};
            },
        error: function(){
            console.log("Error fetching data:")
            return 'Error fetching data'
            }
    });
    return results;
}

//leading cell lines for the entered drug name
function getDrug(drug_name,score){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/drugRequest",
        dataType: "json",

        traditional: true,
        // cache: false,
        timeout: 30000,
        
        data: {'d_name': drug_name,'score':score},
        success : function(response){
            console.log("success");
            var g = response['drug_response'];
            $('#drug-graphic-modal-body').append(g);

            console.log(g);
            var data = {};
            },
        error: function(){
            console.log("Error getting data:")
            return 'Error getting data'
            }
    });
    return results;
}

//leading drugs for the entered cancer name
function getIndication(indi_name,score){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/indicationRequest",
        dataType: "json",

        traditional: true,
        // cache: false,
        timeout: 30000,
        
        data: {'i_name': indi_name,"score":score},
        success : function(response){
            console.log("success of cancer modal");
            var g = response['indi_response'];
            $('#indi-graphic-modal-body').append(g);
            console.log(g);
            var data = {};
            },
        error: function(){
            console.log("Error getting data:")
            return 'Error getting data'
            }
    });
    return results;
}

//leading indications for the entered drug name
function getDrugforIndication(drug_name,score){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/drugIndicationRequest",
        dataType: "json",

        traditional: true,
        // cache: false,
        timeout: 30000,
        
        data: {'drug_name': drug_name,"score":score},
        success : function(response){
            console.log("success of drug vs cancer modal");
            var g = response['drugIndi_response'];
            $('#drugIndi-graphic-modal-body').append(g);
            console.log(g);
            var data = {};
            },
        error: function(){
            console.log("Error getting data:")
            return 'Error getting data'
            }
    });
    return results;
}

//best performing drugs for the entered drug 1 name
function getDrugvsDrug(drug_name,score){
    var results;
    $.ajax({
        type: "GET",
        url: "/API/drugvsdrugRequest",
        dataType: "json",

        traditional: true,
        // cache: false,
        timeout: 30000,
        
        data: {'d1_name': drug_name,"score":score},
        success : function(response){
            console.log("success of drug vs drug modal");
            var g = response['dvd_response'];
            $('#d1d2-graphic-modal-body').append(g);
            console.log(g);
            var data = {};
            },
        error: function(){
            console.log("Error getting data:")
            return 'Error getting data'
            }
    });
    return results;
}

function getIc50(s) {
    console.log("hello")
    $.ajax({
        type: "GET",
        url: "/API/ic50search/",
        traditional: true,
        timeout: 30000,
        data: { 'search': s},
        success: function(data) {
            console.log("inside function")
            $('#search-results').append(data);
            console.log("successfully displayed")
            console.log(data)
        },
        error: function () {
            console.log("Error retreiving data:")
            return 'Error retreiving data'
        }
    });
}

function runMachineModel(fd, callback){
    // SUMMARY: requests form data to send over to server
    // Form data should contain: the model type; the corresponding data; the user that requested



    // formData.append('csrfmiddlewaretoken', CSRF_TOKEN); # django security
    var results;
    $.ajax({
        type: "POST",
        // headers: {  'Access-Control-Allow-Origin': 'http://127.0.0.1:5000/' },
        // crossDomain: true,
        url: "/API/MLRequest/",
        processData: false,
        contentType: false,
        data: fd,
        timeout: 30000,
        
        
        success : function(response){
            // console.log(response)
            // saveMLResults(response)
            callback(response)
            },
        error: function(response){
            console.log("Error getting data:")
            console.log(response);
            callback({'Error':false})
            }
    });
    return results;
}

    
function addMachineModel(model_name, modelFile, description){
    var results;
    var fd = new FormData();
    fd.append('model', modelFile);
    fd.append('desc', description);
    fd.append('mod_name', model_name);
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/new-model-5593b0b371cd2e0e900d0c99e644890c",
        processData: false,
        contentType: false,
        data: fd,
        timeout: 30000,
        
        success : function(jqxhr, status, msg){
            console.log("jqxhr, status, msg");
            console.log(jqxhr, status, msg);
            },
        error: function(jqxhr, status, msg){
            console.log("Error getting data:")
            console.log("jqxhr, status, msg");
            console.log(jqxhr, status, msg);
            }
    });
    return results;
}

function saveMLResults(item){
    var form_data = new FormData();

    for ( var key in item ) {
        form_data.append(key, item[key]);
    }
    $.ajax({
        type: "POST",
        url: "/API/MLSave/",
        processData: false,
        contentType: false,
        data: form_data,
        timeout: 30000,
        
        success : function(response){
            },
        error: function(response){
            console.log("Error saving data:")
            }
    });
}


function getMLResults(callback){
    $.ajax({
        type: "GET",
        url: "/API/getMLReport",
        processData: false,
        contentType: false,
        timeout: 30000,
        
        success : function(jqxhr, status, msg){
            callback(jqxhr)
            },
        error: function(jqxhr, status, msg){
            console.log("Error getting data:")
            callback([])
            }
    });
}