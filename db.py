import tinydb
import json
from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    name: str | None = ''
    id: int | None
    description: str | None = ''
    notes: str | None = ''
    charge_num: str | None = ''
    category: str | None = "NONE"
    tags: list | None = []
    tve: str | None = ''
    todos: str | None = ''
    created: str | None = ''
    updated: str | None = ''
    status: str | None = ''
    disposition: str | None = ''
    directory: str | None = ''
    use_local_fs: bool | None = False
    
    def as_dict(self):
        return dict(self)
    
    @classmethod
    def from_doc(cls, data: tinydb.table.Document):
        task = cls()
        task.__dict__.update(data)
        task.id = data.doc_id
        return task

    
class DB:
    def __init__(self, db_file:str='.', clean=False):
        self.file = db_file
        self.db = tinydb.TinyDB(self.file)
        self.tasks = self.db.table("tasks")
        # self.tags = self.db.table('tags')
        
        if clean:
            self.clean_duplicates()
        
    def insert_task(self, task: Task)->tuple[bool, dict]:
        try:
            id = self.tasks.insert(task.as_dict())
            # task.id = id
            new_task = Task.from_doc(self.tasks.get(doc_id=id))
            new_task.created = datetime.now().isoformat(' ')
            print(new_task)
        except:
            return False, {}
        return True, new_task
        
    def all_tasks(self, recent_first:bool=True):
        task_docs = self.tasks.all()
        tasks = [Task.from_doc(doc) for doc in task_docs]
        if recent_first:
            tasks.reverse()
        return tasks
    
    def get_task_by_id(self, task_id:int):
        task = self.tasks.get(doc_id=task_id)
        return Task.from_doc(task)
    
    def update_task(self, task:Task)->bool:
        try:
            if task.created == '':
                task.created = datetime.now().isoformat(' ')
            task.updated = datetime.now().isoformat(' ')
            self.tasks.update(task.as_dict(), doc_ids=[task.id])
        except KeyError:
            return False
        return True
    
    def remove_tasks(self, task_ids)->bool:
        try:
            self.tasks.remove(doc_ids=task_ids)
        except:
            return False
        return True
    
    def clean_duplicates(self):
        tasks = self.tasks.all()
        tasks.reverse()
        tasks = [Task.from_doc(doc) for doc in tasks]
        names = []
        cleaned_tasks = []
        duplicates_ids = []
        for task in tasks:
            if task.name in names:
                duplicates_ids.append(task.id)
            else:
                names.append(task.name)
        
        print(f'Duplicates: {len(duplicates_ids)}')
        # print('IDS:', duplicates_ids)  
        print('Removing duplicate entries from db.')     
        self.remove_tasks(duplicates_ids)
        print('Duplicate entries removed.')
                
        