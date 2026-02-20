import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import requests
import time
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Hàm lấy giá trực tiếp từ Steam API
def get_live_price(item_name):
    safe_name = item_name.replace(" ", "%20")
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={safe_name}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("success") and "lowest_price" in data:
            price_str = data.get("lowest_price")
            return float(price_str.replace('$', '').replace(',', ''))
    except Exception as e:
        print(f"  [!] Connection Error for {item_name}: {e}")
    return None

# Hàm lưu lịch sử biến động giá vào file CSV
def save_to_history(case_name, price, data_dir):
    history_file = os.path.join(data_dir, 'price_history.csv')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = pd.DataFrame([[now, case_name, price]], columns=['timestamp', 'case_name', 'price'])
    
    if not os.path.isfile(history_file):
        new_entry.to_csv(history_file, index=False)
    else:
        new_entry.to_csv(history_file, mode='a', header=False, index=False)
    print(f"  [Log]: Data point saved for {case_name} at {now}")

def analyze_and_predict():
    print("--- STARTING ADVANCED AI DATA PIPELINE ---")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # Tạo thư mục data nếu chưa có
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    file_path = os.path.join(data_dir, 'cs2_cases_market.csv')
    
    try:
        df = pd.read_csv(file_path)
        
        # --- CẬP NHẬT GIÁ LIVE & LƯU LỊCH SỬ ---
        print("\n[Step 1]: Fetching live prices & Logging history...")
        live_prices = []
        for name in df['case_name']:
            print(f" -> Processing: {name}...")
            price = get_live_price(name)
            if price:
                live_prices.append(price)
                save_to_history(name, price, data_dir)
            else:
                print(f"    (Fallback: Using CSV price for {name})")
                live_prices.append(df.loc[df['case_name'] == name, 'current_price'].values[0])
            time.sleep(3) # Tránh bị Steam chặn IP
        
        df['current_price'] = live_prices
        
        # --- PHÂN TÍCH ROI & AI PREDICTION ---
        df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
        df_sorted = df.sort_values(by='roi_percent', ascending=False)
        
        print("\n[Step 2]: AI Forecasting (Linear Regression)...")
        X_train = np.array([[0], [30]]) # T0 (Purchase) -> T30 (Now)
        future_time = np.array([[180]]) # T180 (6 Months later)
        
        predictions = []
        for index, row in df_sorted.iterrows():
            y_train = np.array([row['purchase_price'], row['current_price']])
            model = LinearRegression().fit(X_train, y_train)
            pred = model.predict(future_time)[0]
            predictions.append(max(0, pred))
        
        df_sorted['predicted_price_6m'] = predictions
        
        # Xuất báo cáo ra Terminal
        print("\n" + "="*50)
        print("FINAL MARKET REPORT (LIVE + AI)")
        print("="*50)
        print(df_sorted[['case_name', 'current_price', 'predicted_price_6m', 'roi_percent']])

        # Vẽ và lưu biểu đồ
        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted['case_name'], df_sorted['roi_percent'], color='mediumseagreen')
        plt.title('CS2 Real-time ROI & AI Price Prediction')
        plt.ylabel('ROI (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(current_dir, 'cs2_live_report.png'))
        print(f"\n=> Report saved: cs2_live_report.png")
        plt.show()

    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    analyze_and_predict()
