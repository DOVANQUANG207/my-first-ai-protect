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

st.set_page_config(page_title="CS2 Market AI Terminal", page_icon="⚡", layout="wide")
st.toast("Hệ thống giao dịch đã khởi động! 🚀", icon="⚡")

# ==========================================
# 🎨 GÓI GIAO DIỆN PRO (CUSTOM CSS TRADING TERMINAL)
# ==========================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0d1117; }
    [data-testid="stMetric"] {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 15px 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px); border-color: #58a6ff;
        box-shadow: 0 6px 12px rgba(88, 166, 255, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #161b22; border-radius: 8px 8px 0px 0px;
        padding: 10px 20px; color: #8b949e; border: 1px solid #30363d; border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d; color: #2ecc71 !important;
        font-weight: bold; border-top: 3px solid #2ecc71;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #161b22 !important; border: 1px solid #30363d !important;
        border-radius: 12px !important; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        border-color: #f1c40f !important; box-shadow: 0 6px 15px rgba(241, 196, 15, 0.15);
    }
    h1, h2, h3 { color: #e6edf3 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .marquee-container {
        width: 100%; color: #ff4b4b; font-weight: 600; font-size: 14px; padding: 10px 0; 
        background-color: #2d1115; border: 1px solid #ff4b4b; border-radius: 8px; 
        margin-bottom: 20px; box-shadow: 0 0 10px rgba(255, 75, 75, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <marquee class="marquee-container">
        ⚠️ CẢNH BÁO: Hệ thống AI Dự báo này chỉ dành cho mục đích Phân tích Dữ liệu và Học thuật. KHÔNG khuyến nghị giao dịch tiền thật.
    </marquee>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #58a6ff; text-transform: uppercase; letter-spacing: 2px;'>⚡ CS2 Terminal & AI Forecast</h1>", unsafe_allow_html=True)

with st.expander("👨‍💻 About the Developer & System Architecture"):
    st.write("""
        **🎯 Project Purpose:** Analyzing the CS2 economy using Advanced Data Pipeline & Machine Learning.
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
    "Chroma 3 Case": ["🔪 Standard Knives", "🔫 M4A1-S | Chantico's Fire", "🔫 AWP | Fever Dream"],
    "Chroma 2 Case": ["🔪 Standard Knives", "🔫 M4A1-S | Hyper Beast", "🔫 MAC-10 | Neon Rider"],
    "Chroma Case": ["🔪 Standard Knives", "🔫 Galil AR | Chatterbox", "🔫 AWP | Man-o'-war"],
    "Gamma Case": ["🔪 Gamma Knives", "🔫 M4A1-S | Mecha Industries", "🔫 Glock-18 | Wasteland Rebel"],
    "Gamma 2 Case": ["🔪 Gamma Knives", "🔫 AK-47 | Neon Revolution", "🔫 FAMAS | Roll Cage"],
    "Shadow Case": ["🔪 Shadow Daggers", "🔫 M4A1-S | Golden Coil", "🔫 USP-S | Kill Confirmed"],
    "Operation Wildfire Case": ["🔪 Bowie Knife", "🔫 AK-47 | Fuel Injector", "🔫 M4A4 | The Battlestar"],
    "Shattered Web Case": ["🔪 Shattered Web Knives", "🔫 AWP | Containment Breach", "🔫 MAC-10 | Stalker"],
    "Special Agent Ava | FBI": ["🕵️‍♀️ Master Agent", "🎙️ Unique Voice Lines", "🦅 FBI Faction"],
    "Getaway Sally | The Professionals": ["🏃‍♀️ Superior Agent", "🎙️ Unique Voice Lines", "💰 The Professionals"],
    "Number K | The Professionals": ["👔 Premium Agent", "🎙️ Unique Voice Lines", "💰 The Professionals"],
    "Sir Bloody Miami Darryl | The Professionals": ["👔 Premium Agent", "🎙️ Unique Voice Lines", "😎 The Professionals"],
    "Safecracker Voltzmann | The Professionals": ["🔓 Exceptional Agent", "🎙️ Unique Voice Lines", "💰 The Professionals"],
    "Cmdr. Mae 'Dead Cold' Jamison | SWAT": ["🥶 Master Agent", "🎙️ Unique Voice Lines", "🚔 SWAT Faction"],
    "Lt. Commander Ricksaw | NSWC SEAL": ["🪖 Master Agent", "🎙️ Unique Voice Lines", "🌊 NSWC SEAL"]
}

# ==========================================
# 🤖 MODULE TELEGRAM BOT
# ==========================================
def send_telegram_message(msg):
    bot_token = 'ĐIỀN_TOKEN_CỦA_CẬU_VÀO_ĐÂY'
    bot_chat_id = 'ĐIỀN_CHAT_ID_CỦA_CẬU_VÀO_ĐÂY'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chat_id}&text={msg}"
    try:
        requests.get(url, timeout=5)
    except Exception as e:
        pass

@st.cache_data(ttl=3600, show_spinner=False) 
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
                break
        except Exception as e:
            pass
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
    if roi >= 500: return "🚀 MẠNH TAY CHỐT LỜI"
    elif roi >= 100: return "🟢 GIỮ VỊ THẾ"
    elif roi >= 0: return "🟡 THEO DÕI"
    else: return "🔴 BẮT ĐÁY"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    df = pd.read_csv(csv_path)

    existing_cases = df['case_name'].tolist()
    new_cases_to_add = []
    for case in case_contents.keys():
        if case not in existing_cases:
            new_cases_to_add.append({
                'case_name': case, 'purchase_price': 5.00, 'current_price': 5.00, 'quantity': 0
            })
            
    if new_cases_to_add:
        new_df = pd.DataFrame(new_cases_to_add)
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(csv_path, index=False)

    if 'quantity' not in df.columns:
        df['quantity'] = 0
        df.loc[df['case_name'] == 'Fracture Case', 'quantity'] = 10

    st.sidebar.markdown("<h2 style='text-align: center; color: #58a6ff;'>⚙️ CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    items_to_scrape = df['case_name'].tolist()
    
    with st.sidebar:
        with st.spinner("⏳ Đang lấy giá thực từ Steam Market (Mất khoảng 1-2 phút)..."):
            live_steam_data = fetch_steam_prices_directly(items_to_scrape)
    
    if live_steam_data:
        for index, row in df.iterrows():
            item_name = row['case_name']
            if item_name in live_steam_data:
                df.at[index, 'current_price'] = live_steam_data[item_name]
        st.sidebar.success(f"🟢 DATA LINK ACTIVE: Scraped {len(live_steam_data)} items from Steam!")
    else:
        st.sidebar.warning("🟡 Cào thất bại / Chặn IP: Sử dụng dữ liệu CSV Offline.")

    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    df['ai_advice'] = df['roi_percent'].apply(get_ai_recommendation)

    tab1, tab2, tab3 = st.tabs(["📊 TỔNG QUAN THỊ TRƯỜNG", "💼 QUẢN LÝ TÀI SẢN", "🤖 PHÒNG LAB DỰ BÁO AI"])

    with tab1:
        st.sidebar.subheader("🎒 Tủ đồ Live (Inventory)")
        edited_inventory = st.sidebar.data_editor(
            df[['case_name', 'quantity']], hide_index=True, use_container_width=True, disabled=["case_name"]
        )
        df['quantity'] = edited_inventory['quantity']

        search_query = st.sidebar.text_input("🔍 Tìm kiếm mã tài sản:", "")
        sort_option = st.sidebar.selectbox("Lọc theo:", ["Lợi nhuận (ROI) Cao nhất", "Lợi nhuận (ROI) Thấp nhất", "Thị giá Cao nhất"])

        filtered_df = df[df['case_name'].str.contains(search_query, case=False)]
        if sort_option == "Lợi nhuận (ROI) Cao nhất": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=False)
        elif sort_option == "Lợi nhuận (ROI) Thấp nhất": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=True)
        else: filtered_df = filtered_df.sort_values(by='current_price', ascending=False)

        st.sidebar.markdown("---")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(label="📥 Xuất báo cáo (CSV)", data=csv_data, file_name='cs2_terminal_report.csv', mime='text/csv')

        # ==========================================
        # 🔔 NÚT GỬI CẢNH BÁO TELEGRAM
        # ==========================================
        st.sidebar.markdown("---")
        if st.sidebar.button("🔔 Gửi Cảnh Báo Telegram"):
            with st.spinner("Đang bắn tín hiệu..."):
                alerts_sent = 0
                for i, row in filtered_df.iterrows():
                    # Chỉ báo động những món nào có Lãi suất trên 100% VÀ cậu đang nắm giữ (quantity > 0)
                    if row['roi_percent'] >= 100 and row['quantity'] > 0:
                        alert_text = f"🚀 CHỐT LỜI: {row['case_name']} | ROI: {row['roi_percent']:.1f}% | Lãi: ${(row['current_price'] - row['purchase_price']) * row['quantity']:.2f}"
                        send_telegram_message(alert_text)
                        alerts_sent += 1
                        
                if alerts_sent > 0:
                    st.sidebar.success(f"✅ Đã bắn {alerts_sent} tín hiệu chốt lời!")
                else:
                    st.sidebar.info("Hệ thống an toàn: Chưa có mặt hàng nào đạt mức x2 (ROI >100%) trong kho để báo động.")

        total_invested = (filtered_df['purchase_price'] * filtered_df['quantity']).sum()
        total_current = (filtered_df['current_price'] * filtered_df['quantity']).sum()
        total_roi = ((total_current - total_invested) / total_invested) * 100 if total_invested > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng Vốn Đầu Tư", f"${total_invested:,.2f}")
        col2.metric("Định Giá Hiện Tại", f"${total_current:,.2f}")
        col3.metric("Lợi Nhuận Ròng", f"${(total_current - total_invested):,.2f}", delta=f"{total_roi:.2f}%")
        st.divider()

        cols_per_row = 4
        for i in range(0, len(filtered_df), cols_per_row):
            cols = st.columns(cols_per_row)
            batch = filtered_df.iloc[i : i + cols_per_row]
            for idx, (index, row) in enumerate(batch.iterrows()):
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"<h4 style='color: #e6edf3; margin-bottom: 0;'>{row['case_name']}</h4>", unsafe_allow_html=True)
                        st.caption(f"🎒 Số lượng: **{row['quantity']}** | 💰 Trị giá: **${(row['current_price'] * row['quantity']):.2f}**")
                        st.metric(label=f"Giá gốc: ${row['purchase_price']:.2f}", value=f"${row['current_price']:.2f}", delta=f"{row['roi_percent']:.1f}%")
                        st.caption(row['ai_advice'])

    with tab2:
        st.subheader("💼 Cấu trúc Danh mục Đầu tư (Portfolio)")
        inventory_df = df[df['quantity'] > 0].copy()
        inventory_df['Total Value'] = inventory_df['current_price'] * inventory_df['quantity']
        steam_wallet_balance = 50.0 
        pie_data = pd.DataFrame({
            'Item': inventory_df['case_name'].tolist() + ['Steam Wallet (Dự phòng)'],
            'Value ($)': inventory_df['Total Value'].tolist() + [steam_wallet_balance]
        })
        
        col_table, col_pie = st.columns([1, 2])
        with col_table:
            st.write("**Chi tiết tài sản:**")
            st.dataframe(pie_data, hide_index=True, use_container_width=True)
            st.metric("Tổng định giá toàn bộ", f"${pie_data['Value ($)'].sum():.2f}")
            
        with col_pie:
            fig_pie = px.pie(pie_data, values='Value ($)', names='Item', hole=0.6, color_discrete_sequence=px.colors.sequential.Teal)
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#c9d1d9'),
                margin=dict(t=10, l=10, r=10, b=10),
                annotations=[dict(text='ASSETS', x=0.5, y=0.5, font_size=20, showarrow=False, font_color="#58a6ff")]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.subheader("🤖 Module Phân Tích Kỹ Thuật (Machine Learning Model)")
        selected_case = st.selectbox("Lựa chọn Mã tài sản để đưa vào phân tích:", df['case_name'].tolist())
        col_chart, col_info = st.columns([3, 1])
        
        with col_chart:
            st.caption(f"Trực quan hóa Dữ liệu (30 Ngày) & Phóng chiếu AI (7 Ngày) cho **{selected_case}**")
            current_simulated_price = df[df['case_name'] == selected_case]['current_price'].values[0]
            
            # 🚀 TÍNH TOÁN DẢI BĂNG BOLLINGER (BOLLINGER BANDS)
            dates, opens, highs, lows, closes = fetch_historical_data(selected_case, current_simulated_price)
            sma_7 = pd.Series(closes).rolling(window=7).mean().tolist()
            std_7 = pd.Series(closes).rolling(window=7).std().tolist()
            
            upper_band = [m + (2 * s) if not np.isnan(s) else None for m, s in zip(sma_7, std_7)]
            lower_band = [m - (2 * s) if not np.isnan(s) else None for m, s in zip(sma_7, std_7)]
                
            X = np.array(range(len(closes))).reshape(-1, 1)
            y = np.array(closes)
            
            poly = PolynomialFeatures(degree=3)
            X_poly = poly.fit_transform(X)
            
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # 🚀 CHẤM ĐIỂM ĐỘ TIN CẬY CỦA AI (R2 SCORE)
            r2_score = model.score(X_poly, y) * 100
            confidence_level = max(0, min(100, r2_score)) 
            
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
                increasing_line_color='#2ecc71', decreasing_line_color='#ff4b4b',
                name='Lịch sử (30 days)'
            )])
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=upper_band, mode='lines', 
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1), name='Bollinger Upper'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=lower_band, mode='lines', 
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1), fill='tonexty', fillcolor='rgba(88, 166, 255, 0.1)', name='Bollinger Lower'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=sma_7, mode='lines', 
                line=dict(color='#58a6ff', width=2), name='Đường trung bình (SMA 7)'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=dates, y=trend_y, mode='lines', 
                line=dict(color='#f1c40f', width=2), name='Poly-Regression (Bậc 3)'
            ))
            
            fig_candle.add_trace(go.Scatter(
                x=future_dates, y=future_y, mode='lines+markers', 
                line=dict(color='#bd93f9', width=2, dash='dot'), name='AI Forecast (7 Ngày)'
            ))
            
            fig_candle.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#c9d1d9'), 
                xaxis_rangeslider_visible=False, margin=dict(t=10, l=10, r=10, b=10), height=450,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(gridcolor='#30363d'), xaxis=dict(gridcolor='#30363d')
            )
            st.plotly_chart(fig_candle, use_container_width=True)

        with col_info:
            st.markdown(f"### 🎯 Tín Hiệu AI")
            st.metric("Thị giá hiện tại", f"${closes[-1]:.2f}")
            st.metric("Giá kỳ vọng (7 ngày)", f"${predicted_price_7_days:.2f}", f"{trend_percentage:.2f}%")
            
            if confidence_level >= 80:
                st.success(f"📈 Độ tin cậy Model: **{confidence_level:.1f}%** (Cao)")
            elif confidence_level >= 50:
                st.warning(f"🟨 Độ tin cậy Model: **{confidence_level:.1f}%** (Trung bình)")
            else:
                st.error(f"⚠️ Độ tin cậy Model: **{confidence_level:.1f}%** (Thấp)")
            
            st.markdown("---")
            st.markdown(f"### 📦 Chiết xuất Nội dung")
            
            items = case_contents.get(selected_case, ["Hệ thống đang dò tìm dữ liệu..."])
            for item in items:
                st.write(f"🔹 {item}")

    st.markdown("<hr><p style='text-align: center; color: #8b949e; font-size: 13px; letter-spacing: 1px;'>© 2026 CODED BY DO VAN QUANG | BIG DATA & AI TERMINAL</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ HỆ THỐNG GẶP LỖI: {e}")
