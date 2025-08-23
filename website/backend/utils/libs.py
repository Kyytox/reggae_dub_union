def format_return_data(df):
    """
    Format the DataFrame to return a structured dictionary with vinyls, songs, and shops.

        Args:
            df (DataFrame): The DataFrame containing vinyls, songs, and shops data.
        Returns:
            dict: A dictionary with three keys: 'vinyls
            'songs', and 'shops', each containing a list of dictionaries with the relevant data.
    """

    # add cols id_elem
    df["id_elem"] = range(1, len(df) + 1)

    # keep cols starting with "vinyls"
    cols_vinyls = [
        df.columns[i]
        for i in range(len(df.columns))
        if df.columns[i].startswith("vinyl")
    ]

    # add user_id and favoris_id if exists
    if "user_id" in df.columns and "favori_id" in df.columns:
        cols_vinyls += ["user_id", "favori_id"]

    # create a DataFrame with the vinyls data
    df_vinyls = (
        df[cols_vinyls + ["shop_id", "shop_name", "id_elem"]]
        .copy()
        .drop_duplicates(subset=["vinyl_id"])
    )

    #
    #
    # keep cols starting with "songs"
    cols_songs = [
        df.columns[i]
        for i in range(len(df.columns))
        if df.columns[i].startswith("song")
    ]
    df_songs = df[cols_songs + ["vinyl_id", "vinyl_title"]].copy()

    #
    #
    # kepp cols for shops
    cols_shops = ["shop_id", "shop_name"]
    df_shops = df[cols_shops].copy().drop_duplicates()

    # get favoris if user_id and favori_id exist
    if "user_id" in df.columns and "favori_id" in df.columns:
        df_favoris = df_vinyls[["user_id", "favori_id", "vinyl_id"]]
    else:
        df_favoris = None

    # convert to list of dicts
    df_vinyls = df_vinyls.to_dict(orient="records")
    df_songs = df_songs.to_dict(orient="records")
    df_shops = df_shops.to_dict(orient="records")
    df_favoris = (
        df_favoris.to_dict(orient="records") if df_favoris is not None else None
    )

    # return the data
    return {
        "vinyls": df_vinyls,
        "songs": df_songs,
        "shops": df_shops,
        "favoris": df_favoris,
    }
