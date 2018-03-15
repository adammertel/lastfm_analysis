const svgW = 1500;
const svgH = 1000;

window.svg = d3
  .select('body')
  .append('svg')
  .attr('width', svgW)
  .attr('height', svgH);

const projection = d3
  .geoNaturalEarth2()
  .scale(400)
  .center([18, 10])
  .translate([svgW / 2, svgH / 2]);

const path = d3
  .geoPath()
  .projection(projection)
  .pointRadius(1.5);

colors = [
  '#e41a1c',
  '#377eb8',
  '#4daf4a',
  '#984ea3',
  '#ff7f00',
  '#ffff33',
  '#a65628',
  '#f781bf',
  '#999999'
];

d3.tsv('./../tags/outputs/pca.csv', function(pcaData) {
  console.log(pcaData);

  d3.json('./../countries.geojson', function(error, data) {
    var features = data.features;

    // Draw each province as a path
    svg
      .selectAll('path')
      .data(data.features)
      .enter()
      .append('path')
      .attr('d', path)
      .style('fill', function(d) {
        const row = pcaData.find(function(pcaRow) {
          return pcaRow[''] === d.properties.admin;
        });
        if (row) {
          return colors[parseInt(row.clusters_ms, 10)]; //
        } else {
          return 'lightgrey';
        }
      })
      .style('fill-opacity', 0.4)
      .style('stroke', 'grey')
      .style('stroke-opacity', 0.7);
  });
});
