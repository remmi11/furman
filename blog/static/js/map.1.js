
function map_init(defaultPt) {
    mymap = L.map('mapid').setView(defaultPt, 10);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mymap);

    mymap.on('dragend', function onDragEnd(){
        if (condition && $(".map-view").attr("style") != "display: none;") {
            ajaxMap(mymap.getBounds().getWest(), mymap.getBounds().getSouth(),
                mymap.getBounds().getEast(), mymap.getBounds().getNorth());

            bounds['xmin'] = mymap.getBounds().getWest();
            bounds['ymin'] = mymap.getBounds().getSouth();
            bounds['xmax'] = mymap.getBounds().getEast();
            bounds['ymax'] = mymap.getBounds().getNorth();
        }
    });

    mymap.on('zoomend', function() {
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