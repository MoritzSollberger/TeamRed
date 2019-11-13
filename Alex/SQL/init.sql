CREATE USER docker_user WITH PASSWORD 'pw';
CREATE DATABASE twitter;
GRANT ALL PRIVILEGES ON DATABASE twitter TO docker_user;
CREATE TABLE tweets ('index' SERIAL,
                    'created_at' TIMESTAMP,
                    'id' VARCHAR(20) PRIMARY KEY,
                    'text' VARCHAR(300),
                    'username' VARCHAR(20),
                    'followers' INTEGER,
                    'user_favorites_count' INTEGER,
                    'retweets' INTEGER,
                    'favorites' INTEGER,
                    'hashtags' TEXT [], --# ARRAY??
                    'interesting' INTEGER
                    );
