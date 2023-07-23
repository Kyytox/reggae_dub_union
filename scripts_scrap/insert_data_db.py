import os
import glob
import pandas as pd


TEMP_DIR = "scripts_scrap/temp"


def main():
    # collect all parquet files in temp folder
    files = glob.glob(os.path.join(TEMP_DIR, "*.parquet"))

    # create giant df
    df = pd.concat([pd.read_parquet(file) for file in files], ignore_index=True)
    print(df.shape)
    # del vinyls with columns vinyl_link, mp3_link not start with "http"
    df = df[df["vinyl_link"].str.startswith("http")]
    print(df.shape)

    print(df)

    # # Insertion des données dans la table Vinyls
    # df_vinyls = df[["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link"]].drop_duplicates()
    # df_vinyls["Site"] = df_vinyls["name_shop"]
    # df_vinyls = df_vinyls[["Site", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link"]]
    # # df_vinyls.to_sql('Vinyls', conn, if_exists='append', index=False)

    # # Récupération des IDs des vinyls insérés
    # # df_vinyls_ids = pd.read_sql_query('SELECT Id, Site FROM Vinyls', conn)
    # df_vinyls_ids = df_vinyls[["Site"]].drop_duplicates()

    # # Insertion des données dans la table Songs
    # # df_songs = df[["vinyl_title", "mp3_title", "mp3_link"]].drop_duplicates()
    # # df_songs = pd.merge(df_songs, df_vinyls_ids, how="left", left_on="vinyl_title", right_on="Site")
    # # df_songs = df_songs[["Id", "mp3_title", "mp3_link"]]
    # # df_songs = df_songs.rename(columns={"Id": "Id_vinyl"})
    # # df_songs.to_sql('Songs', conn, if_exists='append', index=False)

    # print("Vinyls", df_vinyls)
    # print("Songs", df_songs)

    # print(df)


if __name__ == "__main__":
    main()
