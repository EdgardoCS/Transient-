import time
import os


from PIL import Image, ExifTags

cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)


for i in range(1, 300):
    index = i
    #path = './img/G02-%g.jpg' % index
    try:
        path = '../../../capas_sistam/G01/IMG/G01-%g.jpg' % index
        counter = 0
        try:
            image = Image.open(path)
            print('editing...', path)
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in ExifTags.TAGS
            }
            print(exif)

            print('Orientation', exif['Orientation'])

            if exif['Orientation'] == 3:
                image = image.rotate(180, expand=True)
                print('image change', index)
            elif exif['Orientation'] == 6:
                image = image.rotate(270, expand=True)
                print('image change', index)
            elif exif['Orientation'] ==8:
                image = image.rotate(90, expand=True)
                print('image change', index)

            image.save(path)
            image.close()
            time.sleep(1)
            #except:
             #   print('no orientation field')
              #  pass
        except AttributeError:
            #print(AttributeError)
            #time.sleep(1)
            pass
    except:
        #print('file not found')
        pass