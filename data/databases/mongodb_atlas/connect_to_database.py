from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
dotenv_path = "configuration/.env"
load_dotenv(dotenv_path)

def get_database_client(database_name: str) -> MongoClient:
    """
    Initializes and returns a MongoDB client for the specified database.
    
    This function constructs a MongoDB connection URI using environment variables
    for the MongoDB username, password, and cluster address. It then initializes
    and returns a MongoClient instance connected to the specified database using
    the constructed URI.
    
    Parameters:
        database_name (str): The name of the database to connect to.
    
    Returns:
        MongoClient: A client instance connected to the specified MongoDB database.
    
    Example:
        >>> client = get_database_client('myDatabase')
        >>> print(client)
        MongoClient(host=['cluster0.example.mongodb.net:27017'], document_class=dict, tz_aware=False, connect=True, server_api=ServerApi('1'))
    """
    # Construct the MongoDB connection URI from environment variables
    uri = f"mongodb+srv://{os.getenv('MONGO_DB_ATLAS_USERNAME')}:{os.getenv('MONGO_DB_ATLAS_PASSWORD')}@{os.getenv('MONGO_DB_ATLAS_CLUSTER_ADDRESS')}/{database_name}?retryWrites=true&w=majority"
    
    # Return a MongoClient instance with the specified server API version
    return MongoClient(uri, server_api=ServerApi("1"))

def get_database(database_name: str) -> MongoClient:
    """
    Returns a database instance for the specified database name.
    
    This function uses the `get_db_client` function to obtain a MongoClient
    instance connected to the specified database. It then returns the database
    instance from the client.
    
    Parameters:
        database_name (str): The name of the database to retrieve.
    
    Returns:
        MongoClient: A database instance from the MongoClient connected to the specified database.
    
    Example:
        >>> database = get_database('myDatabase')
        >>> print(database)
        Database(MongoClient(host=['cluster0.example.mongodb.net:27017'], document_class=dict, tz_aware=False, connect=True, server_api=ServerApi('1')), 'myDatabase')
    """
    client = get_database_client(database_name)
    database = client[database_name]
    return database

