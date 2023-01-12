from flask import Flask, render_template, session
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():

    columns=["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link", "mp3_title", "mp3_link"]
    df = pd.read_csv('scripts_scrap/out.csv',
        header=None,
        names=columns)

    list_shops = getListShops(df)
    topAllVinyls = "False"
    nbVinyls = df.shape[0]
    
    list_vinyls = df[:250].to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, topAllVinyls=topAllVinyls, nbVinyls=nbVinyls)


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
    topAllVinyls = "True"
    
    list_vinyls = df.to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, topAllVinyls=topAllVinyls, nbVinyls="")

#
#
#
@app.route('/<variable>', methods=['GET', 'POST'])
def PagePlayerVinyl(variable):
    print('variables: ', variable)
    return True





if __name__ == "__main__":
    print('------- Start App  -------')
    app.debug = True
    app.run
