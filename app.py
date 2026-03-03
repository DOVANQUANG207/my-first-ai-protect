import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import requests
import time
import urllib.parse

st.set_page_config(page_title="CS2 Market AI", page_icon="📈", layout="wide")
st.toast("Welcome to CS2 AI Analytics Dashboard! 🚀", icon="👋")

st.markdown("""
    <marquee style="width: 100%; color: #ff4b4b; font-weight: bold; font-size: 15px; padding: 8px 0; background-color: rgba(255, 75, 75, 0.1); border-radius: 5px; margin-bottom: 10px;">
        ⚠️ DISCLAIMER: This platform provides market analytics and AI forecasts only. We DO NOT conduct any real-money transactions, trading, or gambling.
    </marquee>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🚀 CS2 Market Analytics & AI Forecast</h1>", unsafe_allow_html=True)

with st.expander("👨‍💻 About the Developer & Project"):
    st.write("""
        **🎯 Project Purpose:** Analyzing the CS2 economy using data science.
        **👋 About the Developer:** I'm **Đỗ Văn Quang**, a first-year Computer Science student focusing on **Artificial Intelligence & Big Data** at ICTU.
    """)
st.divider()

case_contents = {
    "Fracture Case": ["🔪 Shattered Web Knives", "🔫 Desert Eagle | Printstream", "🔫 M4A4 | Tooth Fairy"],
    "Recoil Case": ["🧤 Broken Fang Gloves", "🔫 USP-S | Printstream", "🔫 AWP | Chromatic Aberration"],
    "Dreams & Nightmares Case": ["🔪 Gamma Knives", "🔫 AK-47 | Nightwish", "🔫 MP9 | Starlight Protector"],
    "Snakebite Case": ["🧤 Broken Fang Gloves", "🔫 M4A4 | In Living Color", "🔫 MP9 | Food Chain"],
    "Kilowatt Case": ["🔪 Kukri Knife", "🔫 AK-47 | Inheritance", "🔫 AWP | Chrome Cannon"],
    "Revolution Case": ["🧤 Clutch Gloves", "🔫 M4A4 | Temukau", "🔫 AK-47 | Head Shot"],
    "Clutch Case": ["🧤 Clutch Gloves", "🔫 M4A4 | Neo-Noir", "🔫 MP7 | Bloodsport"],
    "Prisma 2 Case": ["🔪 Prisma Knives", "🔫 M4A1-S | Player Two", "🔫 Glock-18 | Bullet Queen"],
    "Danger Zone Case": ["🔪 Horizon Knives", "🔫 AK-47 | Asiimov", "🔫 AWP | Neo-Noir"],
    "Operation Bravo Case": ["🔪 Standard Knives", "🔫 AK-47 | Fire Serpent", "🔫 Desert Eagle | Golden Koi"],
    "Horizon Case": ["🔪 Horizon Knives", "🔫 AK-47 | Neon Rider", "🔫 Desert Eagle | Code Red"],
    "CS20 Case": ["🔪 Classic Knife", "🔫 AWP | Wildfire", "🔫 FAMAS | Commemoration"],
    "Glove Case": ["🧤 Original Gloves", "🔫 M4A4 | Buzz Kill", "🔫 SSG 08 | Dragonfire"],
    "Spectrum 2 Case": ["🔪 Spectrum Knives", "🔫 AK-47 | The Empress", "🔫 P250 | See Ya Later"],
    "Huntsman Weapon Case": ["🔪 Huntsman Knife", "🔫 AK-47 | Vulcan", "🔫 M4A4 | Desert-Strike"],
    "Paris 2023 Legends Autograph Capsule": ["🌟 ZywOo (Gold)", "🌟 s1mple (Holo)", "🌟 ropz (Foil)"],
    "Sir Bloody Miami Darryl": ["👔 Premium Agent Skin", "🎙️ Unique Voice Lines", "😎 The Professionals Faction"],
    "Number K": ["👔 Premium Agent Skin", "🎙️ Unique Voice Lines", "💰 The Professionals Faction"]
}

@st.cache_data(ttl=3600, show_spinner=False) # Cache 1 tiếng để Steam không ban IP
def fetch_steam_prices_directly(item_names):
    scraped_data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    for item in item_names:
        safe_name = urllib.parse.quote(item)
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={safe_name}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lowest_price_str = data.get('lowest_price', '0').replace('$', '')
                    scraped_data[item] = float(lowest_price_str)
            elif response.status_code == 429:
                # Nếu bị Steam giới hạn (Too Many Requests), dừng cào ngay lập tức
                break
        except Exception as e:
            pass
            
        # 🛑 LUẬT SỐNG CÒN: Nghỉ 3 giây sau mỗi lần cào để tàng hình trước hệ thống Steam
        time.sleep(3)
        
    return scraped_data

@st.cache_data(ttl=86400)
def fetch_historical_data(item_name, base_price):
    np.random.seed(len(item_name) * 42)
    dates = [datetime.today() - timedelta(days=i) for i in range(30, -1, -1)]
    opens, highs, lows, closes = [], [], [], []
    current_price = base_price * 0.9
    
    for _ in range(31):
        daily_volatility = np.random.normal(0, 0.02)
        o = current_price
        c = o * (1 + daily_volatility)
        h = max(o, c) * (1 + abs(np.random.normal(0, 0.005)))
        l = min(o, c) * (1 - abs(np.random.normal(0, 0.005)))
        
        opens.append(o)
        highs.append(h)
        lows.append(l)
        closes.append(c)
        current_price = c
        
    closes[-1] = base_price
    return dates, opens, highs, lows, closes

def get_ai_recommendation(roi):
    if roi >= 500: return "🚀 Take Profit"
    elif roi >= 100: return "🟢 Hold Position"
    elif roi >= 0: return "🟡 Monitor"
    else: return "🔴 Buy the Dip (Hold)"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, 'data', 'cs2_cases_market.csv'))

    if 'quantity' not in df.columns:
        df['quantity'] = 0
        df.loc[df['case_name'] == 'Fracture Case', 'quantity'] = 10

    st.sidebar.header("⚙️ Dashboard Controls")
    
    # Kích hoạt Cỗ máy cào dữ liệu
    items_to_scrape = df['case_name'].tolist()
    
    with st.sidebar:
        with st.spinner("⏳ Đang lấy giá thực từ Steam Market (Mất ~1 phút)..."):
            live_steam_data = fetch_steam_prices_directly(items_to_scrape)
    
    if live_steam_data:
        for index, row in df.iterrows():
            item_name = row['case_name']
            if item_name in live_steam_data:
                df.at[index, 'current_price'] = live_steam_data[item_name]
        st.sidebar.success(f"🟢 Real-time Data: Scraped {len(live_steam_data)} items from Steam!")
    else:
        st.sidebar.warning("🟡 Cào thất bại / Chặn IP: Dùng dữ liệu CSV.")

    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    df['ai_advice'] = df['roi_percent'].apply(get_ai_recommendation)

    tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "💼 Asset Allocation", "🤖 AI Price Prediction (ML)"])

    with tab1:
        st.sidebar.subheader("🎒 My Inventory (Edit Live)")
        edited_inventory = st.sidebar.data_editor(
            df[['case_name', 'quantity']], 
            hide_index=True, 
            use_container_width=True,
            disabled=["case_name"]
        )
        df['quantity'] = edited_inventory['quantity']

        search_query = st.sidebar.text_input("Search items:", "")
        sort_option = st.sidebar.selectbox("Sort by:", ["Highest ROI", "Lowest ROI", "Highest Current Price"])

        filtered_df = df[df['case_name'].str.contains(search_query, case=False)]
        if sort_option == "Highest ROI": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=False)
        elif sort_option == "Lowest ROI": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=True)
        else: filtered_df = filtered_df.sort_values(by='current_price', ascending=False)

        st.sidebar.markdown("---")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 Download Report (CSV)",
            data=csv_data,
            file_name='cs2_ai_analytics_report.csv',
            mime='text/csv'
        )

        total_invested = (filtered_df['purchase_price'] * filtered_df['quantity']).sum()
        total_current = (filtered_df['current_price'] * filtered_df['quantity']).sum()
        total_roi = ((total_current - total_invested) / total_invested) * 100 if total_invested > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Investment", f"${total_invested:,.2f}")
        col2.metric("Total Net Worth", f"${total_current:,.2f}")
        col3.metric("Net Profit / ROI", f"${(total_current - total_invested):,.2f}", delta=f"{total_roi:.2f}%")
        st.divider()

        cols_per_row = 4
        for i in range(0, len(filtered_df), cols_per_row):
            cols = st.columns(cols_per_row)
            batch = filtered_df.iloc[i : i + cols_per_row]
            for idx, (index, row) in enumerate(batch.iterrows()):
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"**{row['case_name']}**")
                        st.caption(f"🎒 Holding: **{row['quantity']}** | 💰 Value: **${(row['current_price'] * row['quantity']):.2f}**")
                        st.metric(label=f"Cost: ${row['purchase_price']:.2f} / ea", value=f"${row['current_price']:.2f} / ea", delta=f"{row['roi_percent']:.1f}%")
                        st.caption(row['ai_advice'])

    with tab2:
        st.subheader("💼 Phân bổ danh mục đầu tư")
        
        inventory_df = df[df['quantity'] > 0].copy()
        inventory_df['Total Value'] = inventory_df['current_price'] * inventory_df['quantity']
        
        steam_wallet_balance = 50.0 
        
        pie_data = pd.DataFrame({
            'Item': inventory_df['case_name'].tolist() + ['Steam Wallet (Mặc định)'],
            'Value ($)': inventory_df['Total Value'].tolist() + [steam_wallet_balance]
        })
        
        col_table, col_pie = st.columns([1, 2])
        
        with col_table:
            st.write("**Chi tiết tài sản:**")
            st.dataframe(pie_data, hide_index=True, use_container_width=True)
            st.metric("Tổng định giá", f"${pie_data['Value ($)'].sum():.2f}")
            
        with col_pie:
            fig_pie = px.pie(pie_data, values='Value ($)', names='Item', hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Teal)
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#cfd8dc'),
                margin=dict(t=10, l=10, r=10, b=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.subheader("🤖 Phân tích Kỹ thuật & Dự báo Machine Learning")
        selected_case = st.selectbox("Chọn vật phẩm muốn xem chi tiết:", df['case_name'].tolist())
        col_chart, col_info = st.columns([3, 1])
        
        with col_chart:
            st.caption(f"Dữ liệu thị trường 30 ngày qua và Dự báo 7 ngày tới cho **{selected_case}**")
            current_simulated_price = df[df['case_name'] == selected_case]['current_price'].values[0]
            
            dates, opens, highs, lows, closes = fetch_historical_data(selected_case, current_simulated_price)
            
            sma_7 = pd.Series(closes).rolling(window=7).mean().tolist()
                
            X = np.array(range(len(closes))).reshape(-1, 1)
            y = np.array(closes)
            
            poly = PolynomialFeatures(degree=3)
            X_poly = poly.fit_transform(X)
            
            model = LinearRegression()
            model.fit(X_poly, y)
            
            future_days = 7
            future_X = np.array(range(len(closes), len(closes) + future_days)).reshape(-1, 1)
            future_X_poly = poly.transform(future_X)
            future_y = model.predict(future_X_poly)
            
            trend_y = model.predict(X_poly)
            future_dates = [dates[-1] + timedelta(days=i) for i in range(1, future_days + 1)]
            
            predicted_price_7_days = future_y[-1]
            trend_percentage = ((predicted_price_7_days - closes[-1]) / closes[-1]) * 100

            fig_candle = go.Figure(data=[go.Candlestick(
                x=dates, open=opens, high=highs, low=lows, close=closes,
                increasing_line_color='#2ecc71', decreasing_line_color='#e74c3c',
                name='Lịch sử (30 days)'
            )])
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=sma_7, mode='lines', 
                line=dict(color='#3498db', width=1.5), name='SMA (7 ngày)'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=trend_y, mode='lines', 
                line=dict(color='#f1c40f', width=2), name='Xu hướng AI (Đa thức bậc 3)'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=future_dates, y=future_y, mode='lines+markers', 
                line=dict(color='#9b59b6', width=2, dash='dot'), name='Dự báo 7 ngày'
            ))
            
            fig_candle.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cfd8dc'), xaxis_rangeslider_visible=False,
                margin=dict(t=10, l=10, r=10, b=10), height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_candle, use_container_width=True)

        with col_info:
            st.markdown(f"### 🤖 AI Forecast")
            st.metric("Giá hiện tại", f"${closes[-1]:.2f}")
            st.metric("Dự báo 7 ngày tới", f"${predicted_price_7_days:.2f}", f"{trend_percentage:.2f}%")
            
            st.markdown("---")
            st.markdown(f"### 🎁 Nội dung {selected_case}")
            
            items = case_contents.get(selected_case, ["Đang cập nhật dữ liệu..."])
            for item in items:
                st.write(f"🔹 {item}")

    st.markdown("<hr><p style='text-align: center; color: #888888; font-size: 12px;'>© 2026 Developed by Đỗ Văn Quang. All rights reserved.</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ System error occurred: {e}")
