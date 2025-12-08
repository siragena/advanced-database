# Mongita Interactive Session - MongoDB Concepts Introduction

# Installation:
# pip3 install mongita

# Import and connect
# Mongita Interactive Session - MongoDB Concepts Introduction

from mongita import MongitaClientDisk

client = MongitaClientDisk()

# Access database and collection (created automatically)
hello_world_db = client.hello_world_db
mongoose_collection = hello_world_db.mongoose_collection

# Start fresh so every run is clean
mongoose_collection.delete_many({})

print("=== Insert documents ===")
mongoose_collection.insert_many(
    [
        {"name": "Meercat", "does_not_eat": "Snakes"},
        {"name": "Yellow mongoose", "eats": "Termites"},
    ]
)
print("All documents after insert:")
print(list(mongoose_collection.find()))

print("\n=== Count documents ===")
print("Count:", mongoose_collection.count_documents({}))

print("\n=== Update Meercat with weight=2 ===")
mongoose_collection.update_one({"name": "Meercat"}, {"$set": {"weight": 2}})
print("Documents with weight > 1:")
mongoose_list = list(mongoose_collection.find({"weight": {"$gt": 1}}))
print(mongoose_list)
print("Number of docs with weight > 1:", len(mongoose_list))

print("\n=== All documents now ===")
print(list(mongoose_collection.find()))

print("\n=== Delete Meercat ===")

mongoose_collection.delete_one({"name": "Meercat"})
print("Docs with weight > 1 after delete:")

print(list(mongoose_collection.find({"weight": {"$gt": 1}})))

print("\n=== Insert Meercat again ===")

mongoose_collection.insert_many(
    [{"name": "Meercat", "does_not_eat": "Snakes"}]
)

print("\n=== Final state of collection ===")

print(list(mongoose_collection.find()))
