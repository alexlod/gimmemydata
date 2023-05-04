import os
import json
import shutil

import asana

EXPORT_BASE_DIR = 'export'

if __name__ == '__main__':
    if os.path.exists(EXPORT_BASE_DIR):
        print(f'Deleting existing `{EXPORT_BASE_DIR}` dir.')
        shutil.rmtree(EXPORT_BASE_DIR)

    os.mkdir(EXPORT_BASE_DIR)

    client = asana.Client.access_token(os.environ['ASANA_ACCESS_TOKEN'])

    workspace_to_export = None

    workspaces = client.workspaces.find_all()
    for workspace in workspaces:
        if workspace['name'] == 'Personal Projects':
            workspace_to_export = workspace
            break

    projects = client.projects.find_all(workspace=workspace_to_export['gid'])

    for project in projects:
        print(f'Exporting project {project}')
        dir_name = project['name'].replace('/', '-')
        os.mkdir(os.path.join(EXPORT_BASE_DIR, dir_name))

        object_to_export = {
            'tasks': []
        }

        tasks = client.tasks.find_by_project(project['gid'])
        for task in tasks:
            print(f'Fetching more details for task {task["gid"]}')
            task_details = client.tasks.find_by_id(task['gid'])

            object_to_export['tasks'].append(task_details)

        f = open(os.path.join(EXPORT_BASE_DIR, dir_name, 'all_tasks.json'), 'w')
        f.write(json.dumps(object_to_export, indent=2, sort_keys=True))
        f.close()

