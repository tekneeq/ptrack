import os

from flask import Flask, render_template, request, json, Response
import time
import datetime

from pymongo import MongoClient
from datetime import timezone


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    """
    app = flask.Flask(__name__, static_url_path='',
                      static_folder='static',
                      template_folder='template')
    """

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'ptrack.sqlite'),
        SECRET_KEY='dev'
    )

    IMG_FOLDER = os.path.join('ptrack', 'images')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER

    if test_config is None:
        # load the instance config, if it exists, when not testing
        print("Loading config from config.py")
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/noclip')
    def hidden():
        return render_template("index.html", user_image="static/1.combined.png",
                               processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip2')
    def noclip():
        return render_template("index.html", user_image="static/2.combined.png",
                               processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip3')
    def noclip3():
        return render_template("index.html", user_image="static/3.combined.png",
                               processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip4')
    def noclip4():
        return render_template("index.html", user_image="static/4.combined.png",
                               processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/progress')
    def progress():
        def generate():
            x = 0

            while x <= 100:
                yield "data:" + str(x) + "\n\n"
                x = x + 10
                time.sleep(0.5)

        return Response(generate(), mimetype='text/event-stream')

    @app.route('/chart')
    def chart():
        return render_template("chartme.html", data="hello")

    @app.route('/mongo', methods=['GET', 'POST'])
    def mongo():
        import pymongo

        client = MongoClient(host=app.config['HOST'],
                             port=27017,
                             username=app.config['USER'],
                             password=app.config['PASSWORD'],
                             tls=True,
                             tlsAllowInvalidCertificates=True,
                             tlsCAFile='/home/ec2-user/ptrack/ptrack/rds-combined-ca-bundle.pem',
                             )
        db = client.vesto
        vesto_col = db.vesto

        # curl -X POST -H "Content-type: application/json" -d "{\"firstName\" : \"Jo"lastName\" : \"Smith\"}" http://ptrackit.com/mongo
        data = "No data"
        try:
            data = json.loads(request.data)

            intersection = data['intersection']
            ptop = data['ptop']
            pbot = data['pbot']

            ctop = data['ctop']
            cbot = data['cbot']

            data_date = datetime.datetime.strptime(data['data_date'], '%Y-%m-%dT%H:%M:%S').date()
            version = data['version']

            inserted_id = vesto_col.insert_one(data).inserted_id

        except:
            pass

        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=inserted_id)

    @app.route('/mongo_delete', methods=['GET', 'POST'])
    def mongo_delete():
        import pymongo

        client = MongoClient(host=app.config['HOST'],
                             port=27017,
                             username=app.config['USER'],
                             password=app.config['PASSWORD'],
                             tls=True,
                             tlsAllowInvalidCertificates=True,
                             tlsCAFile='/home/ec2-user/ptrack/ptrack/rds-combined-ca-bundle.pem',
                             )
        db = client.vesto
        vesto_col = db.vesto

        # curl -X POST -H "Content-type: application/json" -d "{\"firstName\" : \"Jo"lastName\" : \"Smith\"}" http://ptrackit.com/mongo
        data = "No data"
        docs = -1
        try:
            data = json.loads(request.data)


            data_date = datetime.datetime.strptime(data['data_date'], '%Y-%m-%d').date()


            # inserted_id = vesto_col.insert_one(data).inserted_id

            docs = list(vesto_col.find({"date": {"$lt": data_date}}))

            #docs = list(vesto_col.find({"version": 1}))

            #doc_list = []
            #for doc in docs:
            #    doc_list.append(doc)
        except Exception as e:
            docs = e

        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=docs)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app
