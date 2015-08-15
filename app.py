from flask import Flask
import twilio.twiml
import rwfb

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route("/create/<number>")
def createPlayer(number):
    db = rwfb.openDB()
    num = number#"18007778888"
    rwfb.createPlayer(db, num, "worm")
    return "Player Created"

@app.route("/player/<number>")
def viewPlayer(number):
    db = rwfb.openDB()
    num = number#"18007778888"
    return rwfb.getStats(db, number)

@app.route("/game")
def showPlayers():
    db = rwfb.openDB()
    return rwfb.getAll(db)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
 
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)

if __name__ == "__main__":
    app.run()
