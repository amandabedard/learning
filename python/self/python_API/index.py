from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>API TEST</h1><p>Testing the request</p>"

app.run()