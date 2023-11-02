from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret keep it, safe keep it'