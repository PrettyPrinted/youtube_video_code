from celery import shared_task
from time import sleep

@shared_task(bind=True)
def mytask(self, duration):
    self.update_state(state="PROCESSING", meta={"progress": 0})
    sleep(duration // 3)
    self.update_state(state="PROCESSING", meta={"progress": 33})
    sleep(duration // 3)
    self.update_state(state="PROCESSING", meta={"progress": 66})
    sleep(duration // 3)
    self.update_state(state="PROCESSING", meta={"progress": 99})
    return {"result": "Task is done!", "progress": 100}