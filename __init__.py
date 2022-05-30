from flask import Flask
from config import Config

# Create the flask app
app = Flask(__name__, host_matching=True, static_host=Config.HOST_IP, template_folder=Config.TEMPLATE_FOLDER)
app.secret_key = Config.SECRET_KEY