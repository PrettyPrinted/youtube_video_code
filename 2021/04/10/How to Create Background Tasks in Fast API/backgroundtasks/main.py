from fastapi import FastAPI, BackgroundTasks
from time import sleep

app = FastAPI()

def send_email(message):
    sleep(5)
    print('Sending email: ', message)

@app.get('/')
async def index(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "Hello there.")
    return {'result' : 'success'}