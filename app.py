from flask import Flask, render_template
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
def showPlayers(players = rwfb.getAll(rwfb.openDB())):
    #db = rwfb.openDB()
    #players = rwfb.getAll(db)
    return render_template('show_map.html', players=players)

@app.route("/")
def root():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
