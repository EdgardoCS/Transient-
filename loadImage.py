import time

from PIL import Image, ExifTags

for i in range(1, 517):
    index = i
    path = './img/G01-%g.jpg' % index
    counter = 0

    try:
        image = Image.open(path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
            print('image change', index)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
            print('image change', index)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
            print('image change', index)
        image.save(path)
        image.close()
        time.sleep(1)

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
