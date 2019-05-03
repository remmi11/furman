var searchText = "{}";
var postTable = null;
var reload = null;

var mymap = null;
var mapMarkers = [];

var defaultPt = [35.1939828742388, -101.90669834943];
var goe = [];
var mapMarkers = [];

var bounds = {
    xmin: null,
    ymin: null,
    xmax: null,
    ymax: null
};

var condition = null;

var cardTemplate = '<div class="card" style="width: 100%; margin-bottom: 15px;"> \
        <div class="card-header"> \
            {0} \
            <ul class="list-group list-group-flush"> \
            <li class="list-group-item">{1}</li> \
            <li class="list-group-item">{2}</li> \
            <li class="list-group-item">{3}</li> \
            <li class="list-group-item">{4}</li> \
            </ul> \
        </div> \
    </div>';

function updatePtOnMap(json_data, update=null) {
    var srch_flag = 1;
    var bounds = [];
    var goe = [];

    for(var i = 0; i < mapMarkers.length; i++){
        mymap.removeLayer(mapMarkers[i]);
    }
    mapMarkers = [];
    $(".card-block").html("");

    try{
        goe = JSON.parse(json_data);
        var temp = goe['features'].length;
        $(".toggle-btn").addClass("srch-active");
    }catch(err) { 
        $(".toggle-btn").removeClass("srch-active");
        return;
    }

    search_res = ""
    for (var i=0; i < goe['features'].length; i++) {
        var item = goe['features'][i]['properties']
        var streetview = goe['features'][i]['streetview']

        bounds.push([goe['features'][i]['lat'], goe['features'][i]['lon']])

        var temp = '<div class="card bg-light mb-3" style="max-width: 100%;"> \
                <div class="card-header">'+item['project_no']+' - \
                <h5 class="card-title" style="display: inline;">'+item['client']+'</h5></div> \
                <img src="'+streetview+'" style="width: 100%;" /> \
                <div class="card-body" style="    margin-top: -100px;"> \
                <p class="card-text"> \
                    <div class="card-date">'+item['date']+'  &nbsp;&nbsp;&nbsp; \
                    '+item['survey_type'].toUpperCase()+'</div> \
                    <div>'+item['join_field']+' </div>\
                    <div class="card-link"><a href="'+item['folder_path']+'" target="_blank">'+item['folder_path']+'</a></div> \
                </p> \
                </div> \
            </div>';

        if (item['survey_type'] == "prad")
            temp = '<div class="card bg-light mb-3" style="max-width: 100%;"> \
                    <div class="card-header">'+item['project_no']+' - \
                    <h5 class="card-title" style="display: inline;">'+item['client']+'</h5></div> \
                    <img src="'+streetview+'" style="width: 100%;" /> \
                    <div class="card-body" > \
                    <p class="card-text"> \
                        <div class="card-date">'+item['date']+'  &nbsp;&nbsp;&nbsp; \
                        '+item['survey_type'].toUpperCase()+'</div> \
                        <div>'+item['address_street']+'</div> \
                        <div>'+item['join_field']+' </div>\
                        <div class="card-link"><a href="'+item['folder_path']+'" target="_blank">'+item['folder_path']+'</a></div> \
                    </p> \
                    </div> \
                </div>';
        search_res += temp;
    }
    $(".card-block").html(search_res);

    if (goe['features']) {
        if (update == null) {
            var polyline = L.polyline(bounds, {color: '#0000'}).addTo(mymap);

            mymap.fitBounds(polyline.getBounds());
        }

        L.geoJSON(goe, {
            pointToLayer: function (feature, latlng) {
                var marker = L.marker(latlng);
                marker.bindPopup("Project No: " + 
                    feature.properties.project_no + '<br/>' +
                    "Join Field: " + feature.properties.join_field);
                mapMarkers.push(marker);
                return marker; 
            }
        }).addTo(mymap);
    }
}

function ajaxMap(xmin, ymin, xmax, ymax) {
    $.ajax({
        method: "post",
        url: '/ajax-map-bound/',
        data: {xmin: xmin, ymin: ymin, xmax: xmax, ymax: ymax, condition: condition}
    }).done(function (res) {
        updatePtOnMap(JSON.stringify(res), true);
    });
}

function openMapWithId(form_id) {
    $.ajax({
        method: "post",
        url: '/ajax-map-formid/',
        data: {form_id: form_id}
    }).done(function (res) {
        updatePtOnMap(JSON.stringify(res));
        $(".map-mode").show();
        $(".list-mode").hide();

        $("#escalation_length").hide();
        $(".dataTables_scroll").hide();
        $("#escalation_info").hide();
        $("#escalation_paginate").hide();
    });
}

function initBase() {
    $('#escalation tfoot th').each( function () {
        var title = $(this).text();
        if (title == "Edit/Review") {
            $(this).html("");
        } else {
            $(this).html( '<input type="text" style="width: 100%"/>' );
        }
    } );

    postTable = $('#escalation').DataTable({
        "order": [[ 0, "desc" ]],
        "columnDefs": [
            { "className": "action-node", "targets": [ 19 ] }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/ajax_pagination/",
            "type": "POST",
            "data": function ( d ) {
                if (d.start == 0 && reload == 1)
                    reload = 2
                else if (d.start == 0 && reload == 2)
                    reload = null

                d.extra_search = JSON.stringify(bounds);
                d.reload = reload;

                if (d.start == 0 && reload == null){
                    bounds = {
                        xmin: null,
                        ymin: null,
                        xmax: null,
                        ymax: null
                    };
                }
            },
            "dataSrc": function ( json ) {
                searchText = json.search_text;
                if (json.geom != null && json.bounds == null) {
                    updatePtOnMap(json.geom);
                }
                condition = json.condition;
                return json.data;
            }       
        },
        "initComplete": function() {
            $('#escalation_filter input').unbind();
            $('#escalation_filter input').bind('keyup', function(e) {
                if(e.keyCode == 13) {
                    postTable.search(this.value).draw();
                }
            });
        },
        "scrollX": true
    });
    $('#usertable').DataTable();

    // Apply the search
    postTable.columns().every( function () {
        var that = this;
 
        $( 'input', this.footer() ).on( 'change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );

    var r = $('.dataTables_scrollFootInner table tfoot tr');
    var index = 0;
    r.find('th').each(function(){
        index += 1;
        var css = $(".dataTables_scrollHeadInner thead th:nth-child("+index.toString()+")").attr("style");

        $(this).attr('style', css + " padding: 2px;");
        $(this).children().css('padding', 0);
    });
    $('.dataTables_scrollHeadInner table thead').append(r);
    $('#search_0').css('text-align', 'center');

    setTimeout(function() {
        window.location.reload();
    }, 3610000);

    $(".toggle-btn").click(function(){
        $(".view-mode").toggle();

        if($(".map-view").attr("style") == "display: none;") {
            reload = 1;
            postTable.ajax.reload();

            $("#escalation_length").show();
            $(".dataTables_scroll").show();
            $("#escalation_info").show();
            $("#escalation_paginate").show();
        } else {
            $("#escalation_length").hide();
            $(".dataTables_scroll").hide();
            $("#escalation_info").hide();
            $("#escalation_paginate").hide();
        }
    })

    $(".excel-download").click(function(){
        var url = "/export/xls/?search=" + encodeURI(searchText) + "&extra_search=" + encodeURI(JSON.stringify(bounds));
        window.location = url;
    })
}