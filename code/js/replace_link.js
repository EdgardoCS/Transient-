const fs = require('fs')
// const path = '/../../../capas_sistam/';

const file1 = fs.readFileSync('../../data/geo/LEV_CAPAUNICA_CONSTRUCCION.geojson', 'utf8')
const file2 = fs.readFileSync('../../data/geo/levantamiento_completo.json', 'utf8')

save_file = function (data1) {
    fs.writeFile("../../data/geo/capa_transversal.json", JSON.stringify(data1), function (err) {
        if (err) {
            console.log(err);
        }
    });
}

try {
    const data1 = JSON.parse(file1)
    const data2 = JSON.parse(file2)

    feats = data1.features;
    img = data2['Hoja 1'];

    for (let i in feats) {
        let id = feats[i].properties.ID_FINAL;
        // let temp_photo = feats[i].properties.FOTO_LNK;
        // let photo = temp_photo.split('"')[1]
        let layer = feats[i].properties.layer.split("_")[0];

        for (let u in img) {
            var target_id = img[u].id.split('-')[1].split('.')[0]
            var target_link = img[u].link
            var target_sector = img[u].sector;

            if (target_sector == layer) {
                if (id == target_id) {
                    data1.features[i].properties.FOTO_LNK = target_link;
                    console.log('match at ' + i)
                }
            }
        }
    }
    save_file(data1)
} catch (err) {
    console.error(err)
}