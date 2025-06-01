import os
from dotenv import load_dotenv 
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

password = os.getenv("MONGODB_PASSWROD")
client = MongoClient(f"mongodb://root:{password}@65.108.219.118:27017/")
print("koblet til database")

db = client["stock"]
collection = db["watchlist"]

def get_stocks(user_id: str) -> list[str]:
    doc = collection.find_one({"_id": user_id})
    return doc["stocks"] if doc and "stocks" in doc else []

def add_stock(user_id: str, symbol: str):
    collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"stocks":symbol}},
        upsert=True
    )

def remove_stocks(user_id: str, symbol: str):
    collection.update_one(
        {"_id":user_id},
        {"$pull": {"stocks": symbol}}
    )

if __name__ == "__main__":
    user_id = "test"

    print(get_stocks(user_id))

    add_stock(user_id, "FRO")
    print("Added Frontline:", get_stocks(user_id))

    remove_stocks(user_id, "FRO")
    print("Removed Frontline:", get_stocks(user_id))

    add_stock(user_id, "FRO")
    print("Added Frontline:", get_stocks(user_id))