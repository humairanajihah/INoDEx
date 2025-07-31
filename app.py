import matplotlib.pyplot as plt

st.markdown("### 📈 VIKOR Q Value Chart")

# Plotting the Q values
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(result_df["Alternative"], result_df["Q"], color="skyblue")
ax.set_title("VIKOR Compromise Index (Q) by Alternative")
ax.set_ylabel("Q Value")
ax.set_xlabel("Alternative")
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Highlight best (min Q) in green
best_index = result_df["Q"].idxmin()
bars[best_index].set_color('green')

# Add text on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

st.pyplot(fig)
