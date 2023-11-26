from Bhagwapataka.celery import app

@app.task
def myfun():
	print('My fun called')