from pymongo import MongoClient
from datetime import datetime, date, timedelta
from typing import Optional


_client: Optional[MongoClient] = None
_db = None


def get_db(mongodb_uri: str):
    """Get or create a MongoDB connection. Reuses connection across Lambda invocations."""
    global _client, _db
    if _client is None:
        _client = MongoClient(mongodb_uri)
        _db = _client["birthday_bot"]
    return _db


def get_collection(mongodb_uri: str):
    """Get the birthdays collection."""
    db = get_db(mongodb_uri)
    return db["birthdays"]


def add_birthday(mongodb_uri: str, name: str, month: int, day: int) -> dict:
    """
    Add a birthday to the database.

    Args:
        mongodb_uri: MongoDB connection string
        name: Person's name
        month: Birthday month (1-12)
        day: Birthday day (1-31)
    """
    collection = get_collection(mongodb_uri)

    doc = {
        "name": name,
        "month": month,
        "day": day,
        "created_at": datetime.utcnow(),
    }

    result = collection.insert_one(doc)
    return {"id": str(result.inserted_id), "name": name, "month": month, "day": day}


def update_birthday(mongodb_uri: str, name: str, month: int, day: int) -> bool:
    """
    Update an existing birthday in the database.

    Args:
        mongodb_uri: MongoDB connection string
        name: Person's name
        month: New birthday month (1-12)
        day: New birthday day (1-31)
    """
    collection = get_collection(mongodb_uri)
    result = collection.update_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"$set": {"month": month, "day": day}},
    )
    return result.modified_count > 0


def list_birthdays(mongodb_uri: str) -> list:
    """List all birthdays."""
    collection = get_collection(mongodb_uri)
    birthdays = []
    for doc in collection.find({}, {"_id": 0, "name": 1, "month": 1, "day": 1, "created_at": 1}):
        birthdays.append(
            {
                "name": doc["name"],
                "month": doc["month"],
                "day": doc["day"],
                "created_at": doc.get("created_at", "").isoformat() if doc.get("created_at") else "",
            }
        )
    return birthdays


def get_birthday(mongodb_uri: str, name: str) -> Optional[dict]:
    """Get a specific person's birthday by name."""
    collection = get_collection(mongodb_uri)
    doc = collection.find_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"_id": 0, "name": 1, "month": 1, "day": 1, "created_at": 1},
    )
    if doc:
        return {
            "name": doc["name"],
            "month": doc["month"],
            "day": doc["day"],
            "created_at": doc.get("created_at", "").isoformat() if doc.get("created_at") else "",
        }
    return None


def delete_birthday(mongodb_uri: str, name: str) -> bool:
    """Delete a birthday by name."""
    collection = get_collection(mongodb_uri)
    result = collection.delete_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    return result.deleted_count > 0


def get_upcoming_birthdays(mongodb_uri: str, days_ahead: int = 3) -> list:
    """Get birthdays coming up in the next N days."""
    collection = get_collection(mongodb_uri)
    today = date.today()
    upcoming = []

    for offset in range(days_ahead + 1):
        target = today + timedelta(days=offset)

        docs = collection.find(
            {"month": target.month, "day": target.day},
            {"_id": 0, "name": 1, "month": 1, "day": 1},
        )
        for doc in docs:
            upcoming.append(
                {
                    "name": doc["name"],
                    "month": doc["month"],
                    "day": doc["day"],
                    "days_until": offset,
                }
            )

    return upcoming
