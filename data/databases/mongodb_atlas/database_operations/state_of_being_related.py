from pymongo.collection import Collection
from pymongo.database import Database
import os
from dotenv import load_dotenv
from ..connect_to_database import get_database

# Load environment variables from a .env file located at the specified path
dotenv_path = "configuration/.env"
load_dotenv(dotenv_path)

def add_state_of_being(user_state_data: dict) -> None:
    """
    Adds a state of being record for a user to the MongoDB Atlas database.

    This function first queries the users collection to find the user by username.
    If the user is found, it adds the state of being record to the states collection
    with the user's ID. If the user is not found, it prints an error message.

    Parameters:
        user_state_data (dict): A dictionary containing the state of being data, including
                           the 'user_name' and other state-related information.

    Returns:
        None
    """
    # Connect to the database using environment variables for configuration
    database: Database = get_database(os.getenv("MONGO_DB_ATLAS_USER_RELATED_DB_NAME"))
    
    # Access the users and states collections from the database
    users_collection: Collection = database[os.getenv("MONGO_DB_ATLAS_USERS_COLLECTION_NAME")]
    user_states_collection: Collection = database[os.getenv("MONGO_DB_ATLAS_USER_STATES_COLLECTION_NAME")]
    
    # Query the database for the user_id based on user_name
    user_record = users_collection.find_one({"user_name": user_state_data["user_name"]})
    
    if user_record:
        # If user is found, add the user_id to the user_state_data and remove the user_name
        user_state_data["user_id"] = user_record["_id"]
        del user_state_data["user_name"]
        
        # Insert the state of being record into the states collection
        user_states_collection.insert_one(user_state_data)
        print("State of being recorded successfully.")
    else:
        # If the user is not found, print an error message
        print(f"User {user_state_data['user_name']} not found in database.")
