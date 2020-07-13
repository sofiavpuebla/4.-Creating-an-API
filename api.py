from flask import request
from src.config import PORT,DBURL
from src.app import app
import src.creating



app.run("0.0.0.0",PORT, debug=True)

