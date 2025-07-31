# app.py

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VIKOR-Stocks", layout="wide")

st.title("📊 VIKOR-Stocks: Intelligent Stock Ranking System")
st.markdown("Using VIKOR MCDM method for ranking stock alternatives based on multiple criteria.")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV File (Alternatives x Criteria)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📁 Raw Data")
    st.dataframe(df)

    # Extract criteria matrix
    criteria_df = df.iloc[:, 1:].copy()
    alternatives = df.iloc[:, 0].values

    # Step 1: Normalize the decision matrix
    st.markdown("### Step 1: Normalize the Decision Matrix")
    norm_df = (criteria_df - criteria_df.min()) / (criteria_df.max() - criteria_df.min())
    st.dataframe(norm_df)

    # Step 2: Determine best and worst values
    st.markdown("### Step 2: Determine Best and Worst Values")
    f_star = norm_df.max()
    f_minus = norm_df.min()
    st.write("Best values (f*):", f_star)
    st.write("Worst values (f-):", f_minus)

    # Step 3: Compute S and R
    st.markdown("### Step 3: Compute Group Utility (S) and Individual Regret (R)")
    S = ((f_star - norm_df) / (f_star - f_minus)).sum(axis=1)
    R = ((f_star - norm_df) / (f_star - f_minus)).max(axis=1)
    st.write("S values:", S)
    st.write("R values:", R)

    # Step 4: Compute Q (VIKOR index)
    st.markdown("### Step 4: Compute Compromise Index (Q)")
    v = 0.5  # Weighting factor
    S_star, S_minus = S.min(), S.max()
    R_star, R_minus = R.min(), R.max()
    Q = v * (S - S_star) / (S_minus - S_star) + (1 - v) * (R - R_star) / (R_minus - R_star)
    st.write("Q values:", Q)

    # Result
    result_df = pd.DataFrame({
        'Alternative': alternatives,
        'S': S,
        'R': R,
        'Q': Q
    })

    result_df = result_df.sort_values('Q').reset_index(drop=True)

    st.subheader("📈 VIKOR Ranking Result")
    st.dataframe(result_df)
    st.success(f"🏆 Best choice: **{result_df.iloc[0]['Alternative']}**")

else:
    st.info("Please upload a CSV file with the first column as alternatives, followed by numeric criteria columns.")
