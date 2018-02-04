const svgW = 1200;
const svgH = 750;
const lvls = ['0', '1', '2', '3', 'sum'];
var usersData = false;

var mode = 'playPerUser'; // users, playPerUser, playcount

var modeData = {
  users: {
    legendText: 'No listeners [per 1M inhabitants]',
    colors: [
      '#ffffcc',
      '#ffeda0',
      '#fed976',
      '#feb24c',
      '#fd8d3c',
      '#fc4e2a',
      '#e31a1c',
      '#bd0026',
      '#800026'
    ],
    scaleExponent: 0.2
  },
  playcount: {
    legendText: 'Playcount [per 1M inhabitants]',
    colors: [
      '#ffffd9',
      '#edf8b1',
      '#c7e9b4',
      '#7fcdbb',
      '#41b6c4',
      '#1d91c0',
      '#225ea8',
      '#253494',
      '#081d58'
    ],
    scaleExponent: 0.2
  },
  playPerUser: {
    legendText: 'Playcount per one listener',
    colors: [
      '#f7fcb9',
      '#d9f0a3',
      '#addd8e',
      '#78c679',
      '#41ab5d',
      '#238443',
      '#006837',
      '#004529'
    ],
    scaleExponent: 1.3
  }
};
var colors = modeData[mode].colors;
var noDataColor = 'lightgrey';

const projection = d3
  .geoNaturalEarth2()
  .scale(200)
  .center([18, 10])
  .translate([svgW / 2, svgH / 2]);

const path = d3
  .geoPath()

  .projection(projection)
  .pointRadius(1.5);

var getColor = function(val, scale) {
  if (mode === 'playPerUser' && val === 0) {
    return noDataColor;
  }
  return colors[Math.floor(scale(val))];
};

var coeff = function(country, lvl) {
  var countryNames = [country.properties.admin, country.properties.NAME];
  var countryData = usersData[countryNames[0]];
  if (!countryData) {
    countryData = usersData[countryNames[1]];
  }

  if (countryData && country.properties.POP_EST > 10000) {
    if (mode === 'playPerUser') {
      if (countryData[lvl]['users'] > 0) {
        return countryData[lvl]['playcount'] / countryData[lvl]['users'];
      } else {
        return 0;
      }
    } else {
      return countryData[lvl][mode] / (country.properties.POP_EST / 1000000);
    }
  } else {
    return 0;
  }
};

//var mode = 'users';

d3.json('./../users/users_aggregated.json', function(data) {
  usersData = data;

  d3.json('./../countries.geojson', function(error, data) {
    var features = data.features;

    var getFeature = function(adminName) {
      return data.features.find(function(c) {
        return (
          c.properties.admin === adminName || c.properties.NAME === adminName
        );
      });
    };

    lvls.map(function(lvl) {
      var max = Math.max(
        ...Object.keys(usersData)
          .filter(function(c) {
            return c;
          })
          .map(function(adminName) {
            var country = getFeature(adminName);
            return country ? coeff(country, lvl) : 0;
          })
      );

      console.log(max);

      var scale = d3
        .scalePow()
        .exponent(modeData[mode]['scaleExponent'])
        .domain([0, max])
        .range([0, colors.length - 1]);

      var svg = d3
        .select('body')
        .append('svg')
        .attr('width', svgW)
        .attr('height', svgH);

      svg
        .selectAll('path')
        .data(data.features)
        .enter()
        .append('path')
        .attr('d', path)
        .style('fill', function(d) {
          if (d.properties.admin) {
            return getColor(coeff(d, lvl), scale);
          } else {
            return 'grey';
          }
        })
        .style('fill-opacity', 1)
        .style('stroke', 'grey')
        .style('stroke-opacity', 0.5);

      svg
        .append('rect')
        .attr('x', 50)
        .attr('y', 380)
        .attr('width', 240)
        .attr('height', 300)
        .style('fill', 'white')
        .style('stroke', 'black');

      var colorW = 40;
      var colorH = 20;
      var colorX = 30;
      var colorY = 30;
      var colorM = 7;

      var legendText = modeData[mode].legendText;

      svg
        .append('text')
        .attr('x', 70)
        .attr('y', 410)
        .text(legendText);

      colors.map(function(color, ci) {
        svg
          .append('rect')
          .attr('x', 50 + colorX)
          .attr('y', 400 + colorY + ci * (colorM + colorH))
          .attr('width', colorW)
          .attr('height', colorH)
          .style('fill', color);

        svg
          .append('text')
          .attr('x', 50 + colorX + colorW + colorM)
          .attr('y', 400 + colorY + ci * (colorM + colorH) + 15)
          .text('> ' + scale.invert(ci).toFixed(2));
      });
    });
  });

  // Draw each province as a path
});
