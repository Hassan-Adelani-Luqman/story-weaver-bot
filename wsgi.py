import sys
import os

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
path = '/home/HassanAdelani1/story-weaver-bot'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/home/HassanAdelani1/story-weaver-bot/.env')

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run() 