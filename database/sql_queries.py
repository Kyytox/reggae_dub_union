"""
Pgm to Store SQL Queries
"""

# insert in vinyls from extract_vinyls_temp
insert_vinyls = """
INSERT INTO vinyls (site, format, title, image, url)
SELECT DISTINCT site, format, title, image, url
FROM extract_vinyls_temp
WHERE NOT EXISTS (
    SELECT 1
    FROM vinyls
    WHERE vinyls.url = extract_vinyls_temp.url
);
"""

# insert in songs from extract_vinyls_temp
insert_songs = """
INSERT INTO songs (id_vinyl, title, mp3)
SELECT DISTINCT vinyls.id, title_mp3, mp3
FROM extract_vinyls_temp
INNER JOIN vinyls ON vinyls.url = extract_vinyls_temp.url
WHERE NOT EXISTS (
    SELECT 1
    FROM songs
    WHERE songs.mp3 = extract_vinyls_temp.mp3
);
"""

# truncate extract_vinyls_temp
truncate_extract_vinyls_temp = """
TRUNCATE TABLE extract_vinyls_temp;
"""
