from flask import Flask, render_template
import twilio.twiml
import rwfb

application = Flask(__name__)

@application.route('/hello')
def hello():
    return 'Hello World'

@application.route("/text", methods=["GET", "POST"])
def textHandling():
    """Handling a text message."""
    db = rwfb.openDB()
    return request.form["From"]
    #resp.message("Hello friends I am twilio")
    #return str(resp)

@application.route("/create/<number>")
def createPlayer(number):
    db = rwfb.openDB()
    num = number#"18007778888"
    rwfb.createPlayer(db, num, "worm")
    return "Player Created"

@application.route("/player/<number>")
def viewPlayer(number):
    db = rwfb.openDB()
    num = number#"18007778888"
    return rwfb.getStats(db, number)

@application.route("/game")
def showPlayers(players = rwfb.getAll(rwfb.openDB())):
    #db = rwfb.openDB()
    #players = rwfb.getAll(db)
    return render_template('show_map.html', players=players)

@application.route("/")
def root():
    return render_template('index.html')

if __name__ == "__main__":
    application.debug = True
    application.run()
