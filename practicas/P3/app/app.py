#./app/app.py
from flask import Flask, render_template, session, request, redirect, url_for
from my_app import model
from ejercicios import ejerciciosP1, subirNotaSVG

app = Flask(__name__)

app.secret_key = 'esto-es-una-clave-muy-secreta'

db = model.my_DB()

@app.errorhandler(404)
def page_not_found(error):
    return "<H1 align=\"center\">Donde vas tuuu 404</H1>", 404

@app.route('/')
@app.route('/index')
def index():
    if 'history' not in session:
        session['history'] = []
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
        apellidos =str(request.form['apellidos'])
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
    session['history'].append(request.url)
    if len(session['history']) > 3:
        session['history'].pop(0)
    session.modified = True
    return (response)

@app.context_processor
def inyect_session():
    if 'history' not in session:
        session['history'] = []
    else:
        urls = session['history']
    if 'logged' not in session:
        session['logged'] = False
        if 'user' not in session:
            session['user'] = None

    return dict(urls =urls, logged=session['logged'], user = session['user'])


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
    return render_template('ejercicios/expresiones.html', res=res)

# subir nota
@app.route('/svg')
def svg_dim():
    svg = subirNotaSVG.svg_dinamico()
    return render_template('ejercicios/svg.html', svg=svg)