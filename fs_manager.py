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
        self.fm_exe = apps.get('file_manager')
        
        
    def create_proj_dir(self, task: Task, subdirs=['Documentation', 'Analysis', 'Models'])->str:
        category = task.category
        name = task.name
        if category == '':
            raise ProjectDirCreationError('Could not create project directory. Task\'s "category" field is empty.')
        
        #create path in form base+{category}+{name}
        
        path = Path(os.path.join(self.base, category, name))
        path.mkdir(parents=True, exist_ok=True)
        
        for dir in subdirs:
            p = path / dir
            p.mkdir(parents=True, exist_ok=True)
        
        task.directory = path.as_posix()
        return path.as_posix()
        
    def open_fm(self, task:Task, fm_exe:str=None, args:list[str]=[]):
        if not task.use_local_fs:
            return
        fm_exe = fm_exe or self.fm_exe
        try:
            Popen([fm_exe]+args+[os.path.join(self.base, task.directory)])
        except:
            Popen([fm_exe]+args+[task.directory])
        
        

# task = Task.parse_obj({'name':'test_name', 'category':'testcat'})

# fs = FSManager('C:\\Users\\e433679\\Documents')
# fs.create_proj_dir(task)
