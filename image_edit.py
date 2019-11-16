from PIL import Image
import os
import glob

file_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/test.JPG"
dir_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/*"
out_path = "/Users/remileblanc/Dropbox/College/Nature Up North/ResizedImages"


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
    print(new_file)
    while size >= target_size:
        print("too big: " + str(size))
        width -= 1
        height -= 1
        img = img.resize((width, height))
        img.save(new_file)
        try:
            img_resized = Image.open(new_file)
        except IOError:
            print("unable to open image {}".format(img_resized))
        size = os.path.getsize(img_resized.filename)






