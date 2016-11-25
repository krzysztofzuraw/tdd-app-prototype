from docker import Client
from flask import Flask
from flask.ext.codemirror import CodeMirror

cli = Client(base_url='unix://var/run/docker.sock')
SECRET_KEY = 'secret!'
# mandatory
CODEMIRROR_LANGUAGES = ['python', 'html']
app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)
