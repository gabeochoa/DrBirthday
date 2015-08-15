#!/Users/gabe/Desktop/Projects/HTP-2015/venv/bin/python3


'''
def openDB():
def query(db, number):
def getItemStats(db, itemname):
def createPlayer(db, number, name)
def applyDamage(db, number, dmg)
def listItems(db, number)
def equipItem(db, number, item)
def getEntities(db, loc array, radius)
'''
import rwfb

def main():
    db = rwfb.openDB()
    #print(rwfb.getAll(db))
    num = "845"#18007778888"
    print(rwfb.getTopTen(db))
    rwfb.createPlayer(db, num, "LeslieLanderTheReprimander")
    rwfb.createPlayer(db, "111", "HartogTheWarthog")
    rwfb.createPlayer(db, "12", "LeiYuAndTheGreatKazoo")
    # print(rwfb.getLocation(db, num))
    #rwfb.updateLocation(db, num, 10, 0)
    # print("Player Moved to:"),
    # print(rwfb.getLocation(db, num))





main()
