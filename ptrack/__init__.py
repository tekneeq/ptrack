import os

import pymongo
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

            # data_date = datetime.datetime.strptime(data['data_date'], '%Y-%m-%d').date()
            # tz = timezone('EST')
            data_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            # inserted_id = vesto_col.insert_one(data).inserted_id

            docs = list(vesto_col.find({"data_date": {"$lt": data_date}}))

            # docs = list(vesto_col.find({"version": 1}))

            # doc_list = []
            # for doc in docs:
            #    doc_list.append(doc)
        except Exception as e:
            docs = e

        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=docs)

    @app.route('/mongo_opts', methods=['GET', 'POST'])
    def mongo_opts():
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
        opts_col = db.opts

        inserted_id = -1
        try:
            data = json.loads(request.data)

            inserted_id = opts_col.insert_one(data).inserted_id

        except Exception as e:
            pass

        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=inserted_id)

    @app.route('/lc')
    def lc():

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

        mydate = datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST')).strftime('%Y-%m-%d')

        data = vesto_col.find({'exp_date': f'{mydate}'}).sort('data_date', pymongo.ASCENDING)

        legend = 'isect for %s' % mydate
        isect = []
        times = []
        ctop = []
        ptop = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])

        mystr = f'{len(times)}, {len(isect)}, {len(ctop)}, {len(ptop)}'

        return render_template('line_chart.html', values=isect, values_ctop=ctop, values_ptop=ptop, labels=times,
                               legend=legend, processed_text=mystr)

    @app.route('/lc2')
    def lc2():

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

        mydate = datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST'))

        # Mon == 0
        # Tue == 1
        # Web == 2
        # Thur == 3
        # Fri == 4
        # Sat == 5
        # Sun == 6
        days_to_add = 1
        if mydate.weekday() == 4:
            days_to_add = 3

        # Sat
        if mydate.weekday() == 5:
            days_to_add = 2

        mydate = mydate + datetime.timedelta(days_to_add)
        mydate = mydate.strftime('%Y-%m-%d')

        data = vesto_col.find({'exp_date': f'{mydate}'}).sort('data_date', pymongo.ASCENDING)

        legend = 'isect for %s' % mydate
        isect = []
        times = []
        ctop = []
        ptop = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])

        mystr = f'{len(times)}, {len(isect)}, {len(ctop)}, {len(ptop)}'

        return render_template('line_chart.html', values=isect, values_ctop=ctop, values_ptop=ptop, labels=times,
                               legend=legend, processed_text=mystr)

    @app.route("/lcc")
    def lcc2():

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

        expdate = datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST')).strftime('%Y-%m-%d')
        data = vesto_col.find({'exp_date': f'{expdate}'}).sort('data_date', pymongo.ASCENDING)

        legend = 'ctop / ptop for %s' % expdate
        isect = []
        times = []
        ctop = []
        ptop = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])

        return render_template('line_chart_two.html', values=isect, values_ctop=ctop, values_ptop=ptop, labels=times,
                               legend=legend)

    @app.route("/lcc2")
    def lcc():

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

        expdate = datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST'))


        days_to_add = 1

        # Friday
        if expdate.weekday() == 4:
            days_to_add = 3

        # Sat
        if expdate.weekday() == 5:
            days_to_add = 2

        expdate = expdate + datetime.timedelta(days_to_add)
        expdate = expdate.strftime('%Y-%m-%d')


        data = vesto_col.find({'exp_date': f'{expdate}'}).sort('data_date', pymongo.ASCENDING)

        legend = 'ctop / ptop for %s' % expdate
        isect = []
        times = []
        ctop = []
        ptop = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])

        return render_template('line_chart_two.html', values=isect, values_ctop=ctop, values_ptop=ptop, labels=times,
                               legend=legend)

    @app.route('/lcc3')
    @app.route('/lcc3/<mydate>')
    def lcc3(mydate=datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST')).strftime('%Y-%m-%d')):

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

        data = vesto_col.find({'exp_date': f'{mydate}'}).sort('data_date', pymongo.ASCENDING)

        isect = []
        times = []
        ctop = []
        ptop = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])



        # Return the components to the HTML template
        return render_template(
            template_name_or_list='new_line_chart.html',
            ctop=ctop,
            ptop=ptop,
            labels=times,
        )

    @app.route('/lcc4')
    @app.route('/lcc4/<mydate>')
    def lcc4(mydate=datetime.datetime.now(timezone(datetime.timedelta(hours=-5), 'EST')).strftime('%Y-%m-%d')):

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

        data = vesto_col.find({'exp_date': f'{mydate}', 'version': 2}).sort('data_date', pymongo.ASCENDING)

        isect = []
        times = []
        ctop = []
        ptop = []

        cprice = []
        coi = []
        cvol = []
        cdelta = []
        cgamma = []
        cvega = []
        ctheta = []
        civ = []

        pprice = []
        poi = []
        pvol = []
        pdelta = []
        pgamma = []
        pvega = []
        ptheta = []
        piv = []



        delta = []
        gamma = []
        for d in data:
            times.append(d['data_date'])
            isect.append(d['intersection'][0])
            ctop.append(d['ctop'][1])
            ptop.append(d['ptop'][1])

            cprice.append(d['price_sum_call'])
            coi.append(d['oi_sum_call'])
            cvol.append(d['vol_sum_call'])
            cdelta.append(d['delta_sum_call'])
            cgamma.append(d['gamma_sum_call'])
            cvega.append(d['vega_avg_call'])
            ctheta.append(d['theta_avg_call'])
            civ.append(d['iv_avg_call'])

            pprice.append(d['price_sum_put'])
            poi.append(d['oi_sum_put'])
            pvol.append(d['vol_sum_put'])
            pdelta.append(d['delta_sum_put'])
            pgamma.append(d['gamma_sum_put'])
            pvega.append(d['vega_avg_put'])
            ptheta.append(d['theta_avg_put'])
            piv.append(d['iv_avg_put'])

            delta.append(d['delta_sum_call'] + d['delta_sum_put'])
            gamma.append(d['gamma_sum_call'] + d['gamma_sum_put'])

        title = f'{mydate}'

        # Return the components to the HTML template
        return render_template(
            template_name_or_list='new_new_line_chart.html',
            ctop=ctop,
            ptop=ptop,
            isect=isect,
            labels=times,
            title=title,
            cprice=cprice,
            coi=coi,
            cvol=cvol,
            cdelta=cdelta,
            cgamma=cgamma,
            cvega=cvega,
            ctheta=ctheta,
            civ=civ,
            pprice=pprice,
            poi=poi,
            pvol=pvol,
            pdelta=pdelta,
            pgamma=pgamma,
            pvega=pvega,
            ptheta=ptheta,
            piv=piv,
            delta=delta,
            gamma=gamma,
        )

    @app.route('/lcc5/<mydate>/<sprice>')
    def lcc5(mydate, sprice):

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


    @app.route('/prices')
    def prices():

        client = MongoClient(host=app.config['HOST'],
                             port=27017,
                             username=app.config['USER'],
                             password=app.config['PASSWORD'],
                             tls=True,
                             tlsAllowInvalidCertificates=True,
                             tlsCAFile='/home/ec2-user/ptrack/ptrack/rds-combined-ca-bundle.pem',
                             )
        db = client.vesto
        prices_col = db.prices

        """
        prices_data = {
          'ticker': TICKER,
          'price': ticker_price_rounded
          'data_date': data_date,
          'version': 1
        }
        """

        inserted_id = -1
        try:
            data = json.loads(request.data)

            inserted_id = prices_col.insert_one(data).inserted_id

        except Exception as e:
            pass


        return render_template("index.html", user_image="static/jpuff.png",
                               processed_text=inserted_id)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app
