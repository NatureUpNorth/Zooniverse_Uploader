from PIL import Image
import os
import glob
import time
from panoptes_client import Panoptes, Project, SubjectSet, Subject


file_path = "/Users/remileblanc/Dropbox/College/Nature Up North/Opossum/test.JPG"
dir_path = "/Users/remileblanc/Desktop/test_pics/*"
out_path = "/Users/remileblanc/Desktop/ResizedImages"
path = "/Users/remileblanc/Desktop/ResizedImages/*"

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

        if size < target_size:
            img.save(old_file)
            continue
        # just saving the image makes it smaller
        quality = 75
        img.save(new_file)

        # decreases quality of image on a scale from 1 (worst) to 95 (best). The default is 75.
        while size >= target_size and quality >= 40:
            quality -= 5
            img.save(new_file, optimize=True, quality=quality)
            size = os.path.getsize(new_file)

        # decreasing the pixels
        while size >= target_size:
            # decrease resolution
            width -= 100
            height -= 100
            img = img.resize((width, height))
            # optimize image and decrease size
            img.save(new_file, optimize=True)
            size = os.path.getsize(new_file)

    except Exception as e:
        # print('Failure whilst processing "' + img.filename + '": ' + str(e))
        if os.path.splitext(image)[1] == ".csv":
            os.rename(image, out_path+'/'+os.path.basename(os.path.normpath(image)))

        else:
            f = open("/Users/remileblanc/Desktop/log.txt", "a")
            t = time.localtime()

            f.write('\nFailure whilst processing "' + image + '": ' + str(e)+ " " + time.strftime("%D:%H:%M:%S",t))
            f.close()
# delete the tmp file after the images have been resized

Panoptes.connect(username='natureupnorth@gmail.com', password='NatureRocks4')

project = Project.find("6307")
print(project.display_name)

subject_set = SubjectSet()
s = Subject()

subject_set.links.project = project
subject_set.display_name = 'Tutorial subject set 2'

images = glob.glob(path)
new_subjects = []

for img in images:
    print(img)
    s = Subject()
    s.links.project = project
    # if os.path.splitext(img)[1] == ".csv":
    #     s.metadata.update(img)
    # else:
    s.add_location(img)
    s.save()
    new_subjects.append(s)
subject_set.save()
subject_set.add(new_subjects)

# once upload to zooniverse is complete, delete resized images
for img in images:
    os.remove(img)

# move uploaded images out of original folder to archive
og_images = glob.glob(dir_path)
completed_images = "/Users/remileblanc/Desktop/completed_images/"
for img in og_images:
    os.rename(img, completed_images+os.path.basename(os.path.normpath(img)))

