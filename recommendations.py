# recommendations.py
import pandas as pd
import numpy as np
import pickle
import requests
from sklearn.decomposition import TruncatedSVD

# Cargar el modelo de SVD
with open('svd_model.pkl', 'rb') as f:
    SVD = pickle.load(f)

# Cargar el scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def get_product_details(product_id):
    url = f"https://back-estetica-production-710f.up.railway.app/api/v1/products/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_sales_data():
    sales_url = "https://back-estetica-production-710f.up.railway.app/api/v1/sales"
    response = requests.get(sales_url)
    response.raise_for_status()
    data = response.json()

    rows = []
    for sale in data:
        for detail in sale["Detalle_ventas"]:
            row = {
                "id_sale": sale["id"],
                "id_user": sale["id_user"],
                "id_detail": detail["id"],
                "id_product": detail["Producto"]["id"],
                "amount": detail["amount"],
                "name": detail["Producto"]["name"],
                "price": detail["Producto"]["price"],
                "Categoria": detail["Producto"]["Categoria"]["name"],
                "Marca": detail["Producto"]["Marca"]["name"]
            }
            rows.append(row)

    df_clean = pd.DataFrame(rows)
    return df_clean

def get_recommendations(user_id):
    df_clean = get_sales_data()
    df_recsys = df_clean[['id_user', 'id_product', 'amount', 'name']]

    total_products_per_user = df_recsys.groupby(['id_user', 'id_product', 'name'])['amount'].sum().reset_index()

    X = total_products_per_user.pivot_table(values='amount', index='id_product', columns='id_user', fill_value=0)

    # Normalizar y transformar los datos usando el scaler y el modelo de SVD cargados
    X_normalized = scaler.transform(X)
    U = SVD.transform(X_normalized)
    Sigma = SVD.singular_values_
    VT = SVD.components_

    Sigma_matrix = np.diag(Sigma)
    X_approx = np.dot(U, np.dot(Sigma_matrix, VT))

    X_approx_original_scale = scaler.inverse_transform(X_approx)
    X_approx_df = pd.DataFrame(X_approx_original_scale, index=X.index, columns=X.columns)

    def recommend_items_svd_with_percentage(user_id, original_matrix, approx_matrix, num_recommendations=5):
        user_idx = original_matrix.columns.get_loc(user_id)
        user_ratings = approx_matrix.iloc[:, user_idx]

        unseen_items = original_matrix.index[original_matrix.iloc[:, user_idx] == 0]
        unseen_ratings = user_ratings[unseen_items]
        recommended_items = unseen_ratings.sort_values(ascending=False).head(num_recommendations)

        total_score = recommended_items.sum()
        percentage_relation = (recommended_items / total_score) * 100

        recommendations_df = pd.DataFrame({
            'predicted_rating': recommended_items,
            'percentage_relation': percentage_relation
        })

        # Añadir detalles del producto desde la API
        recommendations = []
        for idx in recommendations_df.index:
            product_details = get_product_details(idx)
            if product_details:
                recommendations.append({
                    'predicted_rating': recommendations_df.loc[idx, 'predicted_rating'],
                    'percentage_relation': recommendations_df.loc[idx, 'percentage_relation'],
                    'product_name': product_details['name'],
                    'image_url': product_details['image']
                })

        return recommendations

    recommendations_with_percentage = recommend_items_svd_with_percentage(user_id, X, X_approx_df)
    return recommendations_with_percentage
