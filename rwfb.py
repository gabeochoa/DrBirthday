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

def tostr(pl):
    return str(pl["key"][-2:]) + " hp:" + str(pl["currenthp"])

def getEntities(db, loc, radius):
    obj = []
    #TODO FIX COORDS
    coords = [(x,y) 
        for x in range(loc[0]-radius, loc[0]+radius+1)
        for y in range(loc[1]-radius, loc[1]+radius+1)
        if ((x-loc[0])**2 + (y-loc[1])**2) <= radius**2
    ]
    for x,y in coords:
        #print(x,y)
        qri = {"location": [x,y]}
        pcursor = db["players"].find(qri)
        # ecursor = db["enemies"].find(qri)
        for pl in pcursor:
            obj.append(tostr(pl))
    return obj
                
def getItemStats(db, itemname):
    qri = {"key": itemname}
    cursor = db["items"].find(qri)
    value = None
    if cursor.count() != 0:
        #we found something
        value = cursor[0]
    return value

def createItem(db, item, atk, blk):
    db["items"].insert({
        "name":str(item),
        "attack":str(atk),
        "defense":str(blk),
    })
    return "Item Created"

def createPlayer(db, number, name):
    if(query(db, number) != None):
        return

    db["players"].insert({
        "key": number,
        "loggedon": "true",
        "location": [0,0],
        "isdead": "false",
        "currenthp": "10",
        "maxhp": "10",
        "level": "1",
        "attack": "10",
        "defense": "10", 
        "equipment": [],
        "inventory": []
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
        player["currenthp"] = cur-dmg
        db["players"].update(
            {'_id':player["_id"]}, 
            player,
            upsert=False)

    return "Update Successful: " + str(cur-dmg)
     
def getLocation(db, number):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    return player["location"]

def updateLocation(db, number, dx=0, dy=0):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND

    cur = player["location"]
    loc = [cur[0]+dx, cur[1]+dy]

    player["location"] = loc
    db["players"].update(
        {'_id':player["_id"]}, 
        player,
        upsert=False)

    return "Update Successful: " + str(loc)

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














