from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Alumno: Angel Wenceslao Hernández Hernández<br>Grupo: '9A'"

if __name__ == '__main__':
    app.run(debug=True)