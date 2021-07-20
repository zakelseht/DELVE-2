$(document).ready(function(){
    console.log("inside");
    $(function() {
        //graph using id
        $("#dynamicButton").mouseover(function(){
            getGraphic($("#graphicRequestDynamic").val());
            console.log("mouse over");
        });
        //Leading drugs for cell line
        $('#cellLineButton').click(function(){
            console.log("clicked");
            getCellLine($("#cellLineRequestDynamic").val(),$("#cell_scorename").val());
        });
        //Leading cell line for drug
        $('#drugButton').click(function(){
            console.log("clicked");
            getDrug($("#drugRequestDynamic").val(),$("#d_scorename").val());
        });
        //Cancer vs drugs
        $('#indiButton').click(function(){
            console.log("clicked indiButton");
            getIndication($("#indicationRequestDynamic").val(),$("#c_scorename").val());
        });
        //Drugs vs Cancer
        $('#drugIndiButton').click(function(){
            console.log("clicked drugIndiButton");
            getDrugforIndication($("#drugIndicationRequestDynamic").val(),$("#drugc_scorename").val());
            
        });
        //Drug vs Drug
        $('#d1Button').click(function(){
            console.log("clicked d1Button");
            getDrugvsDrug($("#d1RequestDynamic").val(),$("#dvd_scorename").val());
        });

        $('#Refresh').click(getGlobalSearchList);

        // additional
        // $('#SearchString').select2({
        //     // data: ["MCF7","Etoposide", "Merkel Cell Carcinoma"],
        //     tags: true,
        //     maximumSelectionLength: 10,
        //     selectOnClose: true,
        //     tokenSeparators: [',', ' '],
        //     placeholder: "Select or type keywords",
        // });
        
    
    });
    
})