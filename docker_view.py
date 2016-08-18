import os
from flask import Flask, request, render_template
from docker import Client

app = Flask(__name__)
cli = Client(base_url='unix://var/run/docker.sock')


@app.route("/", methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/send_code", methods=['POST'])
def get_code():
    data = request.form['code_to_send']
    file_path = write_code_to_file_and_return_path(data)
    output = create_container(file_path)
    return output

def write_code_to_file_and_return_path(code):
    with open(os.path.join(os.getcwd(), 'python_code_to_execute.py'), 'w') as f:
        f.write(code)
    return f.name


def build_image():
    response = [line for line in cli.build(
        path=os.getcwd(), tag='my_docker'
    )]
    return response

def create_container(command):
    cli.create_container(
         image='my_docker',
         command=[os.path.basename(command)],
         volumes=['/opt'],
         host_config=cli.create_host_config(
             binds={ os.getcwd(): {
                 'bind': '/opt',
                 'mode': 'rw',
                 }
             }
         ),
         name='hello_word_from_docker'
    )
    cli.start('hello_word_from_docker')
    cli.wait('hello_word_from_docker')
    output = cli.logs('hello_word_from_docker')

    cli.remove_container('hello_word_from_docker', force=True)

    return "From docker: {}".format(output.strip())

if __name__ == "__main__":
    app.run(debug=True)
