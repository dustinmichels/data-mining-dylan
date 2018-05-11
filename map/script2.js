class MapWidget {
    constructor(data) {

        this.map = L.map('map', { center: [20, -30], zoom: 2 });

        this.tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        this.activeGroup = L.featureGroup([]).addTo(this.map);

        // Add geoJSON data to map
        this.placesGroup = L.geoJson(data, {
            pointToLayer: this.makePointToLayerFcn(),
            onEachFeature: this.onEachFeature
        }).addTo(this.map);
    }

    makePointToLayerFcn() {
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
        return pointToLayer;
    }

    onEachFeature(feature, layer) {
        // Add popup
        let props = feature.properties;
        layer.bindPopup(
            `<b>${props.name}</b>, ${props.cnt} mention(s)<br>
                <i>Appears in: </i>${props.songs.join(', ')}`
        );
        // Send text to div
        layer.on("click", function (e) {
            console.log(e);
            let props = e.target.feature.properties;
            let text = (
                `${props.name}: ${props.cnt} mention(s)<br>
                        <i>Appears in: </i>${props.songs.join(', ')}`
            );
            // console.log(text);
            $("#info-inner").html(text);
            // $("#city-select").val(e.target._leaflet_id).change();
        })
        // Color change
        // let opts = { ...e.layer.options };
        // opts.fillColor = 'red';
        // activeGroup.clearLayers();
        // activeGroup.addLayer(L.circleMarker(e.latlng, opts)).addTo(map);
    }
}

$.getJSON("places.geojson", function (geodata) {
    // console.log(geodata);
    const mapWidget = new MapWidget(geodata);
});