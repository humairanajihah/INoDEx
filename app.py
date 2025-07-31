import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sample stock data
data = {
    "Stock": ["BSLCORP", "FPGROUP", "GTRONIC", "JHM", "KESM", "MPI", "SJC", "TONGHER", "UWC", "YBS", "YTL", "YPSAH"],
    "Q": [0.35, 0.27, 0.43, 0.39, 0.55, 0.60, 0.33, 0.29, 0.25, 0.48, 0.52, 0.31]  # Replace with your actual Q values
}

df = pd.DataFrame(data)
df = df.sort_values("Q")  # Lower Q is better

# Plotting
plt.figure(figsize=(10, 6))
plt.barh(df["Stock"], df["Q"], color="skyblue")
plt.xlabel("Q Value (Lower is Better)")
plt.title("VIKOR Ranking of Stocks")
plt.gca().invert_yaxis()  # Best stock on top
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
