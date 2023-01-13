from flask import Flask, render_template, session
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():

    columns=["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link", "mp3_title", "mp3_link"]
    df = pd.read_csv('scripts_scrap/out.csv',
        header=None,
        names=columns)

    # collect shops name 
    list_shops = getListShops(df)
    top_all_vinyls = "False"

    # count nb line in df
    nb_vinyls = df.shape[0]
    
    # collect only xxxx vinyls for home page 
    list_vinyls = df[:150].to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, top_all_vinyls=top_all_vinyls, nb_vinyls=nb_vinyls)


def getListShops(df):
    lst_shops = df["name_shop"].unique()
    lst_shop_format = []
    for shop in lst_shops:
        lst = df[df["name_shop"] == shop]
        lst_shop_format.append({"shop": shop, "formats": lst["format_vinyl"].unique()})
    
    return lst_shop_format


@app.route('/AllVinyls')
def getAllVinyls():

    columns=["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link", "mp3_title", "mp3_link"]
    df = pd.read_csv('scripts_scrap/out.csv',
        header=None,
        names=columns)

    list_shops = getListShops(df)
    top_all_vinyls = "True"
    
    list_vinyls = df.to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, top_all_vinyls=top_all_vinyls, nb_vinyls="")

#
#
#
@app.route('/<shop_name>, <format_vinyl>', methods=['GET', 'POST'])
def PagePlayerVinyl(shop_name, format_vinyl):
    print('variables: ', shop_name)
    print('variables: ', format_vinyl)

    columns=["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link", "mp3_title", "mp3_link"]
    df = pd.read_csv('scripts_scrap/out.csv',
        header=None,
        names=columns)

    # collect shops name 
    list_shops = getListShops(df)
    top_all_vinyls = "True"

    # collect vinyls of one shops with format 
    list_vinyls = df.loc[(df['name_shop'] == shop_name) & (df['format_vinyl'] == format_vinyl)].to_dict(orient='records')
    print("list_vinyls", list_vinyls)
    
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, top_all_vinyls=top_all_vinyls, nb_vinyls="")





if __name__ == "__main__":
    print('------- Start App  -------')
    app.debug = True
    app.run
