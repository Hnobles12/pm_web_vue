import os
from subprocess import Popen
from pathlib import Path
from db import Task

class EmptyCategoryError(Exception):
    pass

class ProjectDirCreationError(Exception):
    pass

class DirectoryExistsWarning(Warning):
    pass

class FSManager:
    def __init__(self, PM_BASE_DIR:str, apps: dict={}):
        self.base = PM_BASE_DIR
        
        
    def create_proj_dir(self, task: Task)->str:
        category = task.category
        name = task.name
        if category == '':
            raise ProjectDirCreationError('Could not create project directory. Task\'s "category" field is empty.')
        
        #create path in form base+{category}+{name}
        
        path = Path(os.path.join(self.base, category, name))
        print(path)
        
        path.mkdir(parents=True, exist_ok=True)
        task.directory = path
        return path
        
    def open_fm(self, task:Task, fm_exe:str, args:list[str]=[]):
        Popen([fm_exe]+args+[task.directory])
        pass
        
        

# task = Task.parse_obj({'name':'test_name', 'category':'testcat'})

# fs = FSManager('C:\\Users\\e433679\\Documents')
# fs.create_proj_dir(task)
