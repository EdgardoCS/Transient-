const fs = require('fs')

const file = fs.readFileSync('../../data/json/pscv-mena.json', 'utf8')

save_file = function (data) {
    fs.writeFile('../../data/json/newPscvMena.json', JSON.stringify(data), function (err) {
        if (err) {
            console.log(err);
        }
    });
}

try {
    const data = JSON.parse(file)
    console.log(data[0])
    var temp = data[0];
    var nuevo_genero;
    var nuevo_dm; 
    var nuevo_hta; 

    if (temp.datosPersonales.genero == 'F') {
        nuevo_genero = 'FEMENINO'
    } else if (temp.datosPersonales.genero == 'M') {
        nuevo_genero = 'MASCULINO'
    }
    if (temp.pscv.patologias.diabetesMellitus == 0){
        nuevo_dm = 'NO'
    }
    else if (temp.pscv.patologias.diabetesMellitus == 1){
        nuevo_dm = 'SI'
    }
    if (temp.pscv)
    

    var user_pscv_cormuval = {
        'index': temp.index,
        'datosPersonales': {
            'nombres': temp.datosPersonales.nombres,
            'apellido1': temp.datosPersonales.apellido1,
            'apellido2': temp.datosPersonales.apellido2,
            'genero': temp.datosPersonales.genero,
            'fechaNacimiento': temp.datosPersonales.fechaNacimiento
        },
        'documento': {
            'tipo': temp.documento.tipo,
            'numero': temp.documento.numero,
            'digitoVerificador': temp.documento.digitoVerificador
        },
        'direccion': {
            'numero': temp.direccion.numero,
            'calle': temp.direccion.calle,
            'ciudad': temp.direccion.ciudad,
            'pais': temp.direccion.pais
        },
        'sector': temp.sector,
        'geometry': {
            'type': temp.geometry.type,
            'coordinates': temp.geometry.coordinates
        },
        'telefonos': {
            'telefono1': temp.telefonos.telefono1,
            'telefono2': temp.telefonos.telefono2
        },
        'pscv': {
            'Cod': temp.index,
            'Rut': temp.documento.numero + '-' + temp.documento.digitoVerificador,
            'Nombre completo': temp.datosPersonales.nombres + ' ' + temp.datosPersonales.apellido1 + ' ' + temp.datosPersonales.apellido2,
            'Ficha': temp.pscv.numeroFicha,
            'Fecha_nac': temp.datosPersonales.fechaNacimiento,
            'Edad': 0,
            'Sexo': nuevo_genero,
            'Sector': temp.sctor,
            'Fecha_ingreso': temp.pscv.fechaIngreso,
            'Migrante': NaN,
            'Pueblos_originarios': NaN,
            'Telefonos': {
                'telefono1': temp.telefonos.telefono1,
                'telefono2': temp.telefonos.telefono2
            }, 
            'Fecha_ultimo_control': temp.pscv.fechaUltimoControl, 
            'Fecha_proximo_control': NaN, 
            'Estado_control': NaN, 
            'Comentario': NaN, 
            'Peso': NaN,
            'IMC': temp.pscv.estadoNutricional.imc, 
            'Estado_nutricional': NaN, 
            'RCV': temp.pscv.riesgoCardiovascular, 
            'DM': nuevo_dm, 
            'HTA': , 
            'Epilepsia': temp.pscv.patologias.epilepsia,
            'Dislipidemia': temp.pscv.patologias.dislipidemia, 
            'Tabaco': NaN, 
            'Artrosis': temp.pscv.patologias.artrosis, 
            'Parkinson': NaN, 
            'Hipotiroidismo': NaN, 




        }
    }
} catch (err) {
    console.log(err)
}