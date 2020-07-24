from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/birthday', methods=['POST'])
def set_birthday():
    """This section is where a birthday will come in.  We should be able to get the following args out of it;
        username=
        birthday=
    ------FUTURE------
        Face Colors = (format of RUBWG)
    """


