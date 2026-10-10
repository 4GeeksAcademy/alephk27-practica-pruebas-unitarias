from fastapi import FastAPI


app = FastAPI()
app.state.tasks = []


@app.get("/tasks")
def get_tasks():
    return app.state.tasks