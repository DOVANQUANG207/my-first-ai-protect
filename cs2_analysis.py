import pandas as pd
data = {
    'Case_Name': ['Fracture Case', 'Recoil Case', 'Dreams & Nightmares', 'Snakebite Case'],
    'Current_Price_USD': [0.85, 0.45, 1.20, 0.25],
    'Weekly_Trend': ['Stable', 'Increasing', 'Decreasing', 'Stable']
}
df = pd.DataFrame(data)

print("--- CS2 Case Investment Analysis ---")
print(df)

avg_price = df['Current_Price_USD'].mean()
print(f"\nAverage Case Price: ${avg_price:.2f}")
