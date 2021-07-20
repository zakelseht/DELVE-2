$(document).ready(function(){
  

    $(function() {
      // ========================================
      // ============= AJAX calls ===============
      // ========================================

      // Map Ajax commands from AJAX_CALLS.js here 

      // ========================================

      // ========================================
      // ======== Page scpecific JQuery =========
      // ========================================

        $(".custom-file-input").on("change", function() {
            var fileName = $(this).val().split("\\").pop();
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
          });
        $("#goStage2").click(invalidCytoTable);
        $("#selectable").selectable({
            stop: function () {
                var all = $("td.ui-selected").map(function() {
                  return this.innerHTML;
                  }).get();
                  console.log(all.join());                  
                }
            });

        $('#selectable').addClass(" tftable table-striped ml-5 mb-4 table table-bordered table-responsive-md table-striped text-center ")
        

        $('#selectable').css({margin:0});
        $('#selectable td').css({
            padding: 5, 
            margin: 0,
            overflow: 'hidden',
            "font-size": 12,
        });
            
        $('td').each(function() {
              if (this.innerHTML.toLowerCase().indexOf("cyto") != -1) {
                  $(this).parent('tr').addClass('highlight');
                  $(this).parent('tr').removeClass('table-striped');
                  console.log("class added");
              }
          });
        
        $(".progress").each(function() {

            var value = $(this).attr('data-value');
            var left = $(this).find('.progress-left .progress-bar');
            var right = $(this).find('.progress-right .progress-bar');
        
            if (value > 0) {
              if (value <= 50) {
                right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
              } else {
                right.css('transform', 'rotate(180deg)')
                left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
              }
            }
        
          })
          
          $('input:radio[name=data-view]').change(function() {
            // console.log("Smart search: on");
            if($('input:radio[name=data-view]:checked').val() == "smart-search"){
              // call smart search
              console.log("Smart search: on");
              
              // get 2d array fo table
              var ar = table_to_array('selectable');
              var tableFlag = false;
              for(var row = 0; row < ar.length-6; row++) {
                var ar_row = ar[row];
                for(var col = 1; col < ar_row.length; col++) {
                  if( ifSix( ar_row.slice(col-1, col+7) ) ) //if number, do this
                  {
                    for(var i = 0; i < 6; i++)
                      if(!ifSix( ar[row+i].slice(col-1, col+7) ))
                      {
                        tableFlag = false;
                        break
                      }
                    
                    for(var i = 0; i < 6; i++)
                      for(var j = 0; j < 6; j++)
                      {
                        if(isNum(ar[row+i][col+j]))
                          break
                      }
                    // for(var i = 0; i < 6; i++)
                      // $('#selectable tr')[row+i].style.backgroundColor = "yellow";
                      
                    }
                }
              }
              if(true){

              }
 
            }
            // $('#selectable tr:not(:contains("Nilotinib"))').hide();
            // or
            // < highlight smart searched tables >
            // < hide un-highlighted rows >
            

          });
          
          // Makes it so that on page load the radio button (smart-search) change-event (above) fires 
          $('input:radio[name=data-view]:first').click();
          
          // ======================================================================================================================== 
          // CUSTOM FUNCTIONS =======================================================================================================
          // ========================================================================================================================

          function ifSix(arr) // takes array of size 8? NOTE: isNaN() does not work; empty strings or bools are caught as numbers
          {
            if(arr.length != 8){
              return false;

            }
            if( !isNum(arr[0]) && !isNum(arr[7]))
            { //if first and last items are not a number number, check inside            
              for(i = 1; i<7; i++)
              {
                if(!isNum(arr[i]))
                {
                  return false
                }
              }            
            }
            else // otherwise, return False
              return false
            return true
          }

          function percentageToDegrees(percentage) {
              return percentage / 100 * 360
          }

          function transpose(arr){
            transposed_arr = m => m[0].map((x,i) => m.map(x => x[i]));
            return transposed_arr
          }

          function table_to_array(table_id) {
            myData = document.getElementById(table_id).rows
            my_liste = []
            for (var i = 0; i < myData.length; i++) {
              el = myData[i].children
              my_el = []
              for (var j = 0; j < el.length; j++) {
                my_el.push(el[j].innerText);
              }
              my_liste.push(my_el)
        
              }
              return my_liste
            }

            function isInt(value) {
              return !isNaN(value) && (function(x) { return (x | 0) === x; })(parseFloat(value))
            }
            function isNum(value) {
              return !isNaN(value) && (value != NaN) && (value != null) && (value != "")
            }
            function invalidCytoTable() {
              alert("Sorry, this is an invalid cyto table selection (check for proper size or that something is selected)");
            }
          
      // ========================================
    });


})

$(document).on("paste", "input[type=text]", function(){
    var input_id = $(this).attr("id");
    var value;
    if (event.originalEvent.clipboardData) { // Firefox, Chrome, etc.
        value = event.originalEvent.clipboardData.getData('text/plain');
    } else if (window.clipboardData) { // IE
        value = window.clipboardData.getData("Text")
    } else {
        // clipboard is not available in this browser
        return;
    }
    /* ... */
    event.preventDefault(); // prevent the original paste
});