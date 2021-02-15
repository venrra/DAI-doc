#./app/app.py
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from my_app import model
from ejercicios import ejerciciosP1, subirNotaSVG
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import loads, dumps
from flask_restful import Resource, Api, reqparse

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
dbMongo = client.SampleCollections   # Elegimos la base de datos de ejemplo

app = Flask(__name__)

app.secret_key = 'esto-es-una-clave-muy-secreta'
db = model.my_DB()

api = Api(app)

@app.errorhandler(404)
def page_not_found(error):
    return "<H1 align=\"center\">Donde vas tuuu 404</H1>", 404

@app.route('/')
@app.route('/index')
def index():
    if 'logged' not in session:
        session['logged'] = False
        if 'user' not in session:
            session['user'] = None
    return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    ms=''
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if db.is_password_equal(user, password):
            session['logged'] = True
            session['user'] = user
            return redirect(url_for("index"))
        else:
            ms = 'El correo o la clave son incorrectos'

    return render_template('login.html', ms = ms)

@app.route('/register',methods=['GET', 'POST'])
def registrarse():
    ms = ''
    if request.method == 'POST':
        user = request.form['user']
        name = request.form['nombre']
        apellidos =request.form['apellidos']
        password = request.form['password']
        password2 = request.form['password2']

        if db.is_register(user):
            ms = 'el usuario ya existe'
            return render_template('register.html', ms = ms)
        if not db.is_par_equal(password, password2):
            ms = 'claves incorrectas'
            return render_template('register.html', ms = ms)

        if not db.is_register(user) and db.is_par_equal(password, password2):
            db.add(user,name,apellidos,password)
            session['logged'] = True
            session['user'] = user
            return redirect(url_for("index"))

    return render_template('register.html')

@app.route('/info')
def info_user():
    if session['logged'] == False:
        return render_template('login.html')
    username = session['user']
    datos = db.getInfo(username)
    return render_template('info.html', user = username,name = datos[0], apellidos = datos[1] )

@app.route('/edit', methods=['GET', 'POST'])
def editar():
    ms = ''
    if session['logged'] == False:
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['user']
        nombre = request.form['nombre']
        apellidos =request.form['apellidos']
        password = request.form['password']
        password2 = request.form['password2']
        if db.is_par_equal(password,password2):
            session['user'] = username
            db.setUser(username,nombre,apellidos,password)
            return redirect(url_for("info_user"))
        else:
            ms='Claves incorrectas'

    username = session['user']
    datos = db.getInfo(username)
    return render_template('edit.html', user = username,name = datos[0], apellidos = datos[1],ms=ms)

@app.route('/logout')
def logout():
    session['logged'] = False
    session['user'] = None
    return redirect(url_for("index"))


@app.after_request
def history(response):
    if 'history' not in session:
        session['history'] = []
    session['history'].append([request.url, request.path])
    if len(session['history']) > 3:
        session['history'].pop(0)
    session.modified = True
    return (response)

@app.context_processor
def inyect_session():
    if 'history' not in session:
        session['history'] = []
        urls=""
    else:
        urls = session['history']
    if 'logged' not in session:
        session['logged'] = False
        if 'user' not in session:
            session['user'] = None
    return dict(urls =urls, logged=session['logged'], user = session['user'])


##################################
##             PRACTICA 4      ###
##################################
@app.route('/films', methods=['GET', 'POST'])
def films():
    lista_films = []
    if request.method == 'POST':
        titulo = request.form['buscar']
        lista_films = dbMongo.Sakila_films.find({"Title":{"$regex" : titulo}})
    else:
        # Encontramos los documentos de la coleccion "samples_friends"
        films = dbMongo.Sakila_films.find() # devuelve un cursor(*), no una lista ni un iterador
        for film in films:
            #app.logger.debug(film) # salida consola
            lista_films.append(film)
    return render_template('films.html', films=lista_films)

