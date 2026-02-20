import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import requests
import time
from sklearn.linear_model import LinearRegression

def get_live_price(item_name):
    # Chuyển đổi tên hòm sang định dạng URL (ví dụ: Fracture Case -> Fracture%20Case)
    safe_name = item_name.replace(" ", "%20")
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={safe_name}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("success") and "lowest_price" in data:
            price_str = data.get("lowest_price")
            # Xử lý chuỗi giá từ Steam (ví dụ "$0.85" thành 0.85)
            return float(price_str.replace('$', '').replace(',', ''))
    except Exception as e:
        print(f"  [!] Lỗi lấy giá Live cho {item_name}: {e}")
    return None

def analyze_and_predict():
    print("--- STARTING LIVE AI DATA PIPELINE ---")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    
    try:
        df = pd.read_csv(file_path)
        
        # --- BƯỚC MỚI: CẬP NHẬT GIÁ LIVE ---
        print("\n[Step 1]: Fetching real-time prices from Steam Market...")
        live_prices = []
        for name in df['case_name']:
            print(f" -> Fetching: {name}...")
            price = get_live_price(name)
            if price:
                live_prices.append(price)
            else:
                print(f"    (Dùng giá cũ từ CSV cho {name})")
                live_prices.append(df.loc[df['case_name'] == name, 'current_price'].values[0])
            time.sleep(3) # Nghỉ 3 giây để không bị Steam ban IP
        
        df['current_price'] = live_prices
        
        # --- CÁC BƯỚC PHÂN TÍCH VÀ AI ---
        df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
        df_sorted = df.sort_values(by='roi_percent', ascending=False)
        
        print("\n[Step 2]: AI Price Prediction (6-Month Forecast)...")
        X_train = np.array([[0], [30]]) 
        future_time = np.array([[180]]) 
        
        predictions = []
        for index, row in df_sorted.iterrows():
            y_train = np.array([row['purchase_price'], row['current_price']])
            model = LinearRegression().fit(X_train, y_train)
            pred = model.predict(future_time)[0]
            predictions.append(max(0, pred))
        
        df_sorted['predicted_price_6m'] = predictions
        
        print("\n--- LIVE MARKET REPORT ---")
        print(df_sorted[['case_name', 'current_price', 'predicted_price_6m', 'roi_percent']])

        # Vẽ biểu đồ
        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted['case_name'], df_sorted['roi_percent'], color='lightgreen')
        plt.title('LIVE CS2 Investment ROI & AI Forecast')
        plt.ylabel('ROI (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(current_dir, 'cs2_live_report.png'))
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_and_predict()
