from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

STUDENT_N = 2

app = FastAPI(title="Booking Service")

CATALOG_SERVICE_URL = "http://catalog-service:8000"

BOOKINGS = []


class BookingRequest(BaseModel):
    item_id: int
    customer_name: str


@app.post("/bookings")
def create_booking(booking: BookingRequest):

    try:
        response = requests.get(
            f"{CATALOG_SERVICE_URL}/items/{booking.item_id}"
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Catalog Service unavailable"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail="Service does not exist"
        )

    item_data = response.json()["item"]

    new_booking = {
        "booking_id": len(BOOKINGS) + 1,
        "item_id": booking.item_id,
        "service_name": item_data["name"],
        "price": item_data["price"],
        "customer_name": booking.customer_name,
        "status": "confirmed"
    }

    BOOKINGS.append(new_booking)

    return {
        "student_id": STUDENT_N,
        "booking": new_booking
    }


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int):

    for booking in BOOKINGS:
        if booking["booking_id"] == booking_id:
            return {
                "student_id": STUDENT_N,
                "booking": booking
            }

    raise HTTPException(
        status_code=404,
        detail="Booking not found"
    )