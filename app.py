from flask import Flask, flash, redirect, render_template, session, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

def get_db_connection():
    conn = sqlite3.connect('vinyls_dub_scrap.db')
    conn.row_factory = sqlite3.Row
    return conn


# SingUp
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    print('signup_post')

    # connect BD
    conn = get_db_connection()

    # collect values form 
    name = request.form.get('name')
    password = request.form.get('password')

    if not name:
        flash('Name is required !')
    elif not password:
        flash('Password is required !')
    elif account := conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone():
        flash('Username already exists !')
    else:
        conn.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, generate_password_hash(password, method='sha256')))
        conn.commit()
        session['logged_in'] = True
        session['username'] = name
        flash('Successful account create !', "succes")
        return render_template('succesAuth.html')


    return render_template('signup.html')


# Login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    print('login_post')

    # connect BD
    conn = get_db_connection()

    # collect values form 
    name = request.form.get('name')
    password = request.form.get('password')

    if not name:
        flash('Name is required !')
    elif not password:
        flash('Password is required !')
    elif account := conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone():
        if check_password_hash(account["password"], password):
            session['logged_in'] = True
            # session['id'] = account['id']
            session['username'] = account['name']
            flash('Successful connection !')
            return render_template('succesAuth.html')
        else:
            flash('Password not correct !')
    else:
        flash('Username not exists !')

    return render_template('login.html')


# LogOut
@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('logged_in', False)
    return redirect(url_for('index'))









# Home
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
    
    return render_template('home.html', list_vinyls=list_vinyls, list_shops=list_shops, top_all_vinyls=top_all_vinyls, nb_vinyls="")





if __name__ == "__main__":
    print('------- Start App  -------')
    app.debug = True
    app.run
