from flask import Flask, render_template, session
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():

    columns=["name_shop", "format_vinyl", "vinyl_title", "vinyl_image", "vinyl_link", "mp3_title", "mp3_link"]
    df = pd.read_csv('scripts_scrap/out.csv',
        header=None,
        names=columns)

        
    list_vinyls = df[:50].to_dict(orient='records')
    return render_template('home.html', list_vinyls=list_vinyls)




if __name__ == "__main__":
    print('------- Start App  -------')
    app.debug = True
    app.run