@app.route('/add_films', methods=['GET', 'POST'])
def add_db():
    if request.method == 'POST':
        Actors = request.form['Actors']
        Category = request.form['Category']
        Description = request.form['Description']
        Length = request.form['Length']
        Rating = request.form['Rating']
        Rental_Duration = request.form['Rental_Duration']
        Replacement_Cost = request.form['Replacement_Cost']
        Special_Features = request.form['Special_Features']
        Title = request.form['Title']

        nuevoID = dbMongo.Sakila_films.find().sort("_id", -1).limit(1)
        _id = nuevoID.next().get("_id") +1
        dbMongo.Sakila_films.insert_one({ "_id":_id, "Actors":Actors,"Category":Category,"Description":Description,"Length":Length,"Rating":Rating,"Rental Duration":Rental_Duration,"Replacement Cost":Replacement_Cost,"Special Features":Special_Features,"Title":Title})
        ms = "Añadido con éxito"
        return redirect(url_for("films", ms=ms))
    return render_template('add_db.html')

@app.route('/editar_films', methods=['GET', 'POST'])
def editar_db():
    edit = []
    if request.method == 'POST':
        if request.form["editar"]!="Guardar":
            film = request.form["editar"]

            edit_films = dbMongo.Sakila_films.find({"Title": film})
            doc = edit_films.next()
            return render_template("editar_db.html",
                    Title = doc["Title"],
                    Actors= doc["Actors"],
                    Category= doc["Category"],
                    Description= doc["Description"],
                    Length= doc["Length"],
                    Rating= doc["Rating"],
                    Rental_Duration= doc["Rental Duration"],
                    Replacement_Cost= doc["Replacement Cost"],
                    Special_Features= doc["Special Features"])
        elif request.form["guardar"]:
            Actors = request.form['Actors']
            Category = request.form['Category']
            Description = request.form['Description']
            Length = request.form['Length']
            Rating = request.form['Rating']
            Rental_Duration = request.form['Rental_Duration']
            Replacement_Cost = request.form['Replacement_Cost']
            Special_Features = request.form['Special_Features']
            Title = request.form['Title']
            dbMongo.Sakila_films.update_one({"Title":Title}, {"$set":{"Actors":Actors, "Category":Category,
                                             "Description":Description, "Length":Length, "Rating":Rating,
                                            "Rental Duration":Rental_Duration, "Replacement Cost":Replacement_Cost,
                                            "Special Features":Special_Features, "Title":Title}})

            return redirect(url_for("films"))

    return redirect(url_for("films"))

@app.route('/borrar_films', methods=['GET', 'POST'])
def borrar_db():
    ms=""
    if request.method == 'POST':
        film = request.form["borrar"]
        if dbMongo.Sakila_films.find({"_id" : film}):
            ms="Se elimino con éxito"
            app.logger.debug(film)
            dbMongo.Sakila_films.delete_one({"Title": film})
        else:
            ms = "No se puedo eliminar"

    return redirect(url_for("films"))


##################################
##             PRACTICA 5      ###
##################################

