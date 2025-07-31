import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VIKOR-Stocks", layout="wide")

st.title("📊 VIKOR-Stocks: Intelligent Stock Ranking System")
st.markdown("Using VIKOR MCDM method for ranking stock alternatives based on multiple criteria.")

# Upload CSV file
uploaded_file = st.file_uploader("📂 Upload CSV file (First column = Alternatives, rest = Criteria)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📁 Raw Data")
    st.dataframe(df)

    alternatives = df.iloc[:, 0].values  # Alternatives
    criteria = df.iloc[:, 1:]  # Criteria data
    criteria_names = criteria.columns

    # Define which criteria are benefit or cost
    benefit_criteria = ['EPS', 'DPS', 'NTA', 'DY', 'ROE']  # Higher is better
    cost_criteria = ['PE', 'PTBV']  # Lower is better

    weights = np.ones(len(criteria.columns)) / len(criteria.columns)  # Equal weights

    # Step 1: Normalize Decision Matrix (min-max normalization)
    norm = pd.DataFrame()
    for col in criteria.columns:
        if col in benefit_criteria:
            norm[col] = (criteria[col] - criteria[col].min()) / (criteria[col].max() - criteria[col].min())
        elif col in cost_criteria:
            norm[col] = (criteria[col].max() - criteria[col]) / (criteria[col].max() - criteria[col].min())
    st.markdown("### ✅ Step 1: Normalized Matrix")
    st.dataframe(norm)

    # Step 2: Determine best and worst values
    f_star = norm.max()
    f_minus = norm.min()
    st.markdown("### ⭐ Step 2: Best (f*) and Worst (f-) Values")
    st.write("Best values (f*):")
    st.write(f_star)
    st.write("Worst values (f-):")
    st.write(f_minus)

    # Step 3: Compute S and R
    S = ((weights * (f_star - norm) / (f_star - f_minus + 1e-9)).sum(axis=1))
    R = ((weights * (f_star - norm) / (f_star - f_minus + 1e-9)).max(axis=1))
    st.markdown("### 📉 Step 3: Utility (Sᵢ) and Regret (Rᵢ)")
    st.write("S (Group utility):", S)
    st.write("R (Individual regret):", R)

    # Step 4: Compute Q index
    v = 0.5  # Strategy weight
    S_star, S_minus = S.min(), S.max()
    R_star, R_minus = R.min(), R.max()

    Q = v * (S - S_star) / (S_minus - S_star + 1e-9) + (1 - v) * (R - R_star) / (R_minus - R_star + 1e-9)

    # Step 5: Rank Alternatives
    result_df = pd.DataFrame({
        'Alternative': alternatives,
        'S': S,
        'R': R,
        'Q': Q
    }).sort_values(by='Q').reset_index(drop=True)

    st.subheader("🏁 Final VIKOR Ranking")
    st.dataframe(result_df)

    st.success(f"🎯 Best Alternative: {result_df.iloc[0]['Alternative']}")

else:
    st.info("Please upload a properly formatted CSV file to begin.")
