from flask import Response,Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import os
import json
import helper.convert as convert
import yaml
import logging
import subprocess
import time
from flask_sqlalchemy import SQLAlchemy
import uuid
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'fd59f7f9-33f0-41fa-a28b-7746a1b4bb7e'

FORMAT = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(level=logging.INFO, filename="bucket.log", format=FORMAT)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            message = json.dumps({'message' : 'Token is missing'})
            return Response(message, status=401, mimetype='application/json')
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            message = json.dumps({'message' : 'Token is invalid'})
            return Response(message, status=401, mimetype='application/json')
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated




class Logging(Resource):
    @app.route('/logging', methods =['GET'])
    def get():
        # return our data and 200 OK HTTP code
        return {'data': convert.Logs}, 200
    
    @app.route('/logging', methods =['POST'])
    @token_required
    def post(current_user): 
        # Storing JSON payload
        try:
            content = request.get_json(force=True)
            logging.info(f"Post request received ")
            source = content['DEFAULT']['source']
            with open('source.txt','w') as f:
                f.write(source)
            
            # Conversion to YAML 
            ff = open('config.yml', 'w+')
            yaml.dump(content, ff, allow_unicode=True)
            logging.info(f"started at {time.strftime('%X')}")
            logging.info("YAML file created from JSON Payload : POST")
            logging.info(f"finished at {time.strftime('%X')}")

            # Fetching files from source
            if (source.find("github") == -1):
                print("executing mounting bucket")
                logging.info("executing mounting bucket: gcsmount.sh")
                logging.info(f"started at {time.strftime('%X')}")
                subprocess.run ("./gcsmount.sh")
                logging.info(f"finished at {time.strftime('%X')}")
            else:
                subprocess.run("./gitclone.sh")
                logging.info("executing repo clone : gitclone.sh")
                logging.info(f"started at {time.strftime('%X')}")
                logging.info(f"finished at {time.strftime('%X')}")
            logging.info("Calling main function")
            # Calling convert logic main function
            logging.info(f"started at {time.strftime('%X')}")
            convert.main()
        except:
            message = json.dumps({'message' : 'Conversion failed'})
            return Response(message, status=401, mimetype='application/json')
        return "Execution completed"

  
# signup route
@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    db.create_all()
    db.session.commit()
    data = request.form
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
        # database ORM object
    user = User(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email
        )
        # insert user
    db.session.add(user)
    db.session.commit()
  
    token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
    return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))