from PIL import Image
import os
import glob
import piexif
import sys

file_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/test.JPG"
# dir_path = "/Users/remileblanc/Dropbox/College/Nature Up North/test_pics/*"
dir_path = "/Users/remileblanc/Desktop/test_pics/*"
out_path = "/Users/remileblanc/Desktop/ResizedImages"
# out_path = "/Users/remileblanc/Dropbox/College/Nature Up North/ResizedImages"

target_size = 1000000

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

    exif_dict = piexif.load(img.info['exif'])
    cr = str.encode('Nature Up North')

    exif_dict['0th'][piexif.ImageIFD.Copyright] = cr
    exif_dict['1st'][piexif.ImageIFD.Copyright] = cr
    exif_bytes = piexif.dump(exif_dict)

    if size < target_size:
        img.save(old_file,exif=exif_bytes)
        continue
    while size >= target_size:
        width -= 1
        height -= 1
        # this method does not seem to work
        img = img.resize((width, height))
        # I dont want to save it every time, but i need to to get the size...
        img.save(new_file, exif=exif_bytes)
        size = os.path.getsize(new_file)
        print(size)
        print("size: ", sys.getsizeof(img))






