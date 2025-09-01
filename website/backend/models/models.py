from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from app import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    user_email = db.Column(db.String(100))
    user_password = db.Column(db.Text)

    def __init__(self, user_name, user_email, user_password):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password

    def __repr__(self):
        return f"<User {self.user_id} - {self.user_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Shop(db.Model):
    __tablename__ = "shops"
    shop_id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(40))
    shop_real_name = db.Column(db.String(40))

    def __init__(self, shop_name, shop_real_name):
        self.shop_name = shop_name
        self.shop_real_name = shop_real_name

    def __repr__(self):
        return f"<Shop {self.shop_id} - {self.shop_name}>"

    @classmethod
    def get_all_shops(cls):
        """
        Get all shops from database.

        Returns:
            list: list of shops
        """
        req = cls.query.all()
        data = [
            {
                "shop_id": shop.shop_id,
                "shop_name": shop.shop_name,
                "shop_real_name": shop.shop_real_name,
            }
            for shop in req
        ]
        return data

    @classmethod
    def get_shop_by_id(cls, shop_id):
        """
        Get a shop from database by id.

        Args:
            shop_id (int): id of the shop

        Returns:
            Shop: Shop object
        """
        req = cls.query.filter_by(shop_id=shop_id).first()
        data = (
            {
                "shop_id": req.shop_id,
                "shop_name": req.shop_name,
                "shop_real_name": req.shop_real_name,
            }
            if req
            else None
        )
        return data

    @classmethod
    def get_shops_by_format(cls, format):
        """
        Get all shops that have a specific vinyl format.

        Args:
            format (str): vinyl format

        Returns:
            list: list of shops
        """
        req = (
            db.session.query(cls)
            .join(Vinyl, cls.shop_id == Vinyl.shop_id)
            .filter(Vinyl.vinyl_format == format)
            .distinct()
            .all()
        )
        data = [
            {
                "shop_id": shop.shop_id,
                "shop_name": shop.shop_name,
                "shop_real_name": shop.shop_real_name,
            }
            for shop in req
        ]
        return data


# class ShopLink(db.Model):
#     __tablename__ = "shops_links"
#     shop_link_id = db.Column(db.Integer, primary_key=True)
#     shop_id = db.Column(db.Integer, db.ForeignKey("shops.shop_id"))
#     shop_link = db.Column(db.Text)
#
#     def __init__(self, shop_id, shop_link):
#         self.shop_id = shop_id
#         self.shop_link = shop_link
#
#     def __repr__(self):
#         return f"<ShopLink {self.shop_link_id}>"


class Vinyl(db.Model):
    __tablename__ = "vinyls"
    vinyl_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.shop_id"))
    shop_link_id = db.Column(db.Integer, db.ForeignKey("shops_links.shop_link_id"))
    vinyl_format = db.Column(db.String(20))
    vinyl_title = db.Column(db.Text)
    vinyl_image = db.Column(db.Text)
    vinyl_price = db.Column(db.Integer)
    vinyl_currency = db.Column(db.String(5))
    vinyl_reference = db.Column(db.Text)
    vinyl_link = db.Column(db.Text)

    def __init__(
        self,
        shop_id,
        shop_link_id,
        vinyl_format,
        vinyl_title,
        vinyl_image,
        vinyl_price,
        vinyl_currency,
        vinyl_reference,
        vinyl_link,
    ):
        self.shop_id = shop_id
        self.shop_link_id = shop_link_id
        self.vinyl_format = vinyl_format
        self.vinyl_title = vinyl_title
        self.vinyl_image = vinyl_image
        self.vinyl_price = vinyl_price
        self.vinyl_currency = vinyl_currency
        self.vinyl_reference = vinyl_reference
        self.vinyl_link = vinyl_link

    def __repr__(self):
        return f"<Vinyl {self.vinyl_id}>"

    @classmethod
    def get_all_formats(cls):
        """
        Get all vinyl formats from database.

        Returns:
            list: list of formats
        """
        req = db.session.query(cls.vinyl_format).distinct().all()
        data = [format[0] for format in req]
        return data

    @classmethod
    def get_formats_by_shop(cls, shop_id):
        """
        Get all vinyl formats from database for a shop.

        Args:
            shop_id (int): id of the shop

        Returns:
            list: list of formats
        """
        req = (
            db.session.query(cls.vinyl_format)
            .distinct()
            .filter(cls.shop_id == shop_id)
            .all()
        )
        data = [format[0] for format in req]
        return data

    @classmethod
    def get_nb_vinyls(cls, shops=None, formats=None, search=None):
        """
        Get number of vinyls in database.

        Returns:
            int: number of vinyls
        """
        req = db.session.query(cls)
        if shops:
            req = req.filter(cls.shop_id.in_(shops))
        if formats:
            req = req.filter(cls.vinyl_format.in_(formats))
        if search:
            req = (
                req.join(Song, Song.vinyl_id == cls.vinyl_id)
                .filter(
                    Vinyl.vinyl_title.ilike(f"%{search}%")
                    | Song.song_title.ilike(f"%{search}%")
                )
                .distinct(Vinyl.vinyl_id)
            )

        return req.count()


