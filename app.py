import matplotlib.pyplot as plt
import pandas as pd

# Sample VIKOR results
result_df = pd.DataFrame({
    "Alternative": ["YPSAH", "FPI", "HEIM", "KLK", "UTDPLT"],
    "Q": [0.000, 0.180, 0.499, 0.803, 1.000]
})

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(result_df["Alternative"], result_df["Q"], color='skyblue')
plt.title("VIKOR Q Values for Stock Alternatives")
plt.xlabel("Alternative")
plt.ylabel("Q Value (Lower is Better)")
plt.ylim(0, 1.1)

# Add values on bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.3f}", ha='center')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
