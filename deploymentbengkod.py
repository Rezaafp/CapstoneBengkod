# -*- coding: utf-8 -*-
"""DeploymentBengkod.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lqsEPbV0hoxvn_2-hKaBQjuSDg7XTcWO
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import streamlit as st
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,recall_score,f1_score,precision_score,roc_auc_score,confusion_matrix,precision_score
import pickle  # Import library pickle
import os  # Import library os

water_potability_df = pd.read_csv('https://drive.google.com/uc?id=1cWZzfVkEw3xMcIanmtb-xi-7nVBKjMRl')
# ... (kode untuk memuat model dan data) ...
# Mengisi kolom numerik dengan mean
water_potability_df.fillna(water_potability_df.mean(), inplace=True)

# Menampilkan data frame
st.write("## Data Frame")
st.dataframe(water_potability_df)

# Membuat histogram
st.write("## Histogram")
numerical_features = water_potability_df.select_dtypes(include=['int64', 'float64']).columns
selected_feature = st.selectbox("Pilih fitur numerik:", numerical_features)
fig, ax = plt.subplots()
sns.histplot(water_potability_df[selected_feature], bins=20, color='blue', kde=True, ax=ax)
ax.set_title(f'Distribusi {selected_feature}', fontsize=16)
ax.set_xlabel(selected_feature)
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Membuat boxplot
st.write("## Boxplot")
selected_feature = st.selectbox("Pilih fitur numerik untuk boxplot:", numerical_features)
fig, ax = plt.subplots()
sns.boxplot(y=water_potability_df[selected_feature], ax=ax)
ax.set_title(f'Boxplot of {selected_feature}')
ax.set_ylabel(selected_feature)
st.pyplot(fig)

# Membuat heatmap korelasi
st.write("## Heatmap Korelasi")
corr_matrix = water_potability_df.corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title('Korelasi Heatmap untuk Data Kualitas Air')
st.pyplot(fig)

# Pilihan model
model_choice = st.selectbox("Pilih Model:", ["Naive Bayes", "Decision Tree", "Random Forest"])

# --- Load Model ---
# (Pastikan model-model telah disimpan sebelumnya)
clean_classifier_nb = GaussianNB()  # Load model Naive Bayes
clean_classifier_dt = DecisionTreeClassifier(random_state=42)  # Load model Decision Tree
clean_classifier_rf = RandomForestClassifier(n_estimators=100, random_state=42)  # Load model Random Forest

# --- Pisahkan Fitur dan Target ---
X = water_potability_df[['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']]
y = water_potability_df['Potability']

# --- Bagi data menjadi data training dan testing ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Bagi data dengan rasio 80:20


# --- Input ---
st.title("Prediksi Kualitas Air")
st.write("Pilih Model yang akan digunakan untuk memprediksi kelayakan air minum")
# Muat semua model
models = {
    "Naive Bayes": pickle.load(open("model_naive_bayes.pkl", "rb")),  # Ganti dengan nama file model Naive Bayes
    "Decision Tree": pickle.load(open("model_decision_tree.pkl", "rb")),  # Ganti dengan nama file model Decision Tree
    "Random Forest": pickle.load(open("model_random_forest.pkl", "rb"))  # Ganti dengan nama file model Random Forest
}

# Pilihan model
selected_model = st.selectbox("Pilih Model", list(models.keys()))

st.write("Masukkan nilai untuk masing-masing fitur di bawah ini lalu klik tombol prediksi untuk mengetahui apakah air layak diminum")

# Input fitur
ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)
Hardness = st.number_input("Hardness", min_value=0.0, max_value=300.0, value=150.0)
Solids = st.number_input("Solids", min_value=0.0, max_value=60000.0, value=20000.0)
Chloramines = st.number_input("Chloramines", min_value=0.0, max_value=15.0, value=7.0)
Sulfate = st.number_input("Sulfate", min_value=0.0, max_value=500.0, value=250.0)
Conductivity = st.number_input("Conductivity", min_value=0.0, max_value=800.0, value=400.0)
Organic_carbon = st.number_input("Organic_carbon", min_value=0.0, max_value=30.0, value=15.0)
Trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0, max_value=120.0, value=60.0)
Turbidity = st.number_input("Turbidity", min_value=0.0, max_value=7.0, value=3.5)

# Tombol prediksi
if st.button("Prediksi"):
    # Buat DataFrame dari input fitur
    input_data = pd.DataFrame({
        'ph': [ph],
        'Hardness': [Hardness],
        'Solids': [Solids],
        'Chloramines': [Chloramines],
        'Sulfate': [Sulfate],
        'Conductivity': [Conductivity],
        'Organic_carbon': [Organic_carbon],
        'Trihalomethanes': [Trihalomethanes],
        'Turbidity': [Turbidity]
    })

    # Prediksi
    prediction = models[selected_model].predict(input_data)[0]

    # Tampilkan hasil prediksi
    if prediction == 1:
        st.success("Air layak diminum")
    else:
        st.error("Air tidak layak diminum")
