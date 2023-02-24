import os

from flask import Flask, render_template
import datetime

from pymongo import MongoClient


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
        return render_template("index.html", user_image="static/1.combined.png", processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip2')
    def noclip():
        return render_template("index.html", user_image="static/2.combined.png", processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip3')
    def noclip3():
        return render_template("index.html", user_image="static/3.combined.png", processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/noclip4')
    def noclip4():
        return render_template("index.html", user_image="static/4.combined.png", processed_text=datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S"))

    @app.route('/mongo')
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
        col = db.list_collection_names()

        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=col)


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app