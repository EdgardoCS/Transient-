const fs = require('fs')
const fileContents = fs.readFileSync('../../../capas_sistam/G01/GEOJSON/G01_SECTORESPERANZA.geojson', 'utf8')

try {
    const data = JSON.parse(fileContents)
    feats = data.features;
    for (let i in feats) {
        // console.log(feats[i])
        let photo = feats[i].properties.FOTO_LNK; 
        console.log(photo); 

    }
} catch (err) {
    console.error(err)
}