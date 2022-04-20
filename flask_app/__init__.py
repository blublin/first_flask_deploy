from flask_bcrypt import Bcrypt
from flask import Flask, flash, session
import re

app = Flask(__name__)

app.secret_key = "9NEudK7YqHrJ-PUtyFms" # INSERT GENERATED KEY FROM SITE