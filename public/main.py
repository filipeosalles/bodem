from flask import Flask, render_template, url_for, request, redirect, session, abort, jsonify, flash
import io
import os
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sheet2 as sh2
import sheet3 as sh3
import extra2 as ex2
import extra3 as ex3
import extra4 as ex4
import bofek
import cgi 


app = Flask(__name__)
app.secret_key = 'the random string'
app.debug = True
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'kml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/')
def home1():
    return render_template('home1.html')           


@app.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        session['sand'] = request.form['sand']
        session['silt'] = request.form['silt']
        session['clay'] = request.form['clay']
        session['organic_matter'] = request.form['organic_matter']
        result = sh2.calculateChart(session['sand'], session['silt'], session['clay'], session['organic_matter'])
        session['result'] = result
        if result != '':
            session['message'] = sh2.messages[result]
            session['generic_text'] = sh2.generic_text[result]
        else:
            session['graphic'] = 'picture1.png'
            session['message'] = "Not Found!"
            session['generic_text'] = "Not Found!"
        selectKey = result.lower() + '.png'
        session['graphic'] = selectKey
        return redirect(url_for('home'))
    else:
        if session.get("graphic") == None:
            session['graphic'] = 'picture1.png'
        return render_template('home.html')


@app.route('/print-plot')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = np.random.rand(100)
    ys = np.random.rand(100)
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sheet2')
def sheet2():
    return sh2.sheet2()


@app.route('/sheet3')
def sheet3():
    return sh3.sheet3()


@app.route('/extra2', methods=['POST', 'GET'])
def extra2():
    return ex2.main()


@app.route('/extra3', methods=['POST', 'GET'])
def extra3():
    return ex3.main()

@app.route('/extra4', methods=['POST', 'GET'])
def extra4():
    return ex4.main()


@app.route('/soil-map', methods=['POST', 'GET'])
def soil_map():
    if request.method == 'POST':
        coordinates = request.form.getlist('coordinates[]')
        data = session['coordinates'] = coordinates
        session['type_map'] = 'coordinate'
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(url_for('soil_map'))
            if file and allowed_file(file.filename):
                filename = 'starch_potato.kml'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session['type_map'] = 'file'
        return redirect(url_for('soil_map'))
    coordinates = []
    img = ''
    columns = []
    rows = []
    b_result = []
    b_position = []

    if session.get('type_map') != 'file':
        if session.get('coordinates'):
            for i in range(1, len(session.get('coordinates')), 2):
                coordinates.append({'x': session.get('coordinates')[i - 1], 'y': session.get('coordinates')[i]})
        if len(coordinates) > 2:
            try:
                img, columns, rows = bofek.main(coordinates)
            except Exception as ex:
                print(ex)
                error = 'Could not create geometry because of errors while reading input'
    else:
        try:
            img, columns, rows = bofek.main(coordinates, type=session.get('type_map'))
        except Exception as ex:
            print(ex)

    if len(rows) == 30:
        for r in rows[29]:
            if r == 'Staring bouwsteen':
                continue
            if r not in b_result:
                b_result.append(r)
        for b in b_result:
             b_position.append(sh2.get_position(b))

    soil_map_text = {
        'B1': 'Leemarm, zeer fijn tot matig fijn zand',
        'B2': 'Zwak lemig, zeer fijn tot matig fijn zand', 
        'B3': 'Sterk lemig, zeer fijn tot matig fijn zand',                
        'B4': 'Zeer sterk lemig, zeer fijn tot matig fijn zand',                
        'B5': 'Grof zand',                
        'B6': 'Keileem',
        'B7': 'Zeer lichte zave',
        'B8': 'Matig lichte zave',
        'B9': 'Zware zave',
        'B10': 'Lichte klei',
        'B11': 'Matig zware klei',
        'B12': 'Zeer zware klei',
        'B13': 'Zandige leem',
        'B14': 'Siltige leem',
        'B15': 'Venig zand',
        'B16': 'Zandig veen en veen',
        'B17': 'Venige kle',
        'B18': 'Kleiig veen'
    }

    return render_template('soil-map.html', coordinates=coordinates, img=img, columns=columns, rows=rows,
                           b_result=b_result, b_position=b_position, soil_map_text=soil_map_text)


@app.route('/parse-csv', methods=['POST'])
def parse_csv():
    try:
        data = request.get_json()
        csv_str = data['csv'].strip('\n').split(',')
        coordinates = []
        for coords in csv_str:
            x, y = tuple(list(coords.strip(' \n').split(' ')))
            coordinates.append({'x': x.strip(), 'y': y.strip()})

        return {'coordinates': coordinates}
    except Exception as ex:
        abort(400, ex)


@app.route('/reset-soil-map', methods=['GET', 'POST'])
def reset_soil_map():
    try:
        del session['type_map']
        del session['coordinates']
        return {}
    except KeyError:
        return {}
