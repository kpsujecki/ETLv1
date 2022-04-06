import sqlite3


def read_track_from_files():
    with open('resources/unique_tracks.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split("<SEP>".encode())
            cur.execute("""INSERT INTO track (id, id_track, artistName, trackName) VALUES (?, ?, ?, ?)""",
                (fields[0], fields[1], str(fields[2]), str(fields[3])))

def read_listenings_from_files():
    with open('resources/triplets_sample_20p.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split("<SEP>".encode())
            cur.execute('INSERT INTO listening VALUES(?, ?, ?, ?);', (None, fields[0], fields[1], fields[2]))

def databaseConnect():
    cur.executescript("""
        DROP TABLE IF EXISTS track;
        CREATE TABLE IF NOT EXISTS track (
            id varchar(250) PRIMARY KEY ASC,
            id_track varchar(250) NOT NULL,
            artistName varchar(1024) NOT NULL,
            trackName varchar(1024) NOT NULL,
            FOREIGN KEY(id_track) REFERENCES listening(id_track)
        )""")
    cur.executescript("""
        DROP TABLE IF EXISTS listening;
        CREATE TABLE IF NOT EXISTS listening (
            id INTEGER PRIMARY KEY ASC,
            id_user varchar(250) NOT NULL,
            id_track varchar(250) NOT NULL,
            listeningDate DATE NOT NULL,
            FOREIGN KEY(id_track) REFERENCES track(id_track)
        )""")

if __name__ == '__main__':
    con = sqlite3.connect('resources/db.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    databaseConnect()
    fields = []
    listenings = []
    read_track_from_files()
    read_listenings_from_files()
    con.commit()
    print("Koniec")

