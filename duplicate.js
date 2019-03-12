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
console.log("running"); 
// test
var lat1; 
var lng1; 

var lat2 = -71.578578;
var lng2 = -33.041823;

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
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

getDistanceFromLatLonInKm(lat1, lat2, lng1, lng2);
