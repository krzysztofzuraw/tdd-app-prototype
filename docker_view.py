import io
import os

from flask import Flask, render_template, request

from forms import MyForm
from settings import app, cli


@app.route("/", methods=['GET'])
def index_page():
    form = MyForm()
    return render_template('index.html', form=form)


@app.route("/send_code", methods=['POST'])
def execute_code():
    data = request.form['source_code']
    code = io.StringIO(data)
    create_container(code)
    output = get_code_from_docker()
    return output


def create_container(code):
    cli.create_container(
         image='python:3',
         command=['python','-c', code.getvalue()],
         volumes=['/opt'],
         host_config=cli.create_host_config(
             binds={ os.getcwd(): {
                 'bind': '/opt',
                 'mode': 'rw',
                 }
             }
         ),
         name='hello_word_from_docker',
         working_dir='/opt'
    )

def get_code_from_docker():
    cli.start('hello_word_from_docker')
    cli.wait('hello_word_from_docker')
    output = cli.logs('hello_word_from_docker')

    cli.remove_container('hello_word_from_docker', force=True)

    return "From docker: {}".format(output.strip())

if __name__ == "__main__":
    app.run(debug=True)
