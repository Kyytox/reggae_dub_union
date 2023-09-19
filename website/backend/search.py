import os


from .app import app
from . import db
from .models import Vinyl, Song


@app.route("/search/<search>", methods=["GET"])
def search(search):
    """
    Get all vinyls and songs from database.

    Args:
        search (str): search

    Returns:
        list: list of vinyls and songs
    """

    # get vinyls and songs from database with search in title, song title
    req = (
        db.session.query(Vinyl, Song)
        .join(Song, Vinyl.id == Song.id_vinyl)
        .filter(Vinyl.title.ilike(f"%{search}%") | Song.title.ilike(f"%{search}%"))
        .order_by(Vinyl.id.desc())
        .all()
    )

    print(req)

    result = []
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
