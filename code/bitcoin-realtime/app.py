from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, url_for, g, render_template, flash, redirect, jsonify, request, \
    make_response, request, current_app, Response
from flask.ext.pymongo import PyMongo
import logging


app = Flask(__name__)

# connect to another MongoDB server altogether
app.secret_key = 'many random bytes'
app.config['PBDB_HOST'] = 'mongodb://ec2-54-152-102-95.compute-1.amazonaws.com'
app.config['PBDB_PORT'] = 27017
app.config['PBDB_DBNAME'] = 'playbrush'
pb_db = PyMongo(app, config_prefix='PBDB')

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')


########################################################################################################################

@app.route('/')
def index():
    return render_template('index1.html')


########################################################################################################################

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')


########################################################################################################################


"""
Initiate the application
"""

if __name__ == '__main__':
    app.run(debug=True)
