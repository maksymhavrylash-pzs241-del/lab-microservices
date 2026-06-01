from fastapi import FastAPI, HTTPException

STUDENT_N = 2

app = FastAPI(title="Catalog Service")

ITEMS = {
    201: {
        "id": 201,
        "name": "Консультація",
        "price": 500
    },
    202: {
        "id": 202,
        "name": "Навчальний курс",
        "price": 2500
    },
    203: {
        "id": 203,
        "name": "Технічна підтримка",
        "price": 1000
    }
}


@app.get("/items")
def get_items():
    return {
        "student_id": STUDENT_N,
        "items": list(ITEMS.values())
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):

    if item_id not in ITEMS:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "student_id": STUDENT_N,
        "item": ITEMS[item_id]
    }