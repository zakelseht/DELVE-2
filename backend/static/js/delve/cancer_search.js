$(document).ready(function(){
    $(function() {
        // append calls to html
        // additionalz
        $('#SearchString').select2({
            // data: ["MCF7","Etoposide", "Merkel Cell Carcinoma"],
            tags: true,
            maximumSelectionLength: 10,
            selectOnClose: true,
            tokenSeparators: [',', ' '],
            placeholder: "Select or type keywords",
        });
        
    
    });
})