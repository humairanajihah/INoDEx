import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="VIKOR-Stocks", layout="wide")

st.title("📊 VIKOR-Stocks: Intelligent Stock Ranking System")
st.markdown("Rank stock alternatives based on multiple criteria using the VIKOR MCDM method.")

# Upload CSV file
uploaded_file = st.file_uploader("📂 Upload CSV file (First column = Alternatives, rest = Criteria)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📁 Raw Data")
    st.dataframe(df)

    # Extract alternatives and criteria
    alternatives = df.iloc[:, 0].values
    criteria = df.iloc[:, 1:]
    criteria_names = criteria.columns.tolist()

    # Define benefit and cost criteria
    benefit_criteria = ['EPS', 'DPS', 'NTA', 'DY', 'ROE']
    cost_criteria = ['PE', 'PTBV']

    # Equal weights
    weights = np.ones(len(criteria.columns)) / len(criteria.columns)

    # Step 1: Normalize Decision Matrix
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
    weights_series = pd.Series(weights, index=norm.columns)
    S = ((weights_series * (f_star - norm) / (f_star - f_minus + 1e-9)).sum(axis=1))
    R = ((weights_series * (f_star - norm) / (f_star - f_minus + 1e-9)).max(axis=1))

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

    # Step 6: Ranked Q Bar Chart (Lower Q is Better)
    st.markdown("### 📊 Ranked Bar Chart by Q Value (Best to Worst)")

    fig, ax = plt.subplots(figsize=(10, 5))
    sorted_df = result_df.sort_values(by='Q', ascending=True)
    bars = ax.bar(sorted_df['Alternative'], sorted_df['Q'], color='teal')

    ax.set_ylabel("Q Value (Lower is Better)")
    ax.set_xlabel("Stock Alternatives")
    ax.set_title("VIKOR Ranked Alternatives")
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.3f}", ha='center', fontsize=9)

    st.pyplot(fig)

else:
    st.info("Please upload a properly formatted CSV file to begin.")
