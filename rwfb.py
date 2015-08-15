
import mongoconn

NOT_FOUND = "No Player Found"
DEAD_PLYR = "Player has died"

def openDB():
    return mongoconn.mongoconn()

def query(db, number):
    qri = {"key": number}
    cursor = db["players"].find(qri)
    value = None
    if cursor.count() != 0:
        #we found something
        value = cursor[0]
    return value

def getItemStats(db, itemname):
    return ""

def createPlayer(db, number, name):
    db["players"].insert({
        key: number,
        loggedon: true,
        location: [0,0],
        isdead: false,
        currenthp: 10,
        maxhp: 10,
        level: 1,
        attack: 10,
        def: 10, 
        equipment: [],
        inventory: []
    })
    return

def applyDamage(db, number, dmg):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND

    cur = player["currenthp"]
    if(cur - dmg <= 0):
        #playerdies
        return DEAD_PLYR
    else:
        db["players"].update(
            {'_id':doc["_id"]}, 
            {"currenthp": cur-dmg},
            upsert=False)

    return "Update Successful: " + str(cur-dmg)
            
def listItems(db, number):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    return player["inventory"]

def equipItem(db, number, item):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND

    equiped = player["equipment"]
    inv = player["inventory"]

    if item in equiped:
        return "Item already equipped."

    if item not in inv:
        return "Item not found"

    stats = getItemStats(db, item)

    #TODO update stats on player

    return "Item Equipped"














