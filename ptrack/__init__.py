import os

from flask import Flask, render_template


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
        myimg = os.path.join(app.config['UPLOAD_FOLDER'], '1.combined.png')
        mytext = 'no homie'
        if os.path.isfile(myimg):
            mytext = 'yes homie'
        return render_template("index.html", user_image="static/1.combined.png", processed_text=mytext)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app