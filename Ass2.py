import pymongo
from datetime import datetime

# MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['hotel_booking_system']
users_collection = db['users']
rooms_collection = db['rooms']
booked_rooms_collection = db['booked_rooms']

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if users_collection.find_one({"username": username}):
        print("Username already exists. Please choose another one.")
        return
    users_collection.insert_one({"username": username, "password": password, "type": "user"})
    print("Registration successful.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username == "admin" and password == "adminpass":
        return {"username": username, "type": "admin"}
    else:
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            return {"username": username, "type": "user"}
        else:
            print("Invalid username or password.")
            return None


def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. View all rooms details")
        print("2. Add a new room details")
        print("3. Change room price")
        print("4. Add facilities or amenities")
        print("5. View booked rooms")
        print("6. Delete a room")
        print("7. Logout")
        admin_choice = input("Enter your choice: ")
        if admin_choice == '1':
            view_rooms()
        elif admin_choice == '2':
            add_room()
        elif admin_choice == '3':
            change_room_price()
        elif admin_choice == '4':
            add_facilities_or_amenities()
        elif admin_choice == '5':
            view_booked_rooms()
        elif admin_choice == '6':
            delete_room()
        elif admin_choice == '7':
            print("Logged out successfully")
            break
        else:
            print("Invalid choice.")


def change_room_price():
    room_type = input("Enter room type to change price: ")
    new_price = float(input("Enter new price per night: "))
    result = rooms_collection.update_one({"type": room_type}, {"$set": {"price_per_night": new_price}})
    if result.modified_count > 0:
        print("Room price updated successfully.")
    else:
        print("Room type not found. Please enter a valid room type.")

def delete_room():
    while True:
        room_number = input("Enter room number to delete: ")
        result = rooms_collection.delete_one({"room_number": room_number})
        if result.deleted_count > 0:
            print("Room deleted successfully.")
            break  # Exit the loop if deletion is successful
        else:
            print("Room not found. Please enter a valid room number.")



def add_facilities_or_amenities():
    room_type = input("Enter room type to add facilities or amenities: ")
    facilities = input("Enter facilities or amenities separated by commas: ").split(',')
    result = rooms_collection.update_one({"type": room_type}, {"$push": {"amenities": {"$each": facilities}}})
    if result.modified_count > 0:
        print("Facilities or amenities added successfully.")
    else:
        print("Room type not found. Please enter a valid room type.")


def view_booked_rooms():
    booked_rooms = list(booked_rooms_collection.find())
    
    if booked_rooms:
        print("Booked Rooms:")
        for idx, room in enumerate(booked_rooms, start=1):
            print(f"Slot {idx} --> Room Number: {room['room_number']}, Check-in Date: {room['checkin_date'].strftime('%d-%m-%Y')}, Check-out Date: {room['checkout_date'].strftime('%d-%m-%Y')}, Booked By: {room['username']}, Total price: {room['total_price']}")
    else:
        print("No rooms are currently booked.")
        return

    # Count total number of rooms for each room type
    pipeline_total_rooms = [
        {"$group": {"_id": "$type", "total_rooms": {"$sum": 1}}}
    ]
    total_rooms_per_type = {doc['_id']: doc['total_rooms'] for doc in rooms_collection.aggregate(pipeline_total_rooms)}

    # Count number of booked rooms for each room type
    pipeline_booked_rooms = [
        {"$group": {"_id": "$type", "booked_rooms": {"$sum": 1}}}
    ]
    booked_rooms_per_type = {doc['_id']: doc['booked_rooms'] for doc in booked_rooms_collection.aggregate(pipeline_booked_rooms)}

    # Calculate number of available rooms for each room type
    available_rooms_per_type = {room_type: total_rooms_per_type.get(room_type, 0) - booked_rooms_per_type.get(room_type, 0) for room_type in total_rooms_per_type}

    print("\nNumber of Available Rooms per Room Type:")
    for room_type, available_rooms in available_rooms_per_type.items():
        print(f"{room_type}: {available_rooms}")

def add_room():
    room_type = input("Enter room type (S for Suite, D for Deluxe, L for Luxury, ST for Standard): ").upper()
    
    # Dictionary to map room type prefixes to full room type names
    room_type_map = {"S": "Suite", "D": "Deluxe", "L": "Luxury", "ST": "Standard"}
    
    if room_type not in room_type_map:
        print("Invalid room type prefix. Please enter a valid room type prefix.")
        return
    
    room_number_prefix = room_type
    
    while True:
        room_number_suffix = input(f"Enter room number (starting from 1): ")
        room_number = room_number_prefix + room_number_suffix
        
        # Check if the room number already exists in the database
        existing_room = rooms_collection.find_one({"room_number": room_number})
        if existing_room:
            print(f"Room number {room_number} already exists for {existing_room['type']} room type. Please choose another one.")
        else:
            break
    
    price = float(input("Enter price per night: "))
    rooms_collection.insert_one({"room_number": room_number, "type": room_type_map[room_type], "price_per_night": price})
    print("Room added successfully.")


def view_rooms():
    print("Available Room Types and Prices Per Night:")
    pipeline = [
        {"$group": {"_id": "$type", "price_per_night": {"$first": "$price_per_night"}, "amenities": {"$first": "$amenities"}}}
    ]
    distinct_room_types = list(rooms_collection.aggregate(pipeline))
    
    if distinct_room_types:
        for room_type in distinct_room_types:
            print(f"Room Type: {room_type['_id']}, Price Per Night: {room_type['price_per_night']}")
            print("Amenities:", ", ".join(room_type['amenities']))
    else:
        print("No room types found.")


def user_menu(user):
    print(f"Welcome {user['username']}!")
    while True:
        print("User Menu:")
        print("1. View Booking")
        print("2. Book a room")
        print("3. Cancel Booking")
        print("4. Logout")
        user_choice = input("Enter your choice: ")
        if user_choice == '1':
            view_booking(user)
        elif user_choice == '2':
            book_room(user)
        elif user_choice == '3':
            cancel_booking(user)
        elif user_choice == '4':
            print("Logged out successfully")
            break
        else:
            print("Invalid choice.")


def view_booking(user):
    username = user["username"]
    bookings = list(booked_rooms_collection.find({"username": username}))
    if bookings:
        print("Your Bookings:")
        for idx, booking in enumerate(bookings, start=1):
            print(f"Slot {idx} --> Room Number: {booking['room_number']}, Check-in Date: {booking['checkin_date'].strftime('%d-%m-%Y')}, Check-out Date: {booking['checkout_date'].strftime('%d-%m-%Y')}, Price Per Night: {booking['price_per_night']}")
    else:
        print("No bookings found.")


def book_room(user):
    checkin_date_str = input("Enter check-in date (DD-MM-YYYY): ")
    checkout_date_str = input("Enter check-out date (DD-MM-YYYY): ")
    
    checkin_date = datetime.strptime(checkin_date_str, "%d-%m-%Y")
    checkout_date = datetime.strptime(checkout_date_str, "%d-%m-%Y")

    if checkin_date >= checkout_date:
        print("Check-out date must be after check-in date.")
        return

    night_count = (checkout_date - checkin_date).days

    print(f"\nSearching for available rooms for {night_count} nights from {checkin_date.strftime('%d-%m-%Y')} to {checkout_date.strftime('%d-%m-%Y')}...\n")

    # Fetch available room types and their prices
    distinct_room_types = rooms_collection.distinct("type")
    room_prices = {room['type']: room['price_per_night'] for room in rooms_collection.find()}
    
    if distinct_room_types:
        print("Available Room Types and Prices Per Night:")
        for idx, room_type in enumerate(distinct_room_types, start=1):
            print(f"{idx}. {room_type} - Price Per Night: {room_prices[room_type]}")
        
        room_type_choice = input("Enter the room type number to book: ")
        selected_room_type = distinct_room_types[int(room_type_choice) - 1]

        # Fetch available rooms of the selected type
        available_rooms = rooms_collection.find({
            "type": selected_room_type,
            "$or": [
                {"bookings.checkin_date": {"$gte": checkout_date}},
                {"bookings.checkout_date": {"$lte": checkin_date}},
                {"bookings": {"$exists": False}}
            ]
        })

        available_rooms_list = list(available_rooms)

        if available_rooms_list:
            print(f"Available {selected_room_type} Rooms for {night_count} nights:")
            for idx, room in enumerate(available_rooms_list, start=1):
                print(f"Slot {idx} --> Room Number: {room['room_number']}, Price Per Night: {room_prices[selected_room_type]}")
            
            choice = int(input("Enter the slot number to book: ")) - 1
            
            if 0 <= choice < len(available_rooms_list):
                selected_room = available_rooms_list[choice]

                total_price = room_prices[selected_room_type] * night_count

                print("Selected Room Details:")
                print(f"Room Number: {selected_room['room_number']}")
                print(f"Check-in Date: {checkin_date.strftime('%d-%m-%Y')}")
                print(f"Check-out Date: {checkout_date.strftime('%d-%m-%Y')}")
                print(f"Total Price: {total_price}")
                confirm_booking = input("Do you want to proceed with booking? (1 for yes/2 for no): ")

                if confirm_booking.lower() == '1':
                    booking_data = {
                        "username": user["username"],
                        "checkin_date": checkin_date,
                        "checkout_date": checkout_date,
                        "room_number": selected_room["room_number"],
                        "price_per_night": room_prices[selected_room_type],
                        "total_price": total_price
                    }
                    booked_rooms_collection.insert_one(booking_data)
                    print("Room booked successfully!")
                else:
                    print("Booking canceled.")
            else:
                print("Invalid slot number. Please enter a valid slot.")
        else:
            print(f"No available {selected_room_type} rooms for the selected dates.")
    else:
        print("No available room types.")


def cancel_booking(user):
    username = user["username"]
    bookings = list(booked_rooms_collection.find({"username": username}))
    if bookings:
        print("Your Bookings:")
        for idx, booking in enumerate(bookings, start=1):
            print(f"Slot {idx} --> Room Number: {booking['room_number']}, Check-in Date: {booking['checkin_date'].strftime('%d-%m-%Y')}, Check-out Date: {booking['checkout_date'].strftime('%d-%m-%Y')}, Price Per Night: {booking['price_per_night']}")
        
        choice = int(input("Enter the slot number to cancel booking: ")) - 1
        
        if 0 <= choice < len(bookings):
            booking_to_cancel = bookings[choice]
            cancellation_fee = 0.25 * (booking_to_cancel["checkout_date"] - booking_to_cancel["checkin_date"]).days * booking_to_cancel["price_per_night"]
            print(f"Cancellation Fee: {cancellation_fee}")
            confirm_cancel = input("Do you want to proceed with cancellation? (1 for yes/2 for no): ")
            if confirm_cancel.lower() == '1':
                booked_rooms_collection.delete_one({"_id": booking_to_cancel["_id"]})
                print("Booking canceled successfully.")
            else:
                print("Cancellation canceled.")
        else:
            print("Invalid slot number. Please enter a valid slot.")
    else:
        print("No bookings found for cancellation.")


def main():
    while True:
        print("\nWelcome to Hotel Booking System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                if user["type"] == "admin":
                    admin_menu()
                    continue  
                elif user["type"] == "user":
                    user_menu(user)
        elif choice == '3':
            print("Thank you for using Hotel Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

main()
