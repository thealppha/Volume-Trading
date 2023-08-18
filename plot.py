import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("data/Analyze/Final_SOLUSDT_1m_2021-01-01_2023-08-01.csv")

# Extract year and month from the Date column
year_month_day = ["-".join(df["Date"].iloc[i].split(" ")[0].split("-")[:2]) for i in range(len(df))]
df["year_month_day"] = year_month_day

# Group by year_month_day and calculate monthly aggregated profits and ratios
monthly_profits = df.groupby("year_month_day").agg({
    'profits': lambda x: np.prod(x),
    'Close': 'last',
    'Open': 'first'
})

# Convert index to datetime for plotting
monthly_profits.index = pd.to_datetime(monthly_profits.index)

# Calculate the ratio of last_date_of_month_close_price to first_date_of_month_open_price
monthly_profits['default_profit'] = monthly_profits['Close'] / monthly_profits['Open']

# Bar plot
plt.figure(figsize=(12, 6))

# Calculate the offset for side-by-side bars
bar_width = 7
bar_offset = bar_width / 2

# Plot monthly profits
plt.bar(monthly_profits.index - pd.DateOffset(days=bar_offset), monthly_profits['profits'], color='green', label='Our Profits', width=bar_width)

# Plot price ratios next to profits
plt.bar(monthly_profits.index + pd.DateOffset(days=bar_offset), monthly_profits['default_profit'], color='red', label='Default Profits', width=bar_width)

# Add a reference line at y = 1.0
plt.axhline(y=1.0, color='black', linestyle='--', label='Reference')

plt.xlabel('Date')
plt.ylabel('Profits')
plt.title('Our Profits and Default Profits Comparison (Monthly)')

plt.xticks(monthly_profits.index, monthly_profits.index.strftime('%Y-%m'), rotation=45, ha='right')

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Profit Comparison.png")
