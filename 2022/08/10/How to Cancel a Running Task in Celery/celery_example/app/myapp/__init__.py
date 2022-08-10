from celery import Celery
from celery.contrib.abortable import AbortableTask
from flask import Flask, render_template
from time import sleep

def make_celery(app):
    celery = Celery(app.name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    app.config.update(CELERY_CONFIG={
        'broker_url': 'redis://redis',
        'result_backend': 'redis://redis'
    })

    celery = make_celery(app)

    @celery.task(bind=True, base=AbortableTask)
    def count(self):
        for i in range(10):
            if self.is_aborted():
                return 'Task stopped!'
            print(i)
            sleep(1)
        return 'DONE!' 

    @app.route('/start')
    def start():
        task = count.delay()
        return render_template('start.html', task=task)


    @app.route('/cancel/<task_id>')
    def cancel(task_id):
        task = count.AsyncResult(task_id)
        task.abort()
        return 'Canceled!'

    return app, celery
