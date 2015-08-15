#!/Users/gabe/Desktop/Projects/HTP-2015/venv/bin/python3
import rwfb

NUM_MON = 50


def main():
    db = rwfb.openDB()
    rwfb.createMonsters(db, NUM_MON)

main()
