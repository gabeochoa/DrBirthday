import mongoconn
import random

NOT_FOUND = "No Player Found"
DEAD_ENT = "Entity has died"
MAP_SIZE = 500

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

def getAll(db):
    ply = []
    for pl in db["players"].find({}):
        if(pl["loggedon"] == "true"):
            ply.append(pl)
    return ply

def exp(key):
    return key["exp"]
def lvl(key):
    return key["level"]

def getTopTen(db):
    top = []
    ply = []
    for pl in db["players"].find({}):
        ply.append(pl)
    if(len(ply) == 0):
        return top
    ply = sorted(ply, key=exp, reverse=True)
    ply = sorted(ply, key=lvl, reverse=True)

    for t in ply[-10:]:
        top.append( [str(t["key"][-2:]), str(t["name"]), str(t["level"]) , str(t["exp"]) ]  )

    return top


def tostr(pl):
    #str(pl["key"][-2:]) + 
    return " name: "+ str(pl["name"]) +" loc: "+str(pl["location"]) +" hp:" + str(pl["currenthp"])

def getEntities(db, loc, radius):
    ent = []
    coords = [(x,y) 
      for x in range(loc[0] - radius, loc[0] + radius + 1)
      for y in range(loc[1] - radius, loc[1] + radius + 1)
      if ((x - loc[0]) ** 2 + (y - loc[1]) ** 2) <= radius ** 2]

    for (x,y) in coords:
        qri = {"location": [x, y]}
        for pl in db["players"].find(qri):
            if(pl["loggedon"] == "true"):
                ent.append(pl)
        for mb in db["mobs"].find(qri):
            ent.append(mb)
    return ent

def applyExp(db, number, lvlk):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    newex = 0
    if(lvlk > player["level"]):
        newex = 50* (lvlk-player["level"])
    else:
        newex = 25* (lvlk/2)
    
    player["exp"] += newex
    tob = (200*(lvlk-player["level"])**3)
    if(player["exp"] > tob):
        player["exp"] -= tob
        player["level"] += 1

    db["players"].update(
        {'_id':player["_id"]}, 
        player,
        upsert=False)
    return

def attackDir(db, number, dir):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    
    loc = player["location"]
    if(dir == 0): #north
        loc[1] -= 1
    elif(dir == 1): 
        loc[0] += 1
    elif(dir == 2):
        loc[1] += 1 
    elif(dir == 3):
        loc[0] -= 1 

    stuff = getEntities(db, loc, 0)
    if(stuff != []):
        #something is there
        r, lvlk = applyDamage(db, stuff[0], player["attack"])
        if(r == DEAD_ENT):
            applyExp(db, number, lvlk)
        return r
    else:
        return "Nothing Hit"


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
        "name": name,
        "loggedon": "true",
        "location": [random.randint(0,MAP_SIZE),random.randint(0,MAP_SIZE)],
        "currenthp": "10",
        "maxhp": "10",
        "level": "1",
        "attack": "10",
        "defense": "10", 
        "equipment": [],
        "inventory": [],
        "exp": "0"
    })
    return

def getStats(db, number):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    return str(player)

def respawn(db, entity):
    return

def applyDamage(db, entity, dmg):
    cur = entity["currenthp"]
    if(int(cur) - int(dmg) <= 0):
        #playerdies
        respawn(db, entity)
        return DEAD_ENT, entity["level"]
    else:
        entity["currenthp"] = cur-dmg
        if entity["key"] == None:
            #it is a mob
            db["mobs"].update(
                {'_id':entity["_id"]}, 
                entity,
                upsert=False)
        else:
            db["players"].update(
                {'_id':player["_id"]}, 
                player,
                upsert=False)
    return "Attack Successful", entity["level"]
     
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

    if getEntities(db, loc, 0) != []:
        return "Not able to move player"

    player["location"] = loc

    db["players"].update(
        {'_id':player["_id"]}, 
        player,
        upsert=False)

    return "Update Successful"

def updateLogged(db, number, logged = True):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND

    if(player["loggedon"] == "false" and logged):
        player["loggedon"] = "true"
    elif(player["loggedon"] == "true" and not logged):
        player["loggedon"] = "false"
    elif(player["loggedon"] == "true" and logged):
            return "Already Logged in"
    elif(player["loggedon"] == "false" and not logged):
            return "Already Logged out"

    db["players"].update(
        {'_id':player["_id"]}, 
        player,
        upsert=False)

    return "Update Successful"

def setName(db, number, name):
    player = query(db, number)
    if(player == None):
        return NOT_FOUND
    player["name"] = name

    db["players"].update(
        {'_id':player["_id"]}, 
        player,
        upsert=False)

    return "Update Successful"

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














