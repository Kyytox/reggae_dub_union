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
    
    list_vinyls = df[:250].to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops)


def getListShops(df):
    lst_shops = df["name_shop"].unique()
    lst_shop_format = []
    for shop in lst_shops:
        lst = df[df["name_shop"] == shop]
        lst_shop_format.append({"shop": shop, "formats": lst["format_vinyl"].unique()})
    
    return lst_shop_format




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
