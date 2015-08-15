from flask import Flask, render_template, request
import twilio.twiml
import rwfb

application = Flask(__name__)
commands = ["?", "setuser", "move"]

INCOR_PARM = "Incorrect Parameters"


def handleAction(db, num, msg):
    resp = twilio.twiml.Response()
    spl = msg.split(" ")
    cmd = spl[0]
    if msg.startswith("?") or cmd not in commands:
        resp.message("Here's a list of commands: {}".format(commands))
    elif cmd == "setuser":
        if(len(spl) != 2):
            return str(resp.message(str(INCOR_PARM)))
        r = rwfb.setName(db, num, spl[1])
        if r == "Update Successful":
            resp.message("Name changed to {}! ").format(spl[1])
        else:
            resp.message("Update Failed! ")
    else:
        resp.message("Unrecognized command {}! "
                     "Send '?' for options.".format(msg))
    return str(resp)


@application.route("/text", methods=["GET", "POST"])
def textHandling():
    """Handling a text message."""
    db = rwfb.openDB()
    if request.method == "GET":
        return "HI"
    elif request.method == "POST":
        num = request.values.get("From", None)
        msg = request.values.get("Body", None).lower()
        if rwfb.query(db, num):
            return handleAction(db, num, msg)
        else:
            rwfb.createPlayer(db, num, "worm")
            resp = twilio.twiml.Response()
            resp.message("You've created an account with {} "
                         "under the name {}. Type '?' for a list of"
                         "commands".format(num, "worm"))
            return str(resp)


@application.route("/create/<number>")
def createPlayer(number):
    db = rwfb.openDB()
    num = number  # "18007778888"
    rwfb.createPlayer(db, num, "worm")
    return "Player Created"


@application.route("/leaderboard")
def showLeaders(players=rwfb.getTopTen(rwfb.openDB())):
    return render_template('leaderboard.html', players=players)


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
