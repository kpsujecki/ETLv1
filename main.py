import sqlite3
import argparse
import logging
from itertools import islice
from scripts.sql import trackTable, listeningTable, getTracks, getArtists

parser = argparse.ArgumentParser()

parser.add_argument('-u', dest='uniqueTracks')
parser.add_argument('-t', dest='tripletsSample')
parser.add_argument('-d', dest='database')
args = parser.parse_args()


def readTrackFromFiles():
    with open(args.uniqueTracks, 'rb') as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split("<SEP>".encode())
            cur.execute("""INSERT INTO track (id, id_track, artistName, trackName) VALUES (?, ?, ?, ?)""",
                        (fields[0], fields[1], str(fields[2]), str(fields[3])))
        logging.info('Songs read from file')


def readListeningsFromFiles():
    with open(args.tripletsSample, 'rb') as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split("<SEP>".encode())
            cur.execute('INSERT INTO listening VALUES(?, ?, ?, ?);', (None, fields[0], fields[1], fields[2]))
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
    for mostpopulartrack in mostpopulartracks:
        logging.info("Track: " + mostpopulartrack[1] + " The number of listenings: ", mostpopulartrack[0])


def showTheMostPopularArtist(mostpopulartartists):
    mostpopulartartists = islice(mostpopulartartists, 5)
    for mostpopulartartist in mostpopulartartists:
        logging.info("Artist: " + mostpopulartartist[1] + " The number of listenings: ", mostpopulartartist[0])


if __name__ == '__main__':
    con = sqlite3.connect(args.database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    createTablesInDatabase()
    readTrackFromFiles()
    readListeningsFromFiles()
    getDataFromDatabase()
    con.commit()
    logging.info("Done")
