import matplotlib.pyplot as plt

# Create the bar chart for Q values
st.markdown("### 📊 VIKOR Q Value Bar Chart")

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(result_df["Alternative"], result_df["Q"], color='royalblue')
ax.set_xlabel("Alternatives")
ax.set_ylabel("Q Value (Lower is Better)")
ax.set_title("VIKOR Q Values for Stock Alternatives")
ax.set_ylim(0, 1.1)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.02, f"{height:.3f}", ha='center', fontsize=9)

st.pyplot(fig)
