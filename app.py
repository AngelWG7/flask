from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['user']
    saludo = f"Bienvenido, {nombre} :)"
    return render_template('greeting.html', saludo=saludo)

if __name__ == '__main__':
    app.run(debug=True)