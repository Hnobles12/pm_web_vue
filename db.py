import tinydb
import json
from pydantic import BaseModel

class Task(BaseModel):
    name: str | None = ''
    id: int | None
    description: str | None = ''
    notes: str | None = ''
    charge_num: int | None = None
    category: str | None = "NONE"
    tags: list | None = []
    tve: str | None = ''
    todos: str | None = ''
    created: str | None = ''
    updated: str | None = ''
    status: str | None = ''
    disposition: str | None = ''
    
    def as_dict(self):
        return dict(self)
    
    @classmethod
    def from_doc(cls, data: tinydb.table.Document):
        task = cls()
        task.__dict__.update(data)
        task.id = data.doc_id
        return task

    
class DB:
    def __init__(self):
        self.file = 'C:\\Users\\e433679\\Documents\\Project_Manager\\pm_web_db.json'
        self.db = tinydb.TinyDB(self.file)
        self.tasks = self.db.table("tasks")
        # self.tags = self.db.table('tags')
        
    def insert_task(self, task: Task)->tuple[bool, dict]:
        try:
            id = self.tasks.insert(task.as_dict())
            # task.id = id
            new_task = Task.from_doc(self.tasks.get(doc_id=id))
            print(new_task)
        except:
            return False, {}
        return True, new_task
        
    def all_tasks(self):
        task_docs = self.tasks.all()
        tasks = [Task.from_doc(doc) for doc in task_docs]
        return tasks
    
    def update_task(self, task:Task)->bool:
        try:
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