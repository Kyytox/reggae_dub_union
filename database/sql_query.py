"""
Pgm to Store SQL Queries
"""


create_shops = """
CREATE TABLE shops (
    id INT NOT NULL,
    name VARCHAR(255),
    name_function VARCHAR(255),
    links VARCHAR[],
    PRIMARY KEY (id)
);
"""

create_vinyls = """
CREATE TABLE vinyls (
    id INT NOT NULL,
    site VARCHAR(255),
    format VARCHAR(255),
    title VARCHAR(255),
    image VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (id)
);
"""

create_songs = """
CREATE TABLE songs (
    id INT NOT NULL,
    id_vinyl INT NOT NULL,
    title VARCHAR(255),
    mp3 VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id)
);
"""


create_users = """
CREATE TABLE users (
    id INT NOT NULL,
    name VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (id)
);
"""


create_favoris = """
CREATE TABLE favoris (
    id INT NOT NULL,
    id_vinyl INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id),
    FOREIGN KEY (id_user) REFERENCES users (id)
);
"""
