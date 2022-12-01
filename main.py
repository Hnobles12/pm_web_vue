from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
from db import DB, Task
from config import load_config
from fs_manager import FSManager

CONF_PATH = 'db/config.json'

conf = load_config(CONF_PATH)
db = DB(conf.get('pm_db'))
fs = FSManager(conf.get('pm_dir'), {'file_manager':conf.get('file_manager')})

app = FastAPI()
app.mount('/ui', StaticFiles(directory='static'), name='static') 

@app.get('/')
async def root():
    return RedirectResponse('/ui/index.html')

@app.get('/tasks')
async def tasks():
    tasks = db.all_tasks()
    return tasks

@app.get('/fs/task')
async def open_task_in_fm(id:int):
    task = db.get_task_by_id(id)
    fs.open_fm(task, args=['-c'])

@app.post('/tasks/new')
async def new_task(task: Task):
    if task.use_local_fs:
        fs.create_proj_dir(task)
    success, new_task = db.insert_task(task)
    if not success:
        raise HTTPException(500, detail="Could not create task.")
    return new_task

@app.post('/tasks/update')
async def update_task(task: Task):
    if task.use_local_fs:
        fs.create_proj_dir(task)
    if not db.update_task(task):
        raise HTTPException(500, detail="Could not update task. Incorrect task id.")
    return task

@app.post('/tasks/remove')
async def remove_tasks(ids: list[int]):
    if not db.remove_tasks(ids):
        raise HTTPException(500, detail="Could not remove tasks.")