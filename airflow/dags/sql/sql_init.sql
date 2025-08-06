
-- This file is used to create the database and the tables.
-- And to insert the data in the table shops

-- Create schema if it does not exist
CREATE SCHEMA IF NOT EXISTS public;


CREATE TABLE IF NOT EXISTS public.vinyls (
    vinyl_id serial,
    shop_id integer,
    vinyl_format character varying(255),
    vinyl_title character varying(255),
    vinyl_image character varying(255),
    vinyl_price integer,
    vinyl_currency character varying(255),
    vinyl_reference character varying(255),
    vinyl_url character varying(255),
    PRIMARY KEY (vinyl_id)
);



CREATE TABLE IF NOT EXISTS public.favoris (
    favoris_id serial,
    vinyl_id integer NOT NULL,
    song_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (favoris_id)
);



CREATE TABLE IF NOT EXISTS public.songs (
    song_id serial,
    vinyl_id integer NOT NULL,
    song_title character varying(255),
    song_mp3 character varying(255),
    PRIMARY KEY (song_id)
);



CREATE TABLE IF NOT EXISTS public.users (
    user_id serial,
    user_name character varying(255),
    user_password character varying(255),
    PRIMARY KEY (user_id)
);



CREATE TABLE IF NOT EXISTS public.shops (
    shop_id serial,
    shop_name character varying(255),
    shop_function character varying(255),
    shop_link character varying(255),
    PRIMARY KEY (shop_id)
);



ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_song_songs_id FOREIGN KEY(song_id) REFERENCES public.songs(song_id);

ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_user_users_id FOREIGN KEY(user_id) REFERENCES public.users(user_id);

ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_vinyl_vinyls_id FOREIGN KEY(vinyl_id) REFERENCES public.vinyls(vinyl_id);

ALTER TABLE public.songs
ADD CONSTRAINT fk_songs_id_vinyl_vinyls_id FOREIGN KEY(vinyl_id) REFERENCES public.vinyls(vinyl_id);

ALTER TABLE public.vinyls
ADD CONSTRAINT fk_vinyls_id_shop_shops_id FOREIGN KEY(shop_id) REFERENCES public.shops(shop_id);



-- INSERT INTO shops (name, name_function, links)
-- VALUES ('jahwaggysrecords', 'scrap_jahwaggysrecords', '{"https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection","https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection","https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection","https://jahwaggysrecords.com/fr/8-brand-new-lp-vinyl-selection","https://jahwaggysrecords.com/fr/18-test-press-selection"}'),
--     ('onlyrootsreggae', 'scrap_onlyrootsreggae', '{"https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=1&order=product.date_add.desc","https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=1&order=product.date_add.desc"}'),
--     ('controltower', 'scrap_controltower', '{"https://controltower.fr/fr/"}'),
--     ('reggaefever', 'scrap_reggaefever', '{"https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=10&sort=relDate_riddim","https://www.reggaefever.ch/catalog?format=12&sort=relDate_riddim"}'),
--     ('pataterecords', 'scrap_pataterecords', '{"https://www.patate-records.com/shop/1/1/1/type/1/","https://www.patate-records.com/shop/1/1/1/type/2/","https://www.patate-records.com/shop/1/1/1/type/3/"}'),
--     ('toolboxrecords', 'scrap_toolboxrecords', '{"https://www.toolboxrecords.com/fr/catalog/list/categoryID/3/item_nbr/60"}'),
--     ('lionvibes', 'scrap_lionvibes', '{"https://shop.lionvibes.com/search.php?mode=quicksearch&search_string=&format=7&decade=&pressing=&period=&page=1&sort_by_created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&search_string=&format=10&decade=&pressing=&period=&page=1&sort_by_created_desc","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&sort_by_created_desc&search_string=&format=12&decade=&pressing=&period=&page=1","https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by_created_desc&sort_by_created_desc&search_string=&format=lp&decade=&pressing=&period=&page=1"}'),
--     ('reggaemuseum', 'scrap_reggaemuseum', '{"https://www.reggae-museum.com/shop/14-rub-a-dub-early-digital?amp%253Borderby=quantity&orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/15-ska-rocksteady-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/16-dancehall-new-roots?orderby=quantity&orderway=desc&p=","https://www.reggae-museum.com/shop/18-lp-albums?orderby=quantity&orderway=desc&p="}')
--     ON CONFLICT DO NOTHING;
