import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/test', methods=['GET'])
def test():
    stringTest = {
    "id": "1", 
    "name": "Bob"
    }
    return stringTest



app.run(host="127.0.0.1", port=5000, debug=True)