$(document).ready(function () {

  // Load Map
  const map = initMap();
  const activeGroup = L.featureGroup([]).addTo(map);

  // Load geojson data
  $.getJSON("places.geojson", function (data) {
    const placesGroup = addPlaces(map, data);
    initSelector(placesGroup);
  });
})

// --------------------------------------------------------
// Create map, tileLayer, activeGroup
const initMap = () => {
  let map = L.map('map', { center: [20, -30], zoom: 2, });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  // let activeGroup = L.featureGroup([]).addTo(map);
  return map;
}

// --------------------------------------------------------
// Add places to map, using geoJSON file
const addPlaces = (map, data) => {
  // pointToLayer
  const scale = d3.scaleSqrt().domain([1, 6]).range([4, 10]);
  const placeRadius = (place) => scale(place.properties.cnt);
  const circleOptions = {
    fillColor: "#ff7800", color: "#000", weight: 1,
    opacity: 1, fillOpacity: 0.7
  };
  const pointToLayer = (feature, latlng) => {
    const circleMakerOptions = Object.assign({ radius: placeRadius(feature) }, circleOptions);
    return L.circleMarker(latlng, circleMakerOptions);
  };

  // On click circleMaker
  function onEachFeature(feature, layer) {
    // Add popup
    const props = feature.properties;
    layer.bindPopup(
      `<b>${props.name}</b>, ${props.cnt} mention(s)<br>`
    );

    // Update selector on click
    layer.on("click", function (e) {
      $("#city-select").val(e.target._leaflet_id).change();
    });
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

  $el.on('change', function (e) {
    let leaflet_id = $(this).val();
    let layer = placesGroup.getLayer(leaflet_id);
    updateView(layer);
  });

  $el.empty();
  $.each(layersArray, function (idx, layer) {
    let id = layer._leaflet_id;
    let props = layer.feature.properties;
    $el.append($("<option></option>")
      .attr("value", id).text(`${props.name}, ${props.cnt}`));
  });

  $el.change();
}

// --------------------------------------------------------
// Updaters
const updateView = (layer) => {
  console.log("update view");
  console.log(layer);
  restyleLayer(layer);
  updateDiv(layer);
}

const updateLyrics = (props, i) => {

  const makeLyricsElement = (lyrics, place) => {
    let start = lyrics.search(place);
    let end = start + place.length;
    return $('<p>')
      .addClass("is-size-7")
      .append(
        '...' + lyrics.slice(start - 100, start),
        $('<b>').text(place),
       lyrics.slice(end, end + 100) + '...'
      )
  }

  let text = makeLyricsElement(props.lyrics[i], props.name);
  // console.log(text);

  let lyricsEl = $("#info-inner2").html(text);
  // lyricsEl.html(lyricsEl.html().replace(/\n/g, '/'));
  lyricsEl.html(lyricsEl.html().replace(/\n/g,'<br/>'));
}

const updateDiv = (layer) => {
  console.log("update div");
  let props = layer.feature.properties;
  let text = (
    `${props.name}: ${props.cnt} mention(s)`
  );
  let songList = $('<ul/>');

  $.each(props.songs, function (i, song) {
    let li = $('<li/>')
      .addClass('ui-menu-item')
      .attr('role', 'menuitem')
      .appendTo(songList);
    let aaa = $('<a/>')
      .addClass('ui-all')
      .text(song)
      .appendTo(li)
      .click(function () {
        updateLyrics(props, i)
      });
    console.log(songList);
  })

  $("#info-inner").html(songList);
}

const restyleLayer = (layer) => {
  console.log("restyle");
  layer.openPopup();
  // Color change
  // let opts = { ...layer.options };
  // opts.fillColor = 'red';
  // activeGroup.clearLayers();
  // activeGroup.addLayer(L.circleMarker(e.latlng, opts)).addTo(map);
}