class Song(db.Model):
    __tablename__ = "songs"
    song_id = db.Column(db.Integer, primary_key=True)
    vinyl_id = db.Column(db.Integer, db.ForeignKey("vinyls.vinyl_id"))
    song_title = db.Column(db.Text)
    song_mp3 = db.Column(db.Text)

    def __init__(self, vinyl_id, song_title, song_mp3):
        self.vinyl_id = vinyl_id
        self.song_title = song_title
        self.song_mp3 = song_mp3

    def __repr__(self):
        return f"<Song {self.song_id} - {self.vinyl_id}>"


class Favori(db.Model):
    __tablename__ = "favoris"
    favori_id = db.Column(db.Integer, primary_key=True)
    vinyl_id = db.Column(db.Integer, db.ForeignKey("vinyls.vinyl_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    def __init__(self, vinyl_id, user_id):
        self.vinyl_id = vinyl_id
        self.user_id = user_id

    def __repr__(self):
        return f"<Favori {self.favori_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_favoris_by_user(cls, user_id):
        """
        Get all favoris from database for a user.

        Args:
            user_id (int): id of the user

        Returns:
            list: list of favoris
        """
        req = (
            db.session.query(cls, Vinyl, Song, Shop)
            .join(Vinyl, cls.vinyl_id == Vinyl.vinyl_id)
            .join(Song, cls.vinyl_id == Song.vinyl_id)
            .join(Shop, Vinyl.shop_id == Shop.shop_id)
            .filter(cls.user_id == user_id)
            .order_by(cls.favori_id.desc())
            .all()
        )

        result = []
        for favori, vinyl, song, shop in req:
            result.append(
                {
                    "user_id": favori.user_id,
                    "favori_id": favori.favori_id,
                    "shop_id": vinyl.shop_id,
                    "shop_name": shop.shop_name,
                    "vinyl_id": favori.vinyl_id,
                    "vinyl_title": vinyl.vinyl_title,
                    "vinyl_image": vinyl.vinyl_image,
                    "vinyl_link": vinyl.vinyl_link,
                    "vinyl_format": vinyl.vinyl_format,
                    "vinyl_price": vinyl.vinyl_price,
                    "vinyl_currency": vinyl.vinyl_currency,
                    "vinyl_reference": vinyl.vinyl_reference,
                    "song_id": song.song_id,
                    "song_title": song.song_title,
                    "song_mp3": song.song_mp3,
                }
            )

        return pd.DataFrame(result)

    @classmethod
    def get_favoris_exist(cls, id_user, id_vinyl):
        """
        Check if a favori exists in the database for a user and a vinyl.

        Args:
            id_user (int): id of the user
            id_vinyl (int): id of the vinyl

        Returns:
            Favori: Favori object if exists, None otherwise
        """

        req = cls.query.filter_by(user_id=id_user, vinyl_id=id_vinyl).first()

        return req
