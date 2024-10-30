# mongo.py

from mongoengine import connect, disconnect, get_connection
import logging

# Set up logging
logger = logging.getLogger(__name__)

# MongoDB connection settings
MONGODB_DATABASES = {
    'default': {
        'name': 'mydatabase',  # Replace with your actual database name
        'host': 'localhost',      # MongoDB host
        'port': 27017,            # Default MongoDB port
        # Uncomment if using authentication
        # 'username': 'your_username',
        # 'password': 'your_password',
    }
}

def connect_to_mongo():
    try:
        if not get_connection('default'):
            disconnect('default')  # Disconnect if there is an existing connection
            logger.debug("Connecting to MongoDB with settings: %s", MONGODB_DATABASES['default'])
            connect(**MONGODB_DATABASES['default'])
            logger.debug("Connection successful!")
    except Exception as e:
        logger.error("Failed to connect to MongoDB: %s", e)

# Call the connect function to establish a connection when this file is imported
connect_to_mongo()
