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
    shop_id integer,
    shop_name character varying(255),
    shop_function character varying(255),
    PRIMARY KEY (shop_id)
);

CREATE TABLE IF NOT EXISTS public.shops_links (
    id_link serial,
    shop_id integer,
    shop_link character varying(255),
    PRIMARY KEY (id_link)
);


ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_song_songs_id FOREIGN KEY(song_id) REFERENCES public.songs(song_id);

ALTER TABLE public.favoris
ADD CONSTRAINT fk_favoris_id_user_users_id FOREIGN KEY(user_id) REFERENCES public.users(user_id);

alter table public.favoris
aDD CONSTRAINT fk_favoris_id_vinyl_vinyls_id foreign key(vinyl_id) references public.vinyls(vinyl_id);

ALTER TABLE public.songs
ADD CONSTRAINT fk_songs_id_vinyl_vinyls_id FOREIGN KEY(vinyl_id) REFERENCES public.vinyls(vinyl_id);

ALTER TABLE public.vinyls
ADD CONSTRAINT fk_vinyls_id_shop_shops_id FOREIGN KEY(shop_id) REFERENCES public.shops(shop_id);

ALTER TABLE public.shops_links
ADD CONSTRAINT fk_shops_links_id_shop_shops_id FOREIGN KEY(shop_id) REFERENCES public.shops(shop_id);
