import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    process_song_file

    :param cur: connection cursor of the database
    :param filepath: the path of the song file to load data from
    :description: this module loads the song data file from the filepath in pandas dataframe
    and process it then insert the data in songs and artists tables
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (
        df[["song_id", "title", "artist_id", "year", "duration"]]
        .values.flatten()
        .tolist()
    )
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = (
        df[
            [
                "artist_id",
                "artist_name",
                "artist_location",
                "artist_latitude",
                "artist_longitude",
            ]
        ]
        .values.flatten()
        .tolist()
    )
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """
    process_log_file

    :param cur: connection cursor of the database
    :param filepath: the path of the log file to load data from
    :description: this module loads the log data file from the filepath in pandas dataframe
    and process it then insert the data in time, users and song_play tables
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")
    df["ts"] = t

    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week,
                 t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ["timestamp", "hour", "day",
                     "week", "month", "year", "weekday"]
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        ]
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    """
    process_data

    :param cur: connection cursor of the database
    :param conn: connection of the database
    :param filepath: the path of the data directory that contains the data files
    :param func: callback function to call the functions process_log_file or process_song_file
    :description: this module collects all the paths of the data files available in the filepath directory
    : then it calls the callback function for each dtata file to be processed.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
