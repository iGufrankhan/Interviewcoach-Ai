import os
from dotenv import load_dotenv
from mongoengine import connect
from utils.apierror import APIError

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection URI from environment variables
uri = os.getenv("DATABASE_URL")
db_name = os.getenv("DATABASE_NAME", "interviewcoach")

try:
    connect(db=db_name, host=uri)
    print("Successfully connected to MongoDB via MongoEngine!")
except Exception as e:
    print("Unable to connect to the server. Error:", e)
    raise APIError("Database connection failed", status_code=500)

