from PIL import Image, ImageEnhance
import os
import glob
import piexif


file_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/test.JPG"
dir_path = "/Users/remileblanc/Desktop/test_pics/*"
out_path = "/Users/remileblanc/Desktop/ResizedImages"

target_size = 1000000

# get all images in folder
images = glob.glob(dir_path)

# insert a tmp file while the images are being resized

for image in images:
    try:
        img = Image.open(image)

        width, height = img.size
        size = os.path.getsize(img.filename)
        outfile = os.path.splitext(out_path+'/'+os.path.basename(os.path.normpath(img.filename)))[0] + "_resized"
        extension = os.path.splitext(img.filename)[1]
        new_file = outfile + extension
        old_file = new_file.replace('_resized', '')

        try:
            exif_dict = piexif.load(img.filename)
            cr = str.encode('Nature Up North')
            exif_dict['0th'][piexif.ImageIFD.Copyright] = cr
            exif_dict['1st'][piexif.ImageIFD.Copyright] = cr
            # common error in exif data
            exif_dict['Exif'][37380] = (0,1)
            exif_bytes = piexif.dump(exif_dict)
        except IOError:
            print("Exif data is improperly formatted by camera.")

        if size < target_size:
            img.save(old_file, exif=exif_bytes)
            continue
        # just saving the image makes it smaller
        quality = 75
        img.save(new_file)

        # decreasing the pixels
        while size >= target_size:
            # decrease resolution
            width -= 100
            height -= 100
            img = img.resize((width, height))
            # optimize image and decrease size
            img.save(new_file, optimize=True, exif=exif_bytes)
            size = os.path.getsize(new_file)
            print(size)

        # decreases quality of image on a scale from 1 (worst) to 95 (best). The default is 75.
        # while size >= target_size:
        #     quality -= 5
        #     img.save(new_file, optimize=True, exif=exif_bytes, quality=quality)
        #     size = os.path.getsize(new_file)

        # decrease sharpness of image
        # factor = 1.0 # default
        # sharpen = ImageEnhance.Sharpness(img)
        # while size >= target_size:
        #     factor -= 0.1
        #     img = sharpen.enhance(factor)
        #     img.save(new_file, optimize=True, exif=exif_bytes)
        #     size = os.path.getsize(new_file)
        #     print(size)

        # decrease brightness of image
        # factor = 1.0 # default
        # brighten = ImageEnhance.Brightness(img)
        # while size >= target_size:
        #     factor -= 0.1
        #     img = brighten.enhance(factor)
        #     img.save(new_file, optimize=True, exif=exif_bytes)
        #     size = os.path.getsize(new_file)
        #     print(size)

        # # decrease contrast of image
        # factor = 1.0 # default
        # contrast = ImageEnhance.Contrast(img)
        # while size >= target_size:
        #     factor -= 0.1
        #     img = contrast.enhance(factor)
        #     img.save(new_file, optimize=True, exif=exif_bytes)
        #     size = os.path.getsize(new_file)
        #     print(size)


    except Exception as e:
        print('Failure whilst processing "' + img.filename + '": ' + str(e))

# delete the tmp file after the images have been resized
