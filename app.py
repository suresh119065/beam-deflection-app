
# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Beam Deflection App", layout="centered")

st.title("📊 Beam Deflection Analysis Web App")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Beam Deflection Data (Excel file)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl', header=1)  # Skip first row

    # Clean column names
    df.columns = [str(col).strip().replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]
    
    if 'Unnamed:_0' in df.columns:
        df.drop(columns=['Unnamed:_0'], inplace=True)

    # Convert columns
    df['Load_kN'] = pd.to_numeric(df['Load_kN'], errors='coerce')
    df['Deflection_mm'] = pd.to_numeric(df['Deflection_mm'], errors='coerce')
    df['Span_m'] = pd.to_numeric(df['Span_m'], errors='coerce')
    df.dropna(subset=['Load_kN', 'Deflection_mm', 'Span_m', 'Material_Type'], inplace=True)

    st.subheader("📈 Linear Regression")

    # Linear Regression
    X = df[['Load_kN']]
    y = df['Deflection_mm']
    model = LinearRegression()
    model.fit(X, y)

    coef = model.coef_[0]
    intercept = model.intercept_
    r2 = model.score(X, y)

    st.markdown(f"**Regression Equation:** Deflection = {coef:.2f} * Load + {intercept:.2f}")
    st.markdown(f"**R² Score:** {r2:.4f}")

    # Grouped average deflection
    avg_def = df.groupby('Material_Type')['Deflection_mm'].mean()

    st.subheader("📉 Load vs Deflection by Material")

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=df, x='Load_kN', y='Deflection_mm', hue='Material_Type', marker='o', ax=ax1)
    ax1.set_title("Load vs Deflection by Material")
    ax1.set_xlabel("Load (kN)")
    ax1.set_ylabel("Deflection (mm)")
    st.pyplot(fig1)

    st.subheader("📊 Average Deflection by Material")

    fig2, ax2 = plt.subplots()
    avg_def.plot(kind='bar', ax=ax2, color=['steelblue', 'gray', 'orange'])
    ax2.set_title("Average Deflection by Material")
    ax2.set_ylabel("Deflection (mm)")
    st.pyplot(fig2)
