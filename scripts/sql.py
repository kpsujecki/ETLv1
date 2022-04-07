

trackTable = """
        DROP TABLE IF EXISTS track;
        CREATE TABLE IF NOT EXISTS track (
            id varchar(250) PRIMARY KEY ASC,
            id_track varchar(250) NOT NULL,
            artistName varchar(1024) NOT NULL,
            trackName varchar(1024) NOT NULL,
            FOREIGN KEY(id_track) REFERENCES listening(id_track)
        )"""

listeningTable = """
        DROP TABLE IF EXISTS listening;
        CREATE TABLE IF NOT EXISTS listening (
            id INTEGER PRIMARY KEY ASC,
            id_user varchar(250) NOT NULL,
            id_track varchar(250) NOT NULL,
            listeningDate DATE NOT NULL,
            FOREIGN KEY(id_track) REFERENCES track(id_track)
        )"""

getTracks = """
            SELECT count(l.id_track), t.trackName FROM
            listening as l, track as t
            WHERE l.id_track=t.id_track
            GROUP BY l.id_track
            ORDER BY COUNT(l.id_track) DESC;
            """

getArtists = """
            SELECT count(l.id_track), t.artistName FROM
                listening as l, track as t
                WHERE l.id_track=t.id_track
                GROUP BY t.artistName
                ORDER BY COUNT(t.artistName) DESC;
            """