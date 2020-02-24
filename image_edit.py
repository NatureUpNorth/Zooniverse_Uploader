from PIL import Image
import os
import glob
import time
import csv
import shutil
from panoptes_client import Panoptes, Project, SubjectSet, Subject

dir_path = "/Users/remileblanc/Desktop/test_pics/*"
out_path = "/Users/remileblanc/Desktop/ResizedImages"
path = "/Users/remileblanc/Desktop/ResizedImages/*"
logfile = "/Users/remileblanc/Desktop/log.txt"
errorfiles = "/Users/remileblanc/Desktop/ErrorFiles/"
completed_images = "/Users/remileblanc/Desktop/completed_images"

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
            f = open(logfile, "a")
            t = time.localtime()
            f.write('\nFailure whilst processing "' + image + '": ' + str(e)+ " " + time.strftime("%D:%H:%M:%S",t)+'\n\n')
            f.close()
            # move error files into seperate folder
            os.rename(image, errorfiles + os.path.basename(os.path.normpath(image)))

# delete the tmp file after the images have been resized

try:
    Panoptes.connect(username='', password='')
    project = Project.find("6307")
except Exception as e:
    f = open(logfile, "a")
    t = time.localtime()

    f.write('Unable to connect to Zooniverse: '+time.strftime("%D:%H:%M:%S",t)+'\n')
    f.close()


subject_set = SubjectSet()
s = Subject()

subject_set.links.project = project
subject_set.display_name = 'Tutorial subject set 2'

images = glob.glob(path)
new_subjects = []

for img in images:
    try:
        s = Subject()
        s.links.project = project
        # manifest file
        if os.path.splitext(img)[1] == ".csv":
            # move csv to complete images folder
            shutil.copy(f, completed_images)
            # make dict out of csv file for upload
            manifest = csv.DictReader(open(img))
            s.metadata.update(manifest)
        else:
            # upload image to subject
            s.add_location(img)
            s.save()
            new_subjects.append(s)
    except Exception as e:
        f = open(logfile, "a")
        t = time.localtime()
        # move error files into seperate folder
        os.rename(img, errorfiles + os.path.basename(os.path.normpath(img)))
        f.write('Unable to upload ' + img + ': ' + str(e) + ' '+time.strftime("%D:%H:%M:%S", t)+'\n\n')
        f.close()

try:
    # add subjects to subject set
    subject_set.save()
    subject_set.add(new_subjects)
except Exception as e:
    f = open(logfile, "a")
    t = time.localtime()
    f.write('Unable to save subject set: ' + str(e) + ' '+time.strftime("%D:%H:%M:%S", t)+'\n\n')
    f.close()


# move uploaded images out of original folder to archive
og_images = glob.glob(dir_path)
for img in og_images:
    os.rename(img, completed_images+'/'+os.path.basename(os.path.normpath(img)))


# once upload to zooniverse is complete, delete resized images
for img in images:
    try:
        os.remove(img)
    except:
        # file was already moved out of directory, likely due to it causing an error
        pass


