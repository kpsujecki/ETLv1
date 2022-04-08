import sqlite3
import argparse
import logging
from itertools import islice
from scripts.sql import trackTable, listeningTable, getTracks, getArtists
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser()

parser.add_argument('-u', dest='uniqueTracks')
parser.add_argument('-t', dest='tripletsSample')
parser.add_argument('-d', dest='database')
args = parser.parse_args()


def readTrackFromFiles():
    with open(args.uniqueTracks, 'r', newline='\n', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '') for line in lines]
        for line in lines:
            fields = line.split("<SEP>")
            cur.execute("""INSERT INTO track (id, id_track, artistName, trackName) VALUES (?, ?, ?, ?)""",
                        (fields[0], fields[1], str(fields[2]), str(fields[3])))
            logging.debug("ID: {} IDTrack: {} ARTISTNAME: {} TRACKNAME: {}".format(fields[0], fields[1], fields[2], fields[3]))
        logging.info('Songs read from file')


def readListeningsFromFiles():
    with open(args.tripletsSample, 'r', newline='\n', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '') for line in lines]
        for line in lines:
            fields = line.split("<SEP>")
            dateListen = datetime.fromtimestamp((int(fields[2])))
            cur.execute('INSERT INTO listening VALUES(?, ?, ?, ?);', (None, fields[0], fields[1], dateListen))
            logging.debug("IDUser {} IDTrack {} DATE {}".format(fields[0], fields[1], dateListen))
        logging.info('Listenings read from file')


def createTablesInDatabase():
    cur.executescript(trackTable)
    logging.info('Track tables have been created')
    cur.executescript(listeningTable)
    logging.info('Listening tables have been created')


def getDataFromDatabase():
    cur.execute(getTracks)
    mostpopulartracks = cur.fetchall()
    showTheMostPopularTracks(mostpopulartracks)
    cur.execute(getArtists)
    mostpopulartartists = cur.fetchall()
    showTheMostPopularArtist(mostpopulartartists)


def showTheMostPopularTracks(mostpopulartracks):
    mostpopulartracks = islice(mostpopulartracks, 5)
    print("The most popular tracks:")
    for idx, mostpopulartrack in enumerate(mostpopulartracks):
        print("{}. Track: {} The number of listenings: {}".format(idx+1, mostpopulartrack[1], mostpopulartrack[0]))


def showTheMostPopularArtist(mostpopulartartists):
    mostpopulartartists = islice(mostpopulartartists, 5)
    print("The most popular Artists/Bands:")
    for idx, mostpopulartartist in enumerate(mostpopulartartists):
        print("{}. Artist: {} The number of listenings: {}".format(idx+1, mostpopulartartist[1], mostpopulartartist[0]))


if __name__ == '__main__':
    con = sqlite3.connect(args.database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    createTablesInDatabase()
    readTrackFromFiles()
    readListeningsFromFiles()
    con.commit()
    logging.info("Saved in database")
    getDataFromDatabase()
    logging.info("Done")
