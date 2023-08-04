
-- This file is used to create the database and the tables.
-- And to insert the data in the table shops


DROP TABLE IF EXISTS shops CASCADE;
CREATE TABLE shops (
    id SERIAL,
    name VARCHAR(255),
    name_function VARCHAR(255),
    links VARCHAR[],
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS vinyls CASCADE;
CREATE TABLE vinyls (
    id SERIAL,
    site VARCHAR(255),
    format VARCHAR(255),
    title VARCHAR(255),
    image VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS songs CASCADE;
CREATE TABLE songs (
    id SERIAL,
    id_vinyl INT NOT NULL,
    title VARCHAR(255),
    mp3 VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id)
);

DROP TABLE IF EXISTS extract_vinyls_temp CASCADE;
CREATE TABLE extract_vinyls_temp (
    id SERIAL,
    site VARCHAR(255),
    format VARCHAR(255),
    title VARCHAR(255),
    image VARCHAR(255),
    url VARCHAR(255),
    title_mp3 VARCHAR(255),
    mp3 VARCHAR(255),
    PRIMARY KEY (id)
);


DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id SERIAL,
    name VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (id)
);


DROP TABLE IF EXISTS favoris CASCADE;
CREATE TABLE favoris (
    id SERIAL,
    id_vinyl INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id),
    FOREIGN KEY (id_user) REFERENCES users (id)
);


-- Insert shops
INSERT INTO shops (name, name_function, links) VALUES ('jahwaggysrecords', 'scrap_jahwaggysrecords', '{"https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection","https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection","https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection","https://jahwaggysrecords.com/fr/8-brand-new-lp-vinyl-selection","https://jahwaggysrecords.com/fr/18-test-press-selection"}');
INSERT INTO shops (name, name_function, links) VALUES ('onlyrootsreggae', 'scrap_onlyrootsreggae', '{"https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=1&order=product.date_add.desc"}');
INSERT INTO shops (name, name_function, links) VALUES ('controltower', 'scrap_controltower', '{"https://controltower.fr/fr/"}');
INSERT INTO shops (name, name_function, links) VALUES ('reggaefever', 'scrap_reggaefever', '{"https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=10&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=12&sort=relDate_riddim"}');
INSERT INTO shops (name, name_function, links) VALUES ('pataterecords', 'scrap_pataterecords', '{"https://www.patate-records.com/shop/1/1/1/type/1/","https://www.patate-records.com/shop/1/1/1/type/2/","https://www.patate-records.com/shop/1/1/1/type/3/"}');
INSERT INTO shops (name, name_function, links) VALUES ('toolboxrecords', 'scrap_toolboxrecords', '{"https://www.toolboxrecords.com/fr/catalog/list/categoryID/3/item_nbr/60"}');
INSERT INTO shops (name, name_function, links) VALUES ('lionvibes', 'scrap_lionvibes', '{"https://shop.lionvibes.com/search.php?mode=quicksearch&search_string=&format=7&decade=&pressing=&period=&page=1&sort_by=created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&search_string=&format=10&decade=&pressing=&period=&page=1&sort_by=created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&sort_by=created_desc&search_string=&format=12&decade=&pressing=&period=&page=1","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&sort_by=created_desc&search_string=&format=lp&decade=&pressing=&period=&page=1"}');
INSERT INTO shops (name, name_function, links) VALUES ('reggaemuseum', 'scrap_reggaemuseum', '{"https://www.reggae-museum.com/shop/14-rub-a-dub-early-digital?amp%253Borderby=quantity&orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/15-ska-rocksteady-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/16-dancehall-new-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/18-lp-albums?orderby=quantity&orderway=desc&p="}');

