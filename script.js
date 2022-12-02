var markdown = require("markdown").markdown;

let vm = new Vue({
  el: '#map-widget',
  data: {
    map: null,
    geoData: null,
    tileLayer: null,
    features: null,
    currCityId: null,
    currSongIdx: 0,
    modalHTML: '',
    showModal: false,
  },
  computed: {
    currCity: function () {
      if (!this.geoData) { return { name: null, cnt: null, id: null, lyrics: [], songs: [] } }
      const place = this.geoData.find(feat => feat.properties.id === this.currCityId);
      return place.properties;
    },
    currLyricsHTML: function () {
      if (!this.geoData) { return 'No data!' }
      const lyrics = this.currCity.lyrics[this.currSongIdx];
      const re = new RegExp(this.currCity.name, "g");
      $el = $('<p>').append(lyrics);
      $el.html($el.html().replace(re, '<span class="has-background-warning">$&</span>'));
      $el.html($el.html().replace(/\n/g, '<br/>'));
      return $el.html();
    }
  },
  mounted() {
    this.initMap();
    $.getJSON("data/places.geojson", (geojson) => {
      this.geoData = geojson;
      this.currCityId = this.geoData[0].properties.id;
      this.initFeatures();
    });
    $.get("data/about_places.md", (input) => {
      const result = markdown.toHTML(input);
      console.log('loaded..');
      this.modalHTML = result;
    }, 'text');
  },
  watch: {
    currCityId: function (id) {
      const layers = this.features.getLayers();
      const selLayer = layers.find(layer => layer.feature.properties.id === id);
      selLayer.openPopup();
      this.currSongIdx = 0;
    },
  },
  methods: {
    initMap() {
      this.map = L.map('map', { center: [20, -30], zoom: 2, });
      this.tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
    },

    initFeatures() {
      this.features = L.geoJson(this.geoData, {
        pointToLayer: (feature, latlng) => {
          const circleOptions = { fillColor: "#ff7800", color: "#000", weight: 1, opacity: 1, fillOpacity: 0.6 };
          const scale = d3.scaleSqrt().domain([1, 6]).range([4, 10]);
          const placeRadius = (place) => scale(place.properties.cnt);
          const circleMakerOptions = Object.assign(
            { radius: placeRadius(feature) }, circleOptions);
          return L.circleMarker(latlng, circleMakerOptions);
        },
        onEachFeature: (feature, layer) => {
          layer.bindPopup(`<b>${feature.properties.name}</b>, ${feature.properties.cnt} mention(s)<br>`);
          layer.on("click", (e) => {
            this.currCityId = e.target.feature.properties.id;
          });
        }
      }).addTo(this.map);
    },


    initLayers() {
      this.layers.forEach((layer) => {
        const markerFeatures = layer.features.filter(feature => feature.type === 'marker');
        const polygonFeatures = layer.features.filter(feature => feature.type === 'polygon');

        markerFeatures.forEach((feature) => {
          feature.leafletObject = L.marker(feature.coords)
        });

        polygonFeatures.forEach((feature) => {
          feature.leafletObject = L.polygon(feature.coords)
            .bindPopup(feature.name);
        });

      });
    },
    layerChanged(layerId, active) {
      const layer = this.layers.find(layer => layer.id === layerId);
      layer.features.forEach((feature) => {
        if (active) {
          feature.leafletObject.addTo(this.map);
        } else {
          feature.leafletObject.removeFrom(this.map);
        }
      });
    },
  },
});
