import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CS2 Market AI", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🚀 CS2 Market Analytics & AI Forecast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Hệ thống theo dõi danh mục đầu tư và phân tích xu hướng giá bằng thuật toán.</p>", unsafe_allow_html=True)
st.divider()

def get_ai_recommendation(roi):
    if roi >= 500:
        return "🚀 Khuyên dùng: Chốt lời"
    elif roi >= 100:
        return "🟢 Khuyên dùng: Giữ vị thế"
    elif roi >= 0:
        return "🟡 Khuyên dùng: Theo dõi thêm"
    else:
        return "🔴 Khuyên dùng: Bắt đáy (HODL)"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    df = pd.read_csv(data_path)

    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    df['ai_advice'] = df['roi_percent'].apply(get_ai_recommendation)

    st.sidebar.header("⚙️ Bảng Điều Khiển")
    search_query = st.sidebar.text_input("Tìm kiếm vật phẩm:", "")
    sort_option = st.sidebar.selectbox("Sắp xếp theo:", ["ROI Cao nhất", "ROI Thấp nhất", "Giá hiện tại Cao nhất"])

    filtered_df = df[df['case_name'].str.contains(search_query, case=False)]

    if sort_option == "ROI Cao nhất":
        filtered_df = filtered_df.sort_values(by='roi_percent', ascending=False)
    elif sort_option == "ROI Thấp nhất":
        filtered_df = filtered_df.sort_values(by='roi_percent', ascending=True)
    elif sort_option == "Giá hiện tại Cao nhất":
        filtered_df = filtered_df.sort_values(by='current_price', ascending=False)

    st.subheader("💼 Tổng Quan Danh Mục Đầu Tư")
    total_invested = filtered_df['purchase_price'].sum()
    total_current = filtered_df['current_price'].sum()
    
    if total_invested > 0:
        total_roi = ((total_current - total_invested) / total_invested) * 100
    else:
        total_roi = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng Vốn Chi Tiêu", f"${total_invested:,.2f}")
    col2.metric("Tổng Giá Trị Ước Tính", f"${total_current:,.2f}")
    col3.metric("Tăng Trưởng Toàn Danh Mục", f"{total_roi:.2f}%", delta=f"{total_roi:.2f}%")

    st.divider()

    st.subheader(f"📦 Chi Tiết Thị Trường ({len(filtered_df)} Vật phẩm)")
    
    cols_per_row = 4
    for i in range(0, len(filtered_df), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        
        for idx, (index, row) in enumerate(batch.iterrows()):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"**{row['case_name']}**")
                    st.metric(
                        label=f"Giá vốn: ${row['purchase_price']:.2f}",
                        value=f"${row['current_price']:.2f}",
                        delta=f"{row['roi_percent']:.1f}%"
                    )
                    st.caption(row['ai_advice'])

    st.divider()
    
    st.subheader("📊 Biểu đồ Phân bổ Lợi nhuận (ROI)")
    chart_data = filtered_df[['case_name', 'roi_percent']].set_index('case_name')
    st.bar_chart(chart_data, color="#2ecc71")

except FileNotFoundError:
    st.error("⚠️ Không tìm thấy cơ sở dữ liệu. Vui lòng kiểm tra lại file CSV.")
except Exception as e:
    st.error(f"⚠️ Đã xảy ra lỗi hệ thống: {e}")
