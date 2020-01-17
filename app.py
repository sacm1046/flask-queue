import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db
from adminqueue import AdminQueue

'''for find the place of the file that we are executing '''
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 

app = Flask(__name__)
''' for the case that i forget de slash on the endpoint '''
app.url_map.strict_slashes = False 
''' for the show or not the errors '''
app.config['DEBUG'] = True
''' for configuration of the environment '''
app.config['ENV'] = 'development'

'''for define my database route and configuration'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
'''is required when i use SQLALCHEMY and for delete not important changes '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

''' for configuration of command to migrate '''
db.init_app(app)
migrate = Migrate(app, db)

''' for start de liveServer '''
manager = Manager(app)
''' run for console the migrate command '''
manager.add_command('db',MigrateCommand)
''' for use the development environment '''
CORS(app)

q=AdminQueue()
''' for define the route for default '''
@app.route('/')
def home():
    return render_template('index.htm', name='home')

@app.route('/new', methods=['POST'])
def enqueue():
    if not request.json.get('name'):
        return jsonify({"name":"Is required"}), 404
    if not request.json.get('phone'):
        return jsonify({"phone":"Is required"}), 404 

    item={
        "name":"sebastian",
        "phone":"+569 8762 1321"
    }
    msg = q.enqueue(item)
    return jsonify({"msg":"Add to list"}), 200

@app.route('/next', methods=['GET'])
def dequeue():
    item = q.dequeue()
    return jsonify({"msg":"Processed in the next queue","item":item}), 200

@app.route('/all', methods=['GET'])
def queue():
    fila = q.get_queue()
    return jsonify({fila}), 200

''' for start my app'''
if __name__=='__main__':
    manager.run()


