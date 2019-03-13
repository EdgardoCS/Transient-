//1000mt
// lat1 = -71.605397;
// lat2 = -71.616107;
// lng1 = -33.047957;
// lng2 = -33.047757;

// 100mt
// lat1 = -71.610647;
// lat2 = -71.609625;
// lng1 = -33.052773;
// lng2 = -33.052468;

//10mt
// lat1 = -71.619838;
// lat2 = -71.619942;
// lng1 = -33.045790;
// lng2 = -33.045767;

//5mt
// lat1 = -71.619109;
// lat2 = -71.619163;
// lng1 = -33.044832;
// lng2 = -33.044823;

//3mt
// lat1 = -71.619967;
// lat2 = -71.619998;
// lng1 = -33.044744;
// lng2 = -33.044739;
///////////////////////////////
//50mt
// lat1 = -71.619806;
// lat2 = -71.619270;
// lng1 = -33.044770;
// lng2 = -33.044812;
//60mt
// lat1 = -71.619667;
// lat2 = -71.619027;
// lng1 = -33.044785;
// lng2 = -33.044812;
//65mt
// lat1 = -71.617808;
// lat2 = -71.617111;
// lng1 = -33.044904;
// lng2 = -33.044918;
//40mt
// lat1 = -71.613787;
// lat2 = -71.614217;
// lng1 = -33.044986;
// lng2 = -33.044986;
//25mt
// lat1 = -71.610571;
// lat2 = -71.610301;
// lng1 = -33.044886;
// lng2 = -33.044885;
//1mt
// lat1 = -71.610545,
// lat2 = -71.610534;
// lng1 = -33.044905;
// lng2 = -33.044906;

const fs = require('fs')
const fileContents = fs.readFileSync('./data/example2.json', 'utf8')

try {
  const data = JSON.parse(fileContents)
  var features = data.source.data.features;
} catch (err) {
  console.error(err)
}

var lat1;
var lng1;
var link;
var typo;
var subtypo;
// var lat2 = -71.577339;
// var lng2 = -33.042782;

// var lat2 = -71.5771;
// var lng2 = -33.0432;

var lat2 = -71.5741;
var lng2 = -33.0435;

for (let u in features) {
  lat1 = features[u].geometry.coordinates[0];
  lng1 = features[u].geometry.coordinates[1];
  link = features[u].properties.image;
  typo = features[u].properties.typology;
  subtypo = features[u].properties.subTypology;
  getDistanceFromLatLonInKm(lat1, lat2, lng1, lng2);

}

function getDistanceFromLatLonInKm(lat1, lat2, lng1, lng2) {
  var R = 6378137; // Radius of the earth in m
  var dLat = deg2rad(lat2 - lat1); // deg2rad below
  var dLng = deg2rad(lng2 - lng1);
  var a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c; // Distance in m
  //console.log("distance in meters: " + d)

  var comparation = 10;
  var factor = comparation * 0.20;
  var diference = comparation + factor;

  if (d <= diference) {
    console.log("match in: " + lat1 + "," + lng2 + " with " + lat2 + "," + lng2);
    var realDistance = (d - (d * 0.10));
    console.log("approximately distance: " + realDistance + "m");
    console.log("type: " + typo + " subtype: " + subtypo);
    console.log("here: " + link);
  }
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}
