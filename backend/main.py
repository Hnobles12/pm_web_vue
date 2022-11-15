from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import json
from db import DB, Task

app = FastAPI()
db = DB()

@app.get('/')
async def root():
    html_content = str(open('../pages/index.html', 'r').read())
    return HTMLResponse(content=html_content)   

@app.get('/tasks')
async def tasks():
    tasks = db.all_tasks()
    return tasks

@app.post('/tasks/new')
async def new_task(task: Task):
    if not db.insert_task(task):
        raise HTTPException(500, detail="Could not create task.")
    return task

@app.post('/tasks/update')
async def update_task(task: Task):
    if not db.update_task(task):
        raise HTTPException(500, detail="Could not update task. Incorrect task id.")
    return task