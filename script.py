from panoptes_client import Panoptes, Project, SubjectSet, Subject
import dropbox

dbx = dropbox.Dropbox("")
dbx.users_get_current_account()

for entry in dbx.files_list_folder('Test').entries:
    dbx.files_list_folder(entry,recursive = True)



Panoptes.connect(username='', password='')

project = Project.find("6307")
print(project.display_name)

for workflow in project.links.workflows:
    print(workflow.display_name)

# subject_set = SubjectSet()
#
# subject_set.links.project = project
# subject_set.display_name = 'Tutorial subject set 2'
#
# subject_set.save()

print(project.links.subject_sets)

