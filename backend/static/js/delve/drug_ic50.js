window.onload = prime_api()
    function prime_api(){
        draw_widget("241")
        $(output).hide()    
    }
    
    var tbl = document.getElementById("chem_table");
    if (tbl != null) {
        for (var i = 0; i < tbl.rows.length; i++) {
            tbl.rows[i].onclick = function () { draw_widget(this.id);
            };
        }
    }
    
    function draw_widget(chem_cid){
        $(output).show()
        var http = new XMLHttpRequest();
        var slug = "https://pubchem.ncbi.nlm.nih.gov/compound/";
        var endslug = "#section=3D-Conformer&embed=true";
        var source = slug.concat(chem_cid | 0, endslug);
        document.getElementById('output').src = source;

        console.log('Status: '+document.getElementById('output').src);

        if(http.status == 200){
            var endslug = "#section=2D-Structure&embed=true";
            var source = slug.concat(chem_cid | 0, endslug);
            // document.getElementById('output').src = source;         
        }
            
    }