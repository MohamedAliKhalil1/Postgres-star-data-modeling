# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL PRIMARY KEY,
start_time TIMESTAMP NOT NULL,
user_id INT NOT NULL, 
level VARCHAR, 
song_id VARCHAR, 
artist_id VARCHAR, 
session_id INT, 
location VARCHAR, 
user_agent VARCHAR,
CONSTRAINT fk_time
      FOREIGN KEY(start_time) 
	  REFERENCES time(start_time),
CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES users(user_id),
CONSTRAINT fk_song
      FOREIGN KEY(song_id) 
	  REFERENCES songs(song_id),
CONSTRAINT fk_artist
      FOREIGN KEY(artist_id) 
	  REFERENCES artists(artist_id)
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id INT PRIMARY KEY, 
first_name VARCHAR, 
last_name VARCHAR, 
gender VARCHAR, 
level VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar PRIMARY KEY,
title varchar NOT NULL,
artist_id VARCHAR NOT NULL,
year INT, 
duration DECIMAL NOT NULL
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar PRIMARY KEY,
name VARCHAR NOT NULL,
location VARCHAR,
latitude DOUBLE PRECISION,
longitude DOUBLE PRECISION
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP PRIMARY KEY, 
hour INT NOT NULL,
day INT NOT NULL,
week INT NOT NULL,
month INT NOT NULL,
year INT NOT NULL,
weekday INT NOT NULL
)
""")

# INSERT RECORDS
songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT(user_id) DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT song_id, songs.artist_id FROM songs JOIN artists ON songs.artist_id = artists.artist_id
WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]