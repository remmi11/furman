///////////////////////////////////////////////////
// original
///////////////////////////////////////////////////
function map_init(defaultPt) {
    L.mapbox.accessToken = 'pk.eyJ1Ijoid3RnZW9ncmFwaGVyIiwiYSI6ImNpdGFicWJqYjAwdzUydHM2M2g0MmhsYXAifQ.oO-MYNUC2tVeXa1xYbCIyw';

    var mbAttr = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

    var grayscale = L.tileLayer(mbUrl, { id: 'mapbox.light', attribution: mbAttr }),
        streets = L.tileLayer(mbUrl, { id: 'mapbox.streets', attribution: mbAttr })
    var satellite = L.mapbox.styleLayer('mapbox://styles/mapbox/satellite-streets-v9');

    var sections = L.mapbox.styleLayer('mapbox://styles/wtgeographer/cjf442uso0z3e2ss1w8jpnyp5');
    // var contours = L.mapbox.styleLayer('mapbox://styles/wtgeographer/cjf6xjfak3ebb2sobig2fnpzh');
    var prad = L.mapbox.styleLayer('mapbox://styles/wtgeographer/cjf75lnp62m612smws69qnu4o');
    var floods = L.mapbox.styleLayer('mapbox://styles/wtgeographer/cjf9riogz4z8n2rmk4eawkc6o');
    var places = L.mapbox.styleLayer('mapbox://styles/wtgeographer/cjftuokfx8ime2sqpyhj88q67');

    mymap = L.map('mapid', {
        center: [35.058104, -101.749877],
        zoom: 9,
        layers: [streets, sections] //, contours, prad, floods]
    });

    var baseLayers = {
        "Streets": streets,
        "Satellite": satellite
    };

    var overlays = {
        "Sections": sections,
        // "10ft Contours": contours,
        "Prad Lines": prad,
        "Flood Hazards": floods,
        "City Limits": places
    };

    L.control.layers(baseLayers, overlays).addTo(mymap);

    // var printer = L.easyPrint({
    //     sizeModes: ['Current', 'A4Landscape', 'A4Portrait'],
    //     filename: 'myMap',
    //     exportOnly: true,
    //     hideControlContainer: true
    // }).addTo(map);

    // function manualPrint() {
    //     printer.printMap('CurrentSize', 'MyManualPrint')
    // }

    mymap.on('dragend', function onDragEnd() {
        if (condition && $(".map-view").attr("style") != "display: none;") {
            ajaxMap(mymap.getBounds().getWest(), mymap.getBounds().getSouth(),
                mymap.getBounds().getEast(), mymap.getBounds().getNorth());

            bounds['xmin'] = mymap.getBounds().getWest();
            bounds['ymin'] = mymap.getBounds().getSouth();
            bounds['xmax'] = mymap.getBounds().getEast();
            bounds['ymax'] = mymap.getBounds().getNorth();
        }
    });

    mymap.on('zoomend', function () {
        if (condition && $(".map-view").attr("style") != "display: none;") {
            ajaxMap(mymap.getBounds().getWest(), mymap.getBounds().getSouth(),
                mymap.getBounds().getEast(), mymap.getBounds().getNorth());

            bounds['xmin'] = mymap.getBounds().getWest();
            bounds['ymin'] = mymap.getBounds().getSouth();
            bounds['xmax'] = mymap.getBounds().getEast();
            bounds['ymax'] = mymap.getBounds().getNorth();
        }
    });
}