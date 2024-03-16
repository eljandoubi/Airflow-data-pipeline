CREATE TABLE IF NOT EXISTS staging_events(
        artist TEXT,
        auth TEXT,
        firstName TEXT,
        gender TEXT,
        ItemInSession INT,
        lastName TEXT,
        length FLOAT,
        level TEXT,
        location TEXT,
        method TEXT,
        page TEXT,
        registration TEXT,
        sessionId INT,
        song TEXT,
        status INT,
        ts BIGINT, 
        userAgent TEXT, 
        userId INT
);

CREATE TABLE IF NOT EXISTS staging_songs(
        song_id TEXT PRIMARY KEY,
        artist_id TEXT,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location TEXT,
        artist_name VARCHAR(255),
        duration FLOAT,
        num_songs INT,
        title TEXT,
        year INT
    );



CREATE TABLE IF NOT EXISTS songplays(
        songplay_id         integer identity(0,1) primary key,
        start_time          timestamp not null sortkey distkey,
        user_id             integer not null,
        level               varchar,
        song_id             varchar not null,
        artist_id           varchar not null,
        session_id          integer,
        location            varchar,
        user_agent          varchar
    );



CREATE TABLE IF NOT EXISTS users(
        user_id VARCHAR PRIMARY KEY NOT NULL,
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR
    );

CREATE TABLE IF NOT EXISTS songs(
        song_id VARCHAR PRIMARY KEY NOT NULL,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INT,
        duration FLOAT
    );


CREATE TABLE IF NOT EXISTS artists(
        artist_id VARCHAR PRIMARY KEY NOT NULL,
        name VARCHAR,
        location VARCHAR,
        latitude VARCHAR,
        longitude VARCHAR
    );

CREATE TABLE IF NOT EXISTS time
    (
        start_time  timestamp not null distkey sortkey primary key,
        hour        integer not null,
        day         integer not null,
        week        integer not null,
        month       integer not null,
        year        integer not null,
        weekday     varchar not null
    ) ;