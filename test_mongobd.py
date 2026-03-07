
from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore

uri = "mongodb+srv://mohamedasaadelbadawy_db_user:<your_Password>@cluster0.fs0z5ga.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)