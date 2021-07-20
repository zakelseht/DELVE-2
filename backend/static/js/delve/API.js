$(document).ready(function(){


    // Select2 plugin
    // $('.js-example-basic-multiple').select2();
    document.onload =  function myFunction1() {
        var d = new Date();
        var n = d.getTime();
        $('#demoo').innerHTML = n;
        console.log(n)
      }
    // AJAX GET
    function autocompleteFunc(){
        // empty result html container
        $('.topnav-dropdown').empty();

        // fill with search results of api request
        $.ajax({
                type:"GET",
                url: "ajax/nav/",
                error: function(data){
                    console.log('Error: ajax request failed');
                },          
                success: function(data){
                for(i = 0; i < data.length; i++){
                    $('.topnav-dropdown').append('<a class="row ml-2">'+data[i].__str__()+'</a>');
                    console.log('message:  ' + Object.keys(data[i].pk));
                }
            }
        }); 
        $('.topnav-dropdown').css('display','block');

    };
    $(function() {
        $('.autocomplete-nav').click(autocompleteFunc);
        $('.autocomplete-nav').keyup(autocompleteFunc());

    });
    // $('.autocomplete-nav').click(autocompleteFunc());
    // $('.autocomplete-nav').keyup(autocompleteFunc());
    // $('.autocomplete-nav').onkeypress =  autocompleteFunc();

    // a = div.getElementsByTagName("a");
    // for (i = 0; i < a.length; i++) {
    //   txtValue = a[i].textContent || a[i].innerText;
    //   if (txtValue.toUpperCase().indexOf(filter) > -1) {
    //     a[i].style.display = "";
    //   } else {
    //     a[i].style.display = "none";
    //   }
    // }
    // AJAX POST
    

    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
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

    // Ajax setup
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
})