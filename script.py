from panoptes_client import Panoptes, Project, SubjectSet, Subject
import dropbox
import glob

path = "/Users/remileblanc/Desktop/ResizedImages/*"

Panoptes.connect(username='', password='')

project = Project.find("6307")
print(project.display_name)

for workflow in project.links.workflows:
    print(workflow.display_name)

subject_set = SubjectSet()
s = Subject()

subject_set.links.project = project
subject_set.display_name = 'Tutorial subject set 6'

images = glob.glob(path)
new_subjects = []

for img in images:
    s = Subject()
    s.links.project = project
    s.add_location(img)
    s.save()
    new_subjects.append(s)
subject_set.save()
subject_set.add(new_subjects)


print(project.links.subject_sets)

