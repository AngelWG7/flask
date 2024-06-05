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
          .container { margin: 50px auto; text-align: center; max-width: 800px; }
          .info { margin-bottom: 20px; }
          .info p { margin: 5px 0; }
          .info .bold { font-weight: bold; }
          .content { display: flex; justify-content: center; align-items: flex-start; gap: 20px; }
          .image img { width: 150px; height: auto; }
          .form { border: 1px solid #ccc; padding: 20px; border-radius: 10px; background-color: #f9f9f9; width: 100%; max-width: 500px; text-align: left; }
          .form h2 { margin-top: 0; }
          .form-group { margin-bottom: 15px; }
          label { display: block; margin-bottom: 5px; }
          input, textarea { width: 100%; padding: 8px; box-sizing: border-box; }
          button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
          button:hover { background-color: #45a049; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="info">
            <p><span class="bold">Alumno:</span> Angel Wenceslao Hernández Hernández</p>
            <p><span class="bold">Grupo:</span> '9A'</p>
          </div>
          <div class="content">
            <div class="image">
              <img src="https://via.placeholder.com/150" alt="Foto del Alumno" />
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
        </div>
      </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/submit', methods=['POST'])
def submit():
    # Aquí podrías manejar los datos enviados por el formulario
    return "Mensaje enviado exitosamente"

if __name__ == '__main__':
    app.run(debug=True)