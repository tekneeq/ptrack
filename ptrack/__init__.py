import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'ptrack.sqlite'),
        SECRET_KEY='dev'
    )

    app.config['IMG_DIR'] = os.path.join('images')

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
        full_filename = os.path.join(app.config['IMG_DIR'], '1.combined.png')
        return render_template("index.html")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app