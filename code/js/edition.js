const fs = require('fs')

const file1 = fs.readFileSync('../../data/geo/nueva_capa_transversal(point).json', 'utf8')

save_file = function (data1) {
    fs.writeFile("../../data/geo/capa_transversal(point).json", JSON.stringify(data1), function (err) {
        if (err) {
            console.log(err);
        }
    });
}

try {
    const data1 = JSON.parse(file1)
    let feats = data1.features;

    for (let u in feats) {
        link = feats[u].properties.FOTO_LNK

        if (link !== null && link.includes('<a href=') || link.includes('<ahref=')) {
            _link = link.split('>')
            __link = _link[1].split('<')
            //console.log(__link[0])
            data1.features[u].properties.FOTO_LNK = __link[0];
        }
    }
    save_file(data1)
    console.log("done")

} catch (err) {
    console.error(err)
}