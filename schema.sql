
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);


-- CREATE TABLE favoris (
--     name_user TEXT NOT NULL,
--     title_vinyl TEXT NOT NULL,
--     image_vinyl TEXT NOT NULL,
--     url_vinyl TEXT NOT NULL,
--     title_mp3 TEXT NOT NULL,
--     file_mp3 TEXT NOT NULL,
--     duration_mp3 TEXT NOT NULL,
-- );