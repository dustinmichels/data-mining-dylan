// Load JSON
$.getJSON("info.geojson", function (data) {
    placesGroup = makeMap(data);
    initSelector(placesGroup);
});

// --------------------------------------------------------
// MAP MAKING

const makeMap = (data) => {
    // Create map, tileLayer, activeGroup
    let map = L.map('map', { center: [20, -30], zoom: 2 });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let activeGroup = L.featureGroup([]).addTo(map);

    // To turn points into circleMarkers
    const scale = d3.scaleSqrt().domain([1, 6]).range([4, 10]);
    const placeRadius = (place) => scale(place.properties.cnt);
    const circleOptions = {
        fillColor: "#ff7800", color: "#000", weight: 1,
        opacity: 1, fillOpacity: 0.7
    };
    const pointToLayer = (feature, latlng) => {
        let circleMakerOptions = Object.assign({ radius: placeRadius(feature) }, circleOptions);
        return L.circleMarker(latlng, circleMakerOptions);
    };

    // On click circleMaker
    const onEachFeature = (feature, layer) => {
        // Add popup
        let props = feature.properties;
        layer.bindPopup(
            `<b>${props.name}</b>, ${props.cnt} mention(s)<br>`
        );
        // Send text to div
        layer.on("click", function (e) {
            console.log(e);
            let props = e.target.feature.properties;
            let text = (
                `${props.name}: ${props.cnt} mention(s)<br><i>Appears in: </i>${props.songs.join(', ')}`
            );
            $("#info-inner").html(text);
            $("#city-select").val(e.target._leaflet_id).change();

            // Color change
            let opts = { ...e.target.options };
            opts.fillColor = 'red';
            activeGroup.clearLayers();
            activeGroup.addLayer(L.circleMarker(e.latlng, opts)).addTo(map);
        })
    }

    // Add geoJSON data to map
    let placesGroup = L.geoJson(data, {
        pointToLayer: pointToLayer,
        onEachFeature: onEachFeature
    }).addTo(map);
    return placesGroup
}

// --------------------------------------------------------
// INITIALIZE SELECTOR
function initSelector(placesGroup) {

    let layersArray = placesGroup.getLayers()
    let $el = $("#city-select");

    $el.empty();
    $.each(layersArray, function (idx, layer) {
        let name = layer.feature.properties.name;
        let id = layer._leaflet_id;
        $el.append($("<option></option>")
            .attr("value", id).text(name));
    });

    $el.on('change', function (e) {
        let id = $(this).val();
        let layer = placesGroup.getLayer(id);
        // layer.fireEvent('click');
    });
}
