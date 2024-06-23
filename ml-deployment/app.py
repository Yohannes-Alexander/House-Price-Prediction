from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import pandas as pd
from babel.numbers import format_currency
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings("ignore")

app = Flask("__name__", template_folder="template")

# Load the scaler
with open("model/scaler_latest.pkl", 'rb') as f:
    loaded_scaler = pickle.load(f)
# Load the model
with open('model/model_latest.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    # Get the JSON data from the request
    data = request.get_json()
    

    data_dict = {'Kamar Tidur': data["Kamar Tidur"],
             'Kamar Mandi': data["Kamar Mandi"],
             'Luas Tanah': data["Luas Tanah"],
             'Luas Bangunan': data["Luas Bangunan"],
             'Daya Listrik': data["Daya Listrik"],
             'Dapur': data["Dapur"],
             'Jumlah Lantai': data["Jumlah Lantai"],
             'Lebar Jalan': data["Lebar Jalan"],
             'Carport': data["Carport"],
             'Kamar Pembantu': data["Kamar Pembantu"],
             'Ruang Makan': int(data["Ruang Makan"]),
             'Ruang Tamu': int(data["Ruang Tamu"]),
             'Kondisi Perabotan': int(data["Kondisi Perabotan"]),
             'Terjangkau Internet': int(data["Terjangkau Internet"]),
             'Hook': int(data["Hook"]),
             'Kondisi Properti': int(data["Kondisi Properti"]),
             'HGB - Hak Guna Bangunan': None,
             'HP - Hak Pakai': None,
             'HS - Hak Sewa': None,
             'Lainnya (PPJB,Girik,Adat,dll)': None,
             'SHM - Sertifikat Hak Milik': None,
             'PAM atau PDAM': None,
             'Sumur Bor': None,
             'Sumur Galian': None,
             'Sumur Pompa': None,
             'Sumur Resapan': None,
             'Jakarta Barat': None,
             'Jakarta Pusat': None,
             'Jakarta Selatan': None,
             'Jakarta Timur': None,
             'Jakarta Utara': None,
             'Cakung': None,
             'Cempaka Putih': None,
             'Cengkareng': None,
             'Cilandak': None,
             'Cilincing': None,
             'Cipayung': None,
             'Ciracas': None,
             'Duren Sawit': None,
             'Gambir': None,
             'Grogol Petamburan': None,
             'Jagakarsa': None,
             'Jatinegara': None,
             'Johar Baru': None,
             'Kalideres': None,
             'Kebayoran Baru': None,
             'Kebayoran Lama': None,
             'Kebon Jeruk': None,
             'Kelapa Gading': None,
             'Kemayoran': None,
             'Kembangan': None,
             'Koja': None,
             'Kramat Jati': None,
             'Makasar': None,
             'Mampang Prapatan': None,
             'Matraman': None,
             'Menteng': None,
             'Pademangan': None,
             'Palmerah': None,
             'Pancoran': None,
             'Pasar Minggu': None,
             'Pasar Rebo': None,
             'Penjaringan': None,
             'Pesanggrahan': None,
             'Pulo Gadung': None,
             'Sawah Besar': None,
             'Senen': None,
             'Setiabudi': None,
             'Taman Sari': None,
             'Tambora': None,
             'Tanah Abang': None,
             'Tanjung Priok': None,
             'Tebet': None
        }
    
    sertifikat = data["Sertifikat"]
    sertifikat_dict = {
        "SHM - Sertifikat Hak Milik": 0,
        'HGB - Hak Guna Bangunan': 0,
        'HP - Hak Pakai': 0,
        'HS - Hak Sewa': 0,
        'Lainnya (PPJB,Girik,Adat,dll)': 0
    }

    # Update the dictionary values
    for key in sertifikat_dict:
        data_dict[key] = 1 if key == sertifikat else 0

    water_source = data["water_source"]
    water_source_dict = {
        'PAM atau PDAM': 0,
        'Sumur Bor': 0,
        'Sumur Galian': 0,
        'Sumur Pompa': 0,
        'Sumur Resapan': 0
    }

    # Update the dictionary values
    for key in water_source_dict:
        data_dict[key] = 1 if key == water_source else 0


    # The region you want to set
    region = data["region"]
    region_dict = {
        'Jakarta Barat': 0,
        'Jakarta Pusat': 0,
        'Jakarta Selatan': 0,
        'Jakarta Timur': 0,
        'Jakarta Utara': 0
    }
    # Set the value of the specific region to 1, others remain 0
    for key in region_dict:
        data_dict[key] = 1 if key == region else 0


    kecamatan = data["kecamatan"]
    kecamatan_list = [
        'Cakung', 'Cempaka Putih', 'Cengkareng', 'Cilandak', 'Cilincing', 'Cipayung', 
        'Ciracas', 'Duren Sawit', 'Gambir', 'Grogol Petamburan', 'Jagakarsa', 
        'Jatinegara', 'Johar Baru', 'Kalideres', 'Kebayoran Baru', 'Kebayoran Lama',
        'Kebon Jeruk', 'Kelapa Gading', 'Kemayoran', 'Kembangan', 'Koja',
        'Kramat Jati', 'Makasar', 'Mampang Prapatan', 'Matraman', 'Menteng',
        'Pademangan', 'Palmerah', 'Pancoran', 'Pasar Minggu', 'Pasar Rebo',
        'Penjaringan', 'Pesanggrahan', 'Pulo Gadung', 'Sawah Besar', 'Senen',
        'Setiabudi', 'Taman Sari', 'Tambora', 'Tanah Abang', 'Tanjung Priok',
        'Tebet'
    ]

    for key in kecamatan_list:
        data_dict[key] = 1 if key == kecamatan else 0
        
    numeric_column = ["Kamar Tidur", "Kamar Mandi", "Luas Tanah", "Luas Bangunan", 
                  "Daya Listrik", "Dapur", "Jumlah Lantai", "Lebar Jalan", "Carport", "Kamar Pembantu"]

    row_df = pd.DataFrame([data_dict])
    row_df[numeric_column] = loaded_scaler.transform(row_df[numeric_column])
    # Make a prediction
    prediction = loaded_model.predict(row_df)

    # Return the prediction as a JSON response
    return jsonify({'prediction': format_currency(np.abs(prediction[0]), 'IDR', locale='id_ID')})

if __name__ == '__main__':
    app.run(port=8080, threaded=True)

