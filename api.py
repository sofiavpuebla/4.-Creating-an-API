from flask import request
from src.config import PORT
from src.app import app
import src.creating
import src.analyzefeelings


app.run("0.0.0.0",PORT, debug=True)

