from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    html_content = """
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <title>Información del Alumno</title>
        <style>
          body { font-family: Arial, sans-serif; }
          .container { margin: 50px; }
          .info { margin-bottom: 20px; }
          .form-group { margin-bottom: 10px; }
          label { display: block; margin-bottom: 5px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="info">
            <p>Alumno: Angel Wenceslao Hernández Hernández</p>
            <p>Grupo: '9A'</p>
          </div>
          <div class="image">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/800px-Python.svg.png" alt="Python" />
          </div>
          <div class="form">
            <h2>Enviar un Mensaje</h2>
            <form action="/submit" method="post">
              <div class="form-group">
                <label for="name">Nombre:</label>
                <input type="text" id="name" name="name">
              </div>
              <div class="form-group">
                <label for="message">Mensaje:</label>
                <textarea id="message" name="message"></textarea>
              </div>
              <button type="submit">Enviar</button>
            </form>
          </div>
        </div>
      </body>
    </html>
    """
    return render_template_string(html_content)
    # return "Alumno: Angel Wenceslao Hernández Hernández<br>Grupo: '9A'"

@app.route('/submit', methods=['POST'])
def submit():
    # Aquí podrías manejar los datos enviados por el formulario
    return "Mensaje enviado exitosamente"

if __name__ == '__main__':
    app.run(debug=True)