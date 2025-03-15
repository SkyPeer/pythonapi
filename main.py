from fastapi import FastAPI

app = FastAPI()

# toStart uvicorn main:app --reload --port 8000

def get_fruits():
    items = ["item1", "item2", "item3"]
    for item in items:
        # print(fruit)
        return items

@app.get("/")
async def root():
    return {"message": get_fruits()}
