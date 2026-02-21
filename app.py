import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

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

# --- TỪ ĐIỂN DỮ LIỆU CHỨA NỘI DUNG HÒM ---
case_contents = {
    "Fracture Case": ["🔪 Shattered Web Knives (Paracord, Survival, Nomad, Skeleton)", "🔫 Desert Eagle | Printstream", "🔫 M4A4 | Tooth Fairy"],
    "Recoil Case": ["🧤 Broken Fang Gloves", "🔫 USP-S | Printstream", "🔫 AWP | Chromatic Aberration"],
    "Dreams & Nightmares Case": ["🔪 Gamma Knives (Butterfly, Huntsman, etc.)", "🔫 AK-47 | Nightwish", "🔫 MP9 | Starlight Protector"],
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
    "Huntsman Weapon Case": ["🔪 Huntsman Knife", "🔫 AK-47 | Vulcan", "🔫 M4A4 | Desert-Strike"]
}

def get_ai_recommendation(roi):
    if roi >= 500: return "🚀 Take Profit"
    elif roi >= 100: return "🟢 Hold Position"
    elif roi >= 0: return "🟡 Monitor"
    else: return "🔴 Buy the Dip (Hold)"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, 'data', 'cs2_cases_market.csv'))

    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    df['ai_advice'] = df['roi_percent'].apply(get_ai_recommendation)

    tab1, tab2 = st.tabs(["📊 Portfolio Overview", "🕯️ Technical Analysis (Deep Dive)"])

    with tab1:
        st.sidebar.header("⚙️ Dashboard Controls")
        search_query = st.sidebar.text_input("Search items:", "")
        sort_option = st.sidebar.selectbox("Sort by:", ["Highest ROI", "Lowest ROI", "Highest Current Price"])

        filtered_df = df[df['case_name'].str.contains(search_query, case=False)]
        if sort_option == "Highest ROI": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=False)
        elif sort_option == "Lowest ROI": filtered_df = filtered_df.sort_values(by='roi_percent', ascending=True)
        else: filtered_df = filtered_df.sort_values(by='current_price', ascending=False)

        col1, col2, col3 = st.columns(3)
        total_invested = filtered_df['purchase_price'].sum()
        total_current = filtered_df['current_price'].sum()
        total_roi = ((total_current - total_invested) / total_invested) * 100 if total_invested > 0 else 0
        
        col1.metric("Total Investment", f"${total_invested:,.2f}")
        col2.metric("Current Value", f"${total_current:,.2f}")
        col3.metric("Total Portfolio ROI", f"{total_roi:.2f}%", delta=f"{total_roi:.2f}%")
        st.divider()

        cols_per_row = 4
        for i in range(0, len(filtered_df), cols_per_row):
            cols = st.columns(cols_per_row)
            batch = filtered_df.iloc[i : i + cols_per_row]
            for idx, (index, row) in enumerate(batch.iterrows()):
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"**{row['case_name']}**")
                        st.metric(label=f"Cost: ${row['purchase_price']:.2f}", value=f"${row['current_price']:.2f}", delta=f"{row['roi_percent']:.1f}%")
                        st.caption(row['ai_advice'])

    with tab2:
        st.subheader("🔍 Khám phá Chi tiết & Phân tích Kỹ thuật")
        selected_case = st.selectbox("Chọn vật phẩm muốn xem chi tiết:", df['case_name'].tolist())
        col_chart, col_info = st.columns([3, 1])
        
        with col_chart:
            st.caption(f"Dữ liệu thị trường 30 ngày qua cho **{selected_case}** (Dữ liệu mô phỏng AI)")
            base_price = df[df['case_name'] == selected_case]['current_price'].values[0]
            dates = [datetime.today() - timedelta(days=i) for i in range(30, 0, -1)]
            
            opens, highs, lows, closes, volumes = [], [], [], [], []
            current_sim_price = base_price
            
            np.random.seed(len(selected_case)) 
            for _ in range(30):
                o = current_sim_price * (1 + np.random.uniform(-0.02, 0.02))
                c = o * (1 + np.random.normal(0, 0.03))
                h = max(o, c) * (1 + abs(np.random.normal(0, 0.01)))
                l = min(o, c) * (1 - abs(np.random.normal(0, 0.01)))
                v = int(np.random.uniform(5000, 50000))
                
                opens.append(o)
                highs.append(h), lows.append(l), closes.append(c), volumes.append(v)
                current_sim_price = c 
                
            fig_candle = go.Figure(data=[go.Candlestick(
                x=dates, open=opens, high=highs, low=lows, close=closes,
                increasing_line_color='#2ecc71', decreasing_line_color='#e74c3c'
            )])
            
            fig_candle.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cfd8dc'), xaxis_rangeslider_visible=False,
                margin=dict(t=10, l=10, r=10, b=10), height=400
            )
            st.plotly_chart(fig_candle, use_container_width=True)

        with col_info:
            st.markdown(f"### 🎁 Nội dung {selected_case}")
            
            # TỰ ĐỘNG HIỂN THỊ NỘI DUNG HÒM TỪ TỪ ĐIỂN
            items = case_contents.get(selected_case, ["Đang cập nhật dữ liệu..."])
            for item in items:
                st.write(f"🔹 {item}")
            
            st.markdown("---")
            st.metric("Khối lượng giao dịch (24h)", f"{volumes[-1]:,} items")
            st.metric("Biến động tuần (7d)", f"{((closes[-1] - closes[-7]) / closes[-7] * 100):.1f}%")

    st.markdown("<hr><p style='text-align: center; color: #888888; font-size: 12px;'>© 2026 Developed by Đỗ Văn Quang. All rights reserved.</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ System error occurred: {e}")
