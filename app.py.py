# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 12:26:13 2025

@author: suresh
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Beam Deflection Analysis Web App")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl', header=1)
    df.columns = [str(col).strip().replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]

    if 'Unnamed:_0' in df.columns:
        df.drop(columns=['Unnamed:_0'], inplace=True)

    df['Load_kN'] = pd.to_numeric(df['Load_kN'], errors='coerce')
    df['Deflection_mm'] = pd.to_numeric(df['Deflection_mm'], errors='coerce')
    df['Span_m'] = pd.to_numeric(df['Span_m'], errors='coerce')
    df.dropna(subset=['Load_kN', 'Deflection_mm', 'Span_m', 'Material_Type'], inplace=True)

    st.subheader("📊 Data Preview")
    st.write(df.head())

    st.subheader("📈 Linear Regression")
    X = df[['Load_kN']]
    y = df['Deflection_mm']
    model = LinearRegression()
    model.fit(X, y)
    st.write(f"**Regression Equation:** Deflection = {model.coef_[0]:.2f} * Load + {model.intercept_:.2f}")
    st.write(f"**R² Score:** {model.score(X, y):.4f}")

    st.subheader("📉 Load vs Deflection by Material")
    sns.lineplot(data=df, x='Load_kN', y='Deflection_mm', hue='Material_Type', marker='o')
    plt.xlabel("Load (kN)")
    plt.ylabel("Deflection (mm)")
    st.pyplot()

    st.subheader("📊 Average Deflection by Material")
    avg_def = df.groupby('Material_Type')['Deflection_mm'].mean()
    st.bar_chart(avg_def)
