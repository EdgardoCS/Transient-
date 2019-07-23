const fs = require('fs')
// const path = '/../../../capas_sistam/';

const file1 = fs.readFileSync('../../data/geo/LEVANTAMIENTO COMPLETO_V3.geojson', 'utf8')
const file2 = fs.readFileSync('../../data/geo/localization.json', 'utf8')

save_file = function (data1) {
    fs.writeFile("../../data/geo/nueva_capa_transversal(point).json", JSON.stringify(data1), function (err) {
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
        // let id = feats[i].properties.ID_FINAL;
        // let temp_photo = feats[i].properties.FOTO_LNK;
        // let photo = temp_photo.split('"')[1]
        var id = feats[i].properties.Descriptio;
        if (id) {
            if (id.includes('ID:')) {
                var id_ = id.split(':')[1]
                console.log(id)
            }
        }
        if (feats[i].properties.layer != null) {
            let layer = feats[i].properties.layer.split("_")[0];
            for (let u in img) {
                var target_id = img[u].id.split('-')[1].split('.')[0]
                var target_link = img[u].link
                var target_sector = img[u].sector;
                if (target_sector == layer) {
                    if (id_ == target_id) {
                        data1.features[i].properties.FOTO_LNK = target_link;
                        console.log('match at ' + i)
                    }
                }
            }
        }
    }
    save_file(data1)
} catch (err) {
    console.error(err)
}