@app.route('/api/films', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        lista_films = []
        films = dbMongo.Sakila_films.find()
        for film in films:
            lista_films.append(loads(dumps(film)))
        return jsonify(lista_films)

    elif request.method == 'POST':
        Title = Actors = Category = Description = Length = Rating = Rental_Duration = Replacement_Cost = Special_Features=""

        if(request.get_json() is not None):
            if 'Title' in request.get_json():
                Title = request.get_json()['Title']
            if 'Actors' in request.get_json():
                Actors = request.get_json()['Actors']
            if 'Category' in request.get_json():
                Category = request.get_json()['Category']
            if 'Description' in request.get_json():
                Description = request.get_json()['Description']
            if 'Length' in request.get_json():
                Length = request.get_json()['Length']
            if 'Rating' in request.get_json():
                Rating = request.get_json()['Rating']
            if 'Rental Duration' in request.get_json():
                Rental_Duration = request.get_json()['Rental Duration']
            if 'Replacement Cost' in request.get_json():
                Replacement_Cost = request.get_json()['Replacement Cost']
            if 'Special Features' in request.get_json():
                Special_Features = request.get_json()['Special Features']

        nuevoID = dbMongo.Sakila_films.find().sort("_id", -1).limit(1)
        _id = nuevoID.next().get("_id") +1

        film = {"_id":_id,"Actors":Actors,"Category":Category,"Description":Description,"Length":Length,"Rating":Rating,"Rental Duration":Rental_Duration,"Replacement Cost":Replacement_Cost,"Special Features":Special_Features,"Title":Title}
        dbMongo.Sakila_films.insert_one(film)

        salida_films = dbMongo.Sakila_films.find({"Title":Title})

        return jsonify(loads(dumps(salida_films)))


@app.route('/api/films/<filmId>', methods=['GET', 'PUT', 'DELETE'])
def api_2(filmId):
    if request.method == 'GET':
        try:
            films = dbMongo.Sakila_films.find({'Title':{"$regex":filmId}})
            lista_films = []
            for film in films:
                lista_films.append(loads(dumps(film)))
            return jsonify(lista_films)
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400

    elif request.method == 'PUT':
        try:
            film = dbMongo.Sakila_films.find_one({'Title':filmId})

            Title = film.get('Title')
            Actors = film.get('Actors')
            Category = film.get('Category')
            Description = film.get('Description')
            Length = film.get('Length')
            Rating = film.get('Rating')
            Rental_Duration = film.get('Rental_Duration')
            Replacement_Cost = film.get('Replacement_Cost')
            Special_Features = film.get('Special_Features')

            if(request.get_json() is not None):
                if 'Title' in request.get_json():
                    Title = request.get_json()['Title']
                if 'Actors' in request.get_json():
                    Actors = request.get_json()['Actors']
                if 'Category' in request.get_json():
                    Category = request.get_json()['Category']
                if 'Description' in request.get_json():
                    Description = request.get_json()['Description']
                if 'Length' in request.get_json():
                    Length = request.get_json()['Length']
                if 'Rating' in request.get_json():
                    Rating = request.get_json()['Rating']
                if 'Rental Duration' in request.get_json():
                    Rental_Duration = request.get_json()['Rental Duration']
                if 'Replacement Cost' in request.get_json():
                    Replacement_Cost = request.get_json()['Replacement Cost']
                if 'Special Features' in request.get_json():
                    Special_Features = request.get_json()['Special Features']

            dbMongo.Sakila_films.update_one({"Title":Title}, {"$set":{"Actors":Actors, "Category":Category,
                                                        "Description":Description, "Length":Length, "Rating":Rating,
                                                        "Rental Duration":Rental_Duration, "Replacement Cost":Replacement_Cost,
                                                        "Special Features":Special_Features, "Title":Title}})
            film = dbMongo.Sakila_films.find_one({'Title':Title})
            return jsonify(loads(dumps(film)))
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400

    elif request.method == 'DELETE':
        try:
            dbMongo.Sakila_films.delete_one({ 'Title' : filmId })
            return jsonify({ 'Title' : filmId, 'status' : 'Delete' })
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400


################################
### P5 SUBIR NOTA ##############
################################

class apirestful_1(Resource):
    def get(self):
        lista_films = []
        films = dbMongo.Sakila_films.find()
        for film in films:
            lista_films.append(loads(dumps(film)))
        return jsonify(lista_films)
    def post(self):
        Title = Actors = Category = Description = Length = Rating = Rental_Duration = Replacement_Cost = Special_Features=""

        if(request.get_json() is not None):
            if 'Title' in request.get_json():
                Title = request.get_json()['Title']
            if 'Actors' in request.get_json():
                Actors = request.get_json()['Actors']
            if 'Category' in request.get_json():
                Category = request.get_json()['Category']
            if 'Description' in request.get_json():
                Description = request.get_json()['Description']
            if 'Length' in request.get_json():
                Length = request.get_json()['Length']
            if 'Rating' in request.get_json():
                Rating = request.get_json()['Rating']
            if 'Rental Duration' in request.get_json():
                Rental_Duration = request.get_json()['Rental Duration']
            if 'Replacement Cost' in request.get_json():
                Replacement_Cost = request.get_json()['Replacement Cost']
            if 'Special Features' in request.get_json():
                Special_Features = request.get_json()['Special Features']

        nuevoID = dbMongo.Sakila_films.find().sort("_id", -1).limit(1)
        _id = nuevoID.next().get("_id") +1

        film = {"_id":_id,"Actors":Actors,"Category":Category,"Description":Description,"Length":Length,"Rating":Rating,"Rental Duration":Rental_Duration,"Replacement Cost":Replacement_Cost,"Special Features":Special_Features,"Title":Title}
        dbMongo.Sakila_films.insert_one(film)

        salida_films = dbMongo.Sakila_films.find({"Title":Title})

        return jsonify(loads(dumps(salida_films)))

api.add_resource(apirestful_1, "/apirestful/films")

class apirestful_2(Resource):
    def get(self, filmId):
        try:
            films = dbMongo.Sakila_films.find({'Title':filmId})
            lista_films = []
            for film in films:
                lista_films.append(loads(dumps(film)))
            return jsonify(lista_films)
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400

    def put(self, filmId):
        try:
            film = dbMongo.Sakila_films.find_one({'Title':filmId})

            Title = film.get('Title')
            Actors = film.get('Actors')
            Category = film.get('Category')
            Description = film.get('Description')
            Length = film.get('Length')
            Rating = film.get('Rating')
            Rental_Duration = film.get('Rental_Duration')
            Replacement_Cost = film.get('Replacement_Cost')
            Special_Features = film.get('Special_Features')

            if(request.get_json() is not None):
                if 'Title' in request.get_json():
                    Title = request.get_json()['Title']
                if 'Actors' in request.get_json():
                    Actors = request.get_json()['Actors']
                if 'Category' in request.get_json():
                    Category = request.get_json()['Category']
                if 'Description' in request.get_json():
                    Description = request.get_json()['Description']
                if 'Length' in request.get_json():
                    Length = request.get_json()['Length']
                if 'Rating' in request.get_json():
                    Rating = request.get_json()['Rating']
                if 'Rental Duration' in request.get_json():
                    Rental_Duration = request.get_json()['Rental Duration']
                if 'Replacement Cost' in request.get_json():
                    Replacement_Cost = request.get_json()['Replacement Cost']
                if 'Special Features' in request.get_json():
                    Special_Features = request.get_json()['Special Features']

            dbMongo.Sakila_films.update_one({"Title":Title}, {"$set":{"Actors":Actors, "Category":Category,
                                                        "Description":Description, "Length":Length, "Rating":Rating,
                                                        "Rental Duration":Rental_Duration, "Replacement Cost":Replacement_Cost,
                                                        "Special Features":Special_Features, "Title":Title}})
            film = dbMongo.Sakila_films.find_one({'Title':Title})
            return jsonify(loads(dumps(film)))
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400

    def delete(self, filmId):
        try:
            dbMongo.Sakila_films.delete_one({ 'Title' : filmId })
            return jsonify({ 'Title' : filmId, 'status' : 'Delete' })
        except:
            return jsonify({'error':'ERROR_NOT_FOUND'}), 400

api.add_resource(apirestful_2, "/apirestful/films/<string:filmId>")


# ejercicio 2
@app.route('/ordenacion_burbura/<l>')
def ordenacion_burbura(l):
    lista=list(l)
    for i in range(len(lista)):
        if ' ' in lista:
            lista.remove(' ')
    return render_template('ejercicios/ordenacion_burbura.html',res=ejerciciosP1.Burbuja(lista))

# ejercicio 2
@app.route('/ordenacion_seleccion/<l>')
def ordenacion_seleccion(l):
    lista=list(l)
    for i in range(len(lista)):
        if ' ' in lista:
            lista.remove(' ')
    return render_template('ejercicios/ordenacion_seleccion.html',res=ejerciciosP1.seleccion(lista))

# ejerccio 3
@app.route('/criba/<num>')
def criba(num):
    res = ejerciciosP1.criba(int(num))
    return render_template('ejercicios/criba.html',res=res)

# ejerccio 4
@app.route('/fibo')
def fibo():
    res = ejerciciosP1.ejercicio4()
    return render_template('ejercicios/fibo.html',res=res)

# ejerccio 5
@app.route('/corchetes/<num>')
def corchetes(num):
    return render_template('ejercicios/corchetes.html',res=ejerciciosP1.corchetes(int(num)))

# ejerccio 6
@app.route('/expresiones/<cadena>')
def expresiones(cadena):
    res = ejerciciosP1.expresiones(cadena)
    return render_template('ejercicios/expresiones.html')

# subir nota
@app.route('/svg')
def svg_dim():
    svg = subirNotaSVG.svg_dinamico()
    return render_template('ejercicios/svg.html', svg=svg)