import pymongo
# Connect to MongoDB
client = pymongo.MongoClient('localhost:27017')

tdb = client["test1db"]
tcoll = tdb["test1"]

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Check if username already exists
    if tcoll.find_one({"username": username}):
        print("Username already exists. Please choose another one.")
        return
    # Insert new user into database
    user = {"username": username, "password": password}
    tcoll.insert_one(user)  # to insert in the collection
    print("Registration successful.")
    
def user_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = tcoll.find_one({"username": username, "password": password})
    if user:
        print("User login successful.")
        
        # Check user type and perform actions accordingly
        user_type = user.get("user_type")
        
        if user_type == "admin":
            # Admin specific actions
            print("Admin actions:")
            admin_action = input("Enter action (1, 2, 3): ")
            switch_admin_actions(admin_action)
        elif user_type == "user":
            # User specific actions
            print("User actions:")
            user_action = input("Enter action (A, B, C): ")
            switch_user_actions(user_action)
        else:
            print("Unknown user type.")
    else:
        print("Invalid username or password.")