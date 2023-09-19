from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    This class represents the user table in the database.

    Attributes:
        id (int): id of the user
        name (string): name of the user
        password (string): password of the user
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User {self.id} - {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Shop(db.Model):
    """
    This class represents the shop table in the database.

    Attributes:
        name (string): name of the shop
        name_function (string): name of the function to get the vinyls
        links (list): list of links to get the vinyls
    """

    __tablename__ = "shops"
    name = db.Column(db.String(255), primary_key=True)
    name_function = db.Column(db.String(255))
    links = db.Column(db.ARRAY(db.String(255)))

    def __init__(self, name, name_function, links):
        self.name = name
        self.name_function = name_function
        self.links = links

    def __repr__(self):
        return f"<Shop {self.name}>"

    @classmethod
    def get_all_shops(cls):
        """
        Get all shops from database.

        Returns:
            list: list of shops
        """
        req = cls.query.all()

        shops = []
        for shop in req:
            shops.append(
                {
                    "name": shop.name,
                }
            )
        return shops


class Vinyl(db.Model):
    """
    This class represents the vinyl table in the database.

    Attributes:
        id (int): id of the vinyl
        site (string): name of the site
        format (string): format of the vinyl
        title (string): title of the vinyl
        image (string): image of the vinyl
        url (string): url of the vinyl
    """

    __tablename__ = "vinyls"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(255))
    format = db.Column(db.String(255))
    title = db.Column(db.String(255))
    image = db.Column(db.String(255))
    url = db.Column(db.String(255))

    def __init__(self, site, format, title, image, url):
        self.site = site
        self.format = format
        self.title = title
        self.image = image
        self.url = url

    def __repr__(self):
        return f"<Vinyl {self.id}>"

    @classmethod
    def get_vinyls_and_songs(cls):
        """
        Get all vinyls and songs from database.

        Returns:
            list: list of vinyls and songs
        """
        req = (
            db.session.query(cls, Song)
            .join(Song, cls.id == Song.id_vinyl)
            .order_by(cls.id.desc(), Song.title.asc())
            .all()
        )

        result = []
        # recup que les 100 premiers
        # for vinyl, song in req[:75]:
        for vinyl, song in req:
            result.append(
                {
                    "id": vinyl.id,
                    "site": vinyl.site,
                    "format": vinyl.format,
                    "title": vinyl.title,
                    "image": vinyl.image,
                    "url": vinyl.url,
                    "song_id": song.id,
                    "song_id_vinyl": song.id_vinyl,
                    "song_title": song.title,
                    "song_mp3": song.mp3,
                }
            )

        return result


class Song(db.Model):
    """
    This class represents the song table in the database.

    Attributes:
        id (int): id of the song
        id_vinyl (int): id of the vinyl
        title (string): title of the song
        mp3 (string): mp3 of the song

    """

    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    id_vinyl = db.Column(db.Integer, db.ForeignKey("vinyls.id"))
    title = db.Column(db.String(255))
    mp3 = db.Column(db.String(255))

    def __init__(self, id_vinyl, title, mp3):
        self.id_vinyl = id_vinyl
        self.title = title
        self.mp3 = mp3

    def __repr__(self):
        return f"<Song {self.id}>"


class Favori(db.Model):
    """
    This class represents the favori table in the database.

    Attributes:
        id (int): id of the favori
        id_vinyl (int): id of the vinyl
        id_song (int): id of the song
        id_user (int): id of the user
    """

    __tablename__ = "favoris"
    id = db.Column(db.Integer, primary_key=True)
    id_vinyl = db.Column(db.Integer, db.ForeignKey("vinyls.id"))
    id_song = db.Column(db.Integer, db.ForeignKey("songs.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, id_vinyl, id_song, id_user):
        self.id_vinyl = id_vinyl
        self.id_song = id_song
        self.id_user = id_user

    def __repr__(self):
        return f"<Favori {self.id}>"

    @classmethod
    def get_favoris_by_user(cls, id_user):
        """
        Get all favoris from database for a user.

        Returns:
            list: list of favoris
        """
        req = (
            db.session.query(cls, Vinyl, Song)
            .join(Vinyl, cls.id_vinyl == Vinyl.id)
            .join(Song, cls.id_song == Song.id)
            .filter(cls.id_user == id_user)
            .order_by(cls.id.desc())
            .all()
        )

        result = []
        for favori, vinyl, song in req:
            result.append(
                {
                    "fav_id": favori.id,
                    "id_song": favori.id_song,
                    "id_user": favori.id_user,
                    "id": vinyl.id,
                    "site": vinyl.site,
                    "format": vinyl.format,
                    "title": vinyl.title,
                    "image": vinyl.image,
                    "url": vinyl.url,
                    "song_id": song.id,
                    "song_id_vinyl": song.id_vinyl,
                    "song_title": song.title,
                    "song_mp3": song.mp3,
                }
            )

        return result

    @classmethod
    def get_favoris_exist(cls, id_user, id_vinyl, id_song):
        """
        get favori

        Args:
            id_user (int): id of the user
            id_vinyl (int): id of the vinyl
            id_song (int): id of the song
        """

        req = cls.query.filter_by(id_user=id_user, id_vinyl=id_vinyl, id_song=id_song).first()

        return req

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
