-- DROP TABLE IF EXISTS users;
-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     name TEXT NOT NULL,
--     password TEXT NOT NULL
-- );

DROP TABLE IF EXISTS favoris;
CREATE TABLE favoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name_user TEXT NOT NULL,
    name_shop TEXT NOT NULL,
    format_vinyl TEXT NOT NULL,
    title_vinyl TEXT NOT NULL,
    image_vinyl TEXT NOT NULL,
    url_vinyl TEXT NOT NULL,
    title_mp3 TEXT NOT NULL,
    file_mp3 TEXT NOT NULL
);