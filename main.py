from fastapi import FastAPI

app = FastAPI()

# toStart uvicorn main:app --reload --port 8000

class Data:
    def __init__(self, items):
        self.items = items

    def get_items_with_offset(self, offset):
        items_length = len(self.items)
        offset = slice(offset, items_length)
        return self.items[offset]

def get_fruits():
    items = ["item1", "item2", "item3"]
    for item in items:
        # print(fruit)
        return items

@app.get("/")
async def root():
    return {"message": get_fruits()}

@app.get("/data")
async def items():
    data = Data(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
    return data.get_items_with_offset(3)
