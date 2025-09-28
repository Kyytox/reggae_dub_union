CREATE SCHEMA IF NOT EXISTS public;


CREATE TABLE IF NOT EXISTS public.vinyls (
    vinyl_id serial,
    shop_id integer,
    shop_link_id integer,
    vinyl_format character varying(20),
    vinyl_title text,
    vinyl_image text,
    vinyl_price integer,
    vinyl_currency character varying(5),
    vinyl_reference text,
    vinyl_link text,
    vinyl_date_extract timestamp without time zone,
    PRIMARY KEY (vinyl_id)
);


CREATE TABLE IF NOT EXISTS public.favoris (
    favori_id serial,
    vinyl_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (favori_id)
);


CREATE TABLE IF NOT EXISTS public.songs (
    song_id serial,
    vinyl_id integer NOT NULL,
    song_title text,
    song_mp3 text,
    PRIMARY KEY (song_id)
);


CREATE TABLE IF NOT EXISTS public.users (
    user_id serial,
    user_name character varying(50),
    user_email character varying(100),
    user_password text,
    PRIMARY KEY (user_id)
);


CREATE TABLE IF NOT EXISTS public.shops (
    shop_id integer,
    shop_name character varying(40),
    shop_function character varying(40),
    shop_real_name character varying(40),
    shop_nb_min_pages integer, -- Minimum number of pages to scrap for the shop
    shop_nb_max_pages integer, -- Maximum number of pages to scrap for the shop
    PRIMARY KEY (shop_id)
);

CREATE TABLE IF NOT EXISTS public.shops_links (
    shop_link_id serial,
    shop_id integer,
    shop_link text,
    PRIMARY KEY (shop_link_id)
);


ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_user_users_id FOREIGN KEY(user_id) REFERENCES public.users(user_id);

alter table public.favoris
ADD CONSTRAINT fk_favoris_id_vinyl_vinyls_id foreign key(vinyl_id) references public.vinyls(vinyl_id);

ALTER TABLE public.songs
ADD CONSTRAINT fk_songs_id_vinyl_vinyls_id FOREIGN KEY(vinyl_id) REFERENCES public.vinyls(vinyl_id);

ALTER TABLE public.vinyls
ADD CONSTRAINT fk_vinyls_id_shop_shops_id FOREIGN KEY(shop_id) REFERENCES public.shops(shop_id);

ALTER TABLE public.shops_links
ADD CONSTRAINT fk_shops_links_id_shop_shops_id FOREIGN KEY(shop_id) REFERENCES public.shops(shop_id);

ALTER TABLE public.vinyls
ADD CONSTRAINT fk_vinyls_id_link_shops_links_id FOREIGN KEY(shop_link_id) REFERENCES public.shops_links(shop_link_id);
