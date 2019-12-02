from PIL import Image
import os
import glob
import piexif


file_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/test.JPG"
dir_path = "/Users/remileblanc/Desktop/test_pics/*"
out_path = "/Users/remileblanc/Desktop/ResizedImages"

target_size = 1000000

# get all images in folder
images = glob.glob(dir_path)

for image in images:
    try:
        img = Image.open(image)
    except IOError:
        print("unable to open image {}".format(img))
    width, height = img.size
    size = os.path.getsize(img.filename)
    outfile = os.path.splitext(out_path+'/'+os.path.basename(os.path.normpath(img.filename)))[0] + "_resized"
    extension = os.path.splitext(img.filename)[1]
    new_file = outfile + extension
    old_file = new_file.replace('_resized', '')

    exif_dict = piexif.load(img.filename)
    cr = str.encode('Nature Up North')

    exif_dict['0th'][piexif.ImageIFD.Copyright] = cr
    exif_dict['1st'][piexif.ImageIFD.Copyright] = cr
    print(exif_dict)

    # common error is some game camera images
    try:
        exif_dict['Exif'][37380] = (0,1)
    except:
        pass

    try:
        exif_bytes = piexif.dump(exif_dict)
    except:
        print("Exif data is improperly formatted by camera.")

    if size < target_size:
        img.save(old_file, exif=exif_bytes)
        continue
    # just saving the image makes it smaller
    img.save(new_file)
    while size >= target_size:
        # decrease resolution
        width -= 100
        height -= 100
        img = img.resize((width,height))
        # optimize image and decrease the resolution
        img.save(new_file, optimize=True, exif=exif_bytes)
        size = os.path.getsize(new_file)
