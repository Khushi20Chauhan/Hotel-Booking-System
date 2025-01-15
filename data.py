import pymongo

# MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['hotel_booking_system']
rooms_collection = db['rooms']

# Dummy data for rooms with different amenities and features
suite_rooms = [
    {
        "room_number": f"S{i}",
        "type": "Suite",
        "price_per_night": 20000,
        "amenities": ["WiFi", "Swimming Pool", "Jacuzzi"],
        "features": ["King Size Bed", "Living Room", "Kitchenette"]
    } for i in range(1, 21)
]

luxury_rooms = [
    {
        "room_number": f"L{i}",
        "type": "Luxury",
        "price_per_night": 12000,
        "amenities": ["WiFi", "Swimming Pool", "Spa"],
        "features": ["King Size Bed", "Balcony"]
    } for i in range(1, 31)
]

deluxe_rooms = [
    {
        "room_number": f"D{i}",
        "type": "Deluxe",
        "price_per_night": 8000,
        "amenities": ["WiFi", "TV"],
        "features": ["Double Bed", "Balcony"]
    } for i in range(1, 41)
]

standard_rooms = [
    {
        "room_number": f"ST{i}",
        "type": "Standard",
        "price_per_night": 5000,
        "amenities": ["TV"],
        "features": ["Double Bed"]
    } for i in range(1, 51)
]

# Inserting rooms data into the database
rooms_collection.insert_many(suite_rooms)
rooms_collection.insert_many(luxury_rooms)
rooms_collection.insert_many(deluxe_rooms)
rooms_collection.insert_many(standard_rooms)

print("Room data inserted successfully.")
