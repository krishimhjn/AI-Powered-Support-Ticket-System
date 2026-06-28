from fastapi import FastAPI

app=FastAPI(title="Ai-Powered-support-ticket-system")


@app.get("/home")
def root():
    return {"Hello":"Welcome to Ai-Powered-support-ticket-system"}

