const svgW = 900;
const svgH = 400;

const projection = d3
  .geoNaturalEarth2()
  .scale(200)
  .center([20, 20])
  .translate([svgW / 2, svgH / 2]);

const path = d3
  .geoPath()
  .projection(projection)
  .pointRadius(1.5);

var color = d3.scaleSequential(function(d) {
  return d3.interpolateRainbow(d);
});

console.log(color(0.5));
console.log(color(1));

d3.tsv('./../../analyses/output/agglomerations.csv', function(pcaData) {
  console.log(pcaData);

  d3.json('./../../data/countries.geojson', function(error, data) {
    var features = data.features;

    ['0.05', '0.10', '0.15', '0.20', '0.25', '0.30'].map(function(w) {
      const noGroups = Math.max.apply(
        null,
        pcaData.map(function(r) {
          return r[w];
        })
      );

      const svg = d3
        .select('body')
        .append('svg')
        .attr('width', svgW)
        .attr('class', 'world')
        .attr('height', svgH);

      svg
        .selectAll('path')
        .data(features)
        .enter()
        .append('path')
        .attr('d', path)
        .style('fill', function(d) {
          const row = pcaData.find(function(pcaRow) {
            const countryName = pcaRow['tag name'];
            return countryName === d.properties.admin;
          });
          if (row) {
            return color(row[w] / noGroups); //
          } else {
            return 'lightgrey';
          }
        })
        .style('fill-opacity', 0.4)
        .style('stroke', 'grey')
        .style('stroke-opacity', 0.7)
        .attr('id', function(d) {
          return d.properties.admin;
        });
    });
    // Draw each province as a path
  });
});
