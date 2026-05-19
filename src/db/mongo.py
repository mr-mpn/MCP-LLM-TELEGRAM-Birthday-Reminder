from pymongo import MongoClient
from datetime import datetime, date
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


def add_birthday(mongodb_uri: str, name: str, birthday: str, notes: str = "") -> dict:
    """
    Add a birthday to the database.

    Args:
        mongodb_uri: MongoDB connection string
        name: Person's name
        birthday: Birthday in YYYY-MM-DD format
        notes: Optional notes about the person
    """
    collection = get_collection(mongodb_uri)

    # Parse the birthday date
    bday = datetime.strptime(birthday, "%Y-%m-%d")

    doc = {
        "name": name,
        "birthday": bday,
        "month": bday.month,
        "day": bday.day,
        "notes": notes,
        "created_at": datetime.utcnow(),
    }

    result = collection.insert_one(doc)
    return {"id": str(result.inserted_id), "name": name, "birthday": birthday}


def list_birthdays(mongodb_uri: str) -> list:
    """List all birthdays."""
    collection = get_collection(mongodb_uri)
    birthdays = []
    for doc in collection.find({}, {"_id": 0, "name": 1, "birthday": 1, "notes": 1}):
        birthdays.append(
            {
                "name": doc["name"],
                "birthday": doc["birthday"].strftime("%Y-%m-%d"),
                "notes": doc.get("notes", ""),
            }
        )
    return birthdays


def get_birthday(mongodb_uri: str, name: str) -> Optional[dict]:
    """Get a specific person's birthday by name."""
    collection = get_collection(mongodb_uri)
    doc = collection.find_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"_id": 0, "name": 1, "birthday": 1, "notes": 1},
    )
    if doc:
        return {
            "name": doc["name"],
            "birthday": doc["birthday"].strftime("%Y-%m-%d"),
            "notes": doc.get("notes", ""),
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

    # Check each day in the range
    for offset in range(days_ahead + 1):
        check_date = date(
            today.year,
            today.month,
            today.day,
        )
        # Calculate the target date
        from datetime import timedelta

        target = today + timedelta(days=offset)

        docs = collection.find(
            {"month": target.month, "day": target.day},
            {"_id": 0, "name": 1, "birthday": 1, "notes": 1},
        )
        for doc in docs:
            age = target.year - doc["birthday"].year
            upcoming.append(
                {
                    "name": doc["name"],
                    "birthday": doc["birthday"].strftime("%Y-%m-%d"),
                    "days_until": offset,
                    "turning_age": age,
                    "notes": doc.get("notes", ""),
                }
            )

    return upcoming
