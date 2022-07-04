from multiprocessing.dummy import active_children
from flask import Flask, render_template, request, send_from_directory, session
import json
import sqlite3
from numpy import var
import validators
import os
from scripts.scrap_controltowerrecords import *
from scripts.scrap_deeprootsreggaeshop import *
from scripts.scrap_jahwaggys import *
from scripts.scrap_onlyrootsreggae import *
from scripts.scrap_reggaefever import *
from scripts.scrap_unearthedsounds import *
from scripts.scrap_patateRecords import *


def get_db_connection():
    conn = sqlite3.connect('bd_vinyls_dub_scrap.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)

sauv_search_input = ''


#
#
#
@app.route('/')
def index():

    return render_template('home.html')

#
#
#


@app.route('/login', methods=['GET', 'POST'])
def login():

    msg = ''
    if request.method == "POST":
        conn = get_db_connection()
        user = request.form['user']
        password = request.form['password']

        if account := conn.execute("SELECT * FROM users WHERE name = ? and password = ?", (user, password,)).fetchone():
            session['logged_in'] = True
            session['id'] = account['id']
            session['username'] = account['name']
            msg = 'Logged in successfully !'
            return render_template('login.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg=msg)

#
#
#


@app.route('/signUp', methods=['GET', 'POST'])
def signup():

    msg = ''
    if request.method == "POST":
        conn = get_db_connection()
        user = request.form['user']
        password = request.form['password']

        if account := conn.execute("SELECT * FROM users WHERE name = ? ", (user, )).fetchone():
            msg = 'Username already exists !'
        else:
            conn.execute(
                "INSERT INTO users (name, password) VALUES (?, ?)", (user, password))
            conn.commit()

            msg = 'You have successfully registered !'
        return render_template('signup.html', msg=msg)
    return render_template('signup.html', msg=msg)


#
#
#
@app.route("/logout")
def logout():

    session.pop('id', None)
    session.pop('username', None)
    session.pop('logged_in', False)
    return render_template('home.html')


@app.route('/favoris')
def favoris():

    list_vinyls = []

    user = session['username']
    conn = get_db_connection()
    list_favoris = conn.execute(
        "SELECT * FROM favoris WHERE name_user = ? ", (user,)).fetchall()

    for fav in list_favoris:
        list_vinyls.append({'titre': fav[1], 'url':  fav[3], 'img':  fav[2],
                           'songTitle':  fav[4], 'songUrl':  fav[5], 'songDuration':  fav[6]})

    conn.close()
    return render_template('PagePlayerVinyl.html', list_vinyls=list_vinyls)


#
#
#
@app.route('/<variable>', methods=['GET', 'POST'])
def PagePlayerVinyl(variable):
    print('variable: ', variable)

    # if variable == 'favicon.ico':
    #     print('send_from_directory ')
    #     return send_from_directory(os.path.join(app.root_path, 'static'),
    #                                'favicon.ico', mimetype='img/favicon-16x16.png')

    if request.method == "POST":
        # user as click on favoris button => add mp3
        title = request.form['title']
        image = request.form['image']
        url = request.form['url']
        song = request.form['song']
        file = request.form['file']
        duration = request.form['duration']
        user = session['username']
        action = request.form['action']
        print('action', action)

        conn = get_db_connection()

        if action == 'add':
            if not conn.execute("SELECT * FROM favoris WHERE name_user = ? and title_mp3 = ? and file_mp3 = ?", (user, song, file)).fetchone():

                conn.execute("INSERT INTO favoris (name_user, title_vinyl, image_vinyl, url_vinyl, title_mp3, file_mp3, duration_mp3) VALUES (?, ?, ?, ?, ?, ?, ?)",
                             (user, title, image, url, song, file, duration)
                             )

                print('add_fav: ', title, image, url, song, file, duration)
            else:
                print('testeste')
        else:
            # delete fav
            conn.execute(
                "DELETE FROM favoris WHERE name_user = ? and title_mp3 = ? and file_mp3 = ?", (user, song, file))

        conn.commit()
        conn.close()

    else:

        if variable == 'JahWaggys7':
            file_json = 'json/outputJahWaggys7.json'
        elif variable == 'JahWaggys10':
            file_json = 'json/outputJahWaggys10.json'
        elif variable == 'JahWaggys12':
            file_json = 'json/outputJahWaggys12.json'
        elif variable == 'ReggaeFever7':
            file_json = 'json/outputReggaeFever7.json'
        elif variable == 'ReggaeFever10':
            file_json = 'json/outputReggaeFever10.json'
        elif variable == 'ReggaeFever12':
            file_json = 'json/outputReggaeFever12.json'
        elif variable == 'OnlyRootsReggae7':
            file_json = 'json/outputOnlyRootsReggae7.json'
        elif variable == 'OnlyRootsReggae1012':
            file_json = 'json/outputOnlyRootsReggae1012.json'
        elif variable == 'OnlyRootsReggaeLP':
            file_json = 'json/outputOnlyRootsReggaeLP.json'
        elif variable == 'ControlTowerRecords':
            file_json = 'json/outputControlTowerRecords.json'
        elif variable == 'DeepRootsReggaeShop':
            file_json = 'json/outputDeepRootsReggaeShop.json'
        elif variable == 'UnearthedSounds':
            file_json = 'json/outputUnearthedSounds.json'
        elif variable == 'PatateRecords7':
            file_json = 'json/outputPatateRecords7.json'
        elif variable == 'PatateRecords1012':
            file_json = 'json/outputPatateRecords1012.json'
        elif variable == 'PatateRecordsLP':
            file_json = 'json/outputPatateRecordsLP.json'

        with open(file_json) as f:
            # returns JSON
            data = json.load(f)

            # collect data in JSON
            list_vinyls = list(data)

        return render_template('PagePlayerVinyl.html', list_vinyls=list_vinyls)
    return render_template('PagePlayerVinyl.html')


#
#
#
@app.route('/CustomSearch', methods=['GET', 'POST'])
def customSearch():

    global sauv_search_input
    msg = ''
    search_input = ''
    search_input = request.args['req']
    print('search_input: ', search_input)
    print('sauv_search_input: ', sauv_search_input)

    valid = validators.url(search_input)
    print('valid: ', validators.url(search_input))

    if valid != True:
        msg = "Invalid Url"
        print("msg: ", msg)
        return render_template('home.html', msg=msg)

    print("Url is valid")
    if sauv_search_input == search_input:
        # url is already calculated, so just call json file
        print('url is already calculated ')
        with open('json\outputCustomSearch.json') as f:
            # returns JSON
            data = json.load(f)
            # collect data in JSON
            list_vinyls = list(data)

            return render_template('PagePlayerVinyl.html', list_vinyls=list_vinyls)

    sauv_search_input = search_input

    if 'controltower' in search_input:
        print("It controltower")
        scrap_controltowerrecords([search_input])
    elif 'deeprootsreggaeshop' in search_input:
        print("It deeprootsreggaeshop")
        scrap_deeprootsreggaeshop([search_input])
    elif 'jahwaggysrecords' in search_input:
        print("It jahwaggysrecords")
        scrap_jahwaggys([search_input])
    elif 'onlyroots' in search_input:
        print("It onlyroots")
        scrap_onlyrootsreggae([search_input])
    elif 'reggaefever' in search_input:
        print("It reggaefever")
        scrap_reggaefever([search_input])
    elif 'unearthedsounds' in search_input:
        print("It unearthedsounds")
        scrap_unearthedsounds([search_input])
    elif 'patate' in search_input:
        print("It patateRecords")
        scrap_patateRecords([search_input])
    else:
        print('not Found')
        msg = "Invalid Url"
        print("msg: ", msg)
        return render_template('home.html', msg=msg)

    with open('json\outputCustomSearch.json') as f:
        # returns JSON
        data = json.load(f)

        # collect data in JSON
        list_vinyls = list(data)

        return render_template('PagePlayerVinyl.html', list_vinyls=list_vinyls)


if __name__ == "__main__":
    print('------- Start App  -------')
    app.config['SERVER_NAME'] = "www.vinylsdubscrap.xyz"
    app.debug = True
    app.run
    # app.run(host='0.0.0.0')
