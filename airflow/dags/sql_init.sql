
-- This file is used to create the database and the tables.
-- And to insert the data in the table shops


CREATE TABLE IF NOT EXISTS shops (
    name VARCHAR(255),
    name_function VARCHAR(255),
    links VARCHAR[],
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS vinyls (
    id SERIAL,
    site VARCHAR(255),
    format VARCHAR(255),
    title VARCHAR(255),
    image VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS songs (
    id SERIAL,
    id_vinyl INT NOT NULL,
    title VARCHAR(255),
    mp3 VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id)
);

CREATE TABLE IF NOT EXISTS extract_vinyls_temp (
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


CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    name VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS favoris (
    id SERIAL,
    id_vinyl INT NOT NULL,
    id_song INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vinyl) REFERENCES vinyls (id),
    FOREIGN KEY (id_user) REFERENCES users (id)
    FOREIGN KEY (id_song) REFERENCES songs (id)
);


INSERT INTO shops (name, name_function, links)
VALUES ('jahwaggysrecords', 'scrap_jahwaggysrecords', '{"https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection","https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection","https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection","https://jahwaggysrecords.com/fr/8-brand-new-lp-vinyl-selection","https://jahwaggysrecords.com/fr/18-test-press-selection"}'),
    ('onlyrootsreggae', 'scrap_onlyrootsreggae', '{"https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=1&order=product.date_add.desc"}'),
    ('controltower', 'scrap_controltower', '{"https://controltower.fr/fr/"}'),
    ('reggaefever', 'scrap_reggaefever', '{"https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=10&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=12&sort=relDate_riddim"}'),
    ('pataterecords', 'scrap_pataterecords', '{"https://www.patate-records.com/shop/1/1/1/type/1/","https://www.patate-records.com/shop/1/1/1/type/2/","https://www.patate-records.com/shop/1/1/1/type/3/"}'),
    ('toolboxrecords', 'scrap_toolboxrecords', '{"https://www.toolboxrecords.com/fr/catalog/list/categoryID/3/item_nbr/60"}'),
    ('lionvibes', 'scrap_lionvibes', '{"https://shop.lionvibes.com/search.php?mode=quicksearch&search_string=&format=7&decade=&pressing=&period=&page=1&sort_by_created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&search_string=&format=10&decade=&pressing=&period=&page=1&sort_by_created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&sort_by_created_desc&search_string=&format=12&decade=&pressing=&period=&page=1","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&sort_by_created_desc&search_string=&format=lp&decade=&pressing=&period=&page=1"}'),
    ('reggaemuseum', 'scrap_reggaemuseum', '{"https://www.reggae-museum.com/shop/14-rub-a-dub-early-digital?amp%253Borderby=quantity&orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/15-ska-rocksteady-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/16-dancehall-new-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/18-lp-albums?orderby=quantity&orderway=desc&p="}')
    ON CONFLICT DO NOTHING;
