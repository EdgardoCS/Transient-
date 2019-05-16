const fs = require('fs');
const http = require('https');
var ExifImage = require('exif').ExifImage;

// const hostname = '127.0.0.1';
// const port = 3000;

// const server = http.createServer((req, res) => {
//   res.statusCode = 200;
// });

// server.listen(port, hostname, () => {
//   console.log(`Server running at http://${hostname}:${port}/`);
// });


const fileContents = fs.readFileSync('./img/G01-271.jpg')

try {
  new ExifImage({
    image: fileContents
  }, function (error, exifData) {
    if (error)
      console.log('Error: ' + error.message);
    else
      // console.log(exifData); // Do something with your data!
      var orientation = exifData.image.Orientation;
    if (
      orientation != 1 &&
      orientation != undefined &&
      orientation != 0
    ) {
      console.log("imagen volteada");
      orientation = 1;
    } else {
      console.log("imagen en posicion");
    }
    saveImage(exifData)
  });

} catch (error) {}

function saveImage(options){
}
