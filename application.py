from flask import Flask, render_template, request
import twilio.twiml
import rwfb

application = Flask(__name__)
commands = ["Help"]


def handleAction(msg):
    resp = twilio.twiml.Response()
    if msg.startswith("H"):
        resp.message("Here's a list of commands: {}".format(commands))
    else:
        resp.message("Unrecognized command {}! "
                     "Send 'Help' for options.".format(msg))
    return str(resp)


@application.route("/text", methods=["GET", "POST"])
def textHandling():
    """Handling a text message."""
    db = rwfb.openDB()
    if request.method == "GET":
        return "HI"
    elif request.method == "POST":
        num = request.values.get("From", None)
        msg = request.values.get("Body", None)
        if rwfb.query(db, num):
            return handleAction(msg)
        else:
            rwfb.createPlayer(db, num, "worm")
            resp = twilio.twiml.Response()
            resp.message("You've created an account with {} "
                         "under the name {}".format(num, "worm"))
            return str(resp)


@application.route("/create/<number>")
def createPlayer(number):
    db = rwfb.openDB()
    num = number  # "18007778888"
    rwfb.createPlayer(db, num, "worm")
    return "Player Created"


@application.route("/player/<number>")
def viewPlayer(number):
    db = rwfb.openDB()
    num = number  # "18007778888"
    return rwfb.getStats(db, num)


@application.route("/game")
def showPlayers(players=rwfb.getAll(rwfb.openDB())):
    #db = rwfb.openDB()
    #players = rwfb.getAll(db)
    return render_template('show_map.html', players=players)


@application.route("/")
def root():
    return render_template('index.html')

if __name__ == "__main__":
    application.debug = True
    application.run()
