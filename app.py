import os
import json
import datetime

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_header = db.Column(db.String)
    raw_data = db.Column(db.String)
    raw_form = db.Column(db.String)

    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.raw_header + '\n' + self.raw_data + '\n' + self.raw_form

    def serialize(self):
        return {
                'time': str(self.time),
                'header': self.raw_header,
                'data': self.raw_data,
                'form': self.raw_form
                }


@app.route('/', methods=['POST', 'GET'])
def index():
    newrequest = Request(raw_header=str(request.headers), raw_data=str(request.data), raw_form=str(request.form))
    db.session.add(newrequest)
    db.session.commit()
    return render_template('index.html')

@app.route('/api/requests', methods=['GET'])
def get_requests():
    requests = Request.query.all()
    requests = reversed(requests)
    return json.dumps([x.serialize() for x in requests])
