from panoptes_client import Panoptes, Project

Panoptes.connect(username='', password='')

project = Project.find("6307")
print(project.display_name)

for workflow in project.links.workflows:
    print(workflow.display_name)

print(project.links.subject_sets)