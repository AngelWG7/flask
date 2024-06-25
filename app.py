from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
from tensorflow.keras.models import load_model
import logging

app = Flask(__name__)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

# Cargar el modelo entrenado
# model = joblib.load('modelo.pkl')
model = load_model('modelo.h5')
app.logger.debug('Modelo cargado correctamente.')

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos enviados en el request
        season = int(request.form['season'])
        yr = int(request.form['yr'])
        weathersit = int(request.form['weathersit'])
        atemp = float(request.form['atemp'])
        hum = float(request.form['hum'])
        
        # Crear un DataFrame con los datos
        data_df = pd.DataFrame([[atemp, yr, season, hum, weathersit]], columns=['atemp', 'yr', 'season', 'hum', 'weathersit'])
        app.logger.debug(f'DataFrame creado: {data_df}')
        
        # Realizar predicciones
        prediction = model.predict(data_df)
        app.logger.debug(f'Predicción: {prediction[0]}')
        

        # Convertir la predicción a una lista para serialización JSON
        prediction_list = prediction[0].tolist()
        
        # Devolver las predicciones como respuesta JSON
        return jsonify({'categoria': prediction_list})

    except Exception as e:
        app.logger.error(f'Error en la predicción: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

