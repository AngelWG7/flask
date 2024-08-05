# app.py
from flask import Flask, request, render_template
import pandas as pd
from recommendations import get_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    recommendations = []
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        recommendations = get_recommendations(user_id)
    return render_template('form.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)