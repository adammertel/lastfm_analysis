var state = {
  selectedCountry: false,
};
var countries;
var countriesImport;
var map;

var scale = d3.scalePow().exponent(1 / Math.E);
var color = d3.scaleSequential(function (d) {
  return d3.interpolateYlOrRd(scale(d));
});

/*
console.log(color(0));
console.log(color(0.5));
console.log(color(8));
console.log(color(10));
console.log(color(150));
*/
var countriesJson = false;

var fillCountry = function (f) {
  if (!state.selectedCountry) {
    return "grey";
  } else {
    var iso = f.properties.ISO_A2;
    var name = f.properties.admin;
    var value = countriesImport[state.selectedCountry][iso];
    if (value) {
      return color(value / state.max);
    } else {
      return "lightgrey";
      //return color(0);
    }
  }
};

$(document).ready(function () {
  map = L.map("map").setView([20, 0], 3);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  $.getJSON("./../../data/countries_import.json", function (importData) {
    countriesImport = importData;

    $.getJSON("./../../data/countries_full.geojson", function (countriesData) {
      countries = jQuery.extend(true, {}, countriesData);
      countries.features = [];
      countriesData.features.map(function (c) {
        if (countriesImport[c.properties.admin]) {
          countries.features.push(c);
        }
      });

      refresh();
    });
  });
});

var drawCountries = function () {
  if (countriesJson) {
    countriesJson.clearLayers();
  }
  countriesJson = L.geoJSON(countries.features, {
    style: function (f) {
      return {
        color: "black",
        weight: 2,
        fillColor: fillCountry(f),
        fillOpacity: 0.8,
      };
    },
    onEachFeature: function (f, l) {
      l.on("click", function (e) {
        var newSelection = e.target.feature.properties.admin;
        setState({
          selectedCountry: newSelection,
          max: Math.max.apply(
            null,
            Object.values(countriesImport[newSelection])
          ),
        });
      });
    },
  }).addTo(map);
};

var setState = function (newState) {
  console.log(newState);
  Object.keys(newState).map(function (newStateKey) {
    state[newStateKey] = newState[newStateKey];
  });
  refresh();
};

var refresh = function () {
  drawCountries();
};
