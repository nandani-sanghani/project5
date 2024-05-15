import os
from settings import User
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
import sys
from settings import connect_db
from azure.identity import ManagedIdentityCredential,DefaultAzureCredential
app = Flask(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'settings')))



@app.route('/')
def index():
   user_data = User.sendData()
   
   return render_template('index.html',users={})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name') 
   if name:
       print("getting name")
       user = User.User(name)
       user.save()
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
