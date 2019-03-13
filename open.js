const fs = require('fs')
const fileContents = fs.readFileSync('./data/example2.json', 'utf8')

try {
  const data = JSON.parse(fileContents)
  var features = data.source.data.features;
  console.log(features)
} catch(err) {
  console.error(err)
}
