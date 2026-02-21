import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="CS2 Market AI", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🚀 CS2 Market Analytics & AI Forecast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Portfolio tracking and algorithmic price trend analysis system.</p>", unsafe_allow_html=True)
st.divider()

def get_ai_recommendation(roi):
    if roi >= 500:
        return "🚀 Advice: Take Profit"
    elif roi >= 100:
        return "🟢 Advice: Hold Position"
    elif roi >= 0:
        return "🟡 Advice: Monitor"
    else:
        return "🔴 Advice: Buy the Dip"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    df = pd.read_csv(data_path)

    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    df['ai_advice'] = df['roi_percent'].apply(get_ai_recommendation)

    st.sidebar.header("⚙️ Dashboard Controls")
    search_query = st.sidebar.text_input("Search items:", "")
    sort_option = st.sidebar.selectbox("Sort by:", ["Highest ROI", "Lowest ROI", "Highest Current Price"])

    filtered_df = df[df['case_name'].str.contains(search_query, case=False)]

    if sort_option == "Highest ROI":
        filtered_df = filtered_df.sort_values(by='roi_percent', ascending=False)
    elif sort_option == "Lowest ROI":
        filtered_df = filtered_df.sort_values(by='roi_percent', ascending=True)
    elif sort_option == "Highest Current Price":
        filtered_df = filtered_df.sort_values(by='current_price', ascending=False)

    st.subheader("💼 Portfolio Overview")
    total_invested = filtered_df['purchase_price'].sum()
    total_current = filtered_df['current_price'].sum()
    
    if total_invested > 0:
        total_roi = ((total_current - total_invested) / total_invested) * 100
    else:
        total_roi = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Investment", f"${total_invested:,.2f}")
    col2.metric("Current Value", f"${total_current:,.2f}")
    col3.metric("Total Portfolio ROI", f"{total_roi:.2f}%", delta=f"{total_roi:.2f}%")

    st.divider()

    st.subheader(f"📦 Market Details ({len(filtered_df)} Items)")
    
    cols_per_row = 4
    for i in range(0, len(filtered_df), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        
        for idx, (index, row) in enumerate(batch.iterrows()):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"**{row['case_name']}**")
                    st.metric(
                        label=f"Cost: ${row['purchase_price']:.2f}",
                        value=f"${row['current_price']:.2f}",
                        delta=f"{row['roi_percent']:.1f}%"
                    )
                    st.caption(row['ai_advice'])

    st.divider()
    
    st.subheader("📊 In-Depth ROI Analysis")
    
    fig = px.bar(
        filtered_df, 
        x='case_name', 
        y='roi_percent',
        color='roi_percent',
        color_continuous_scale=['#e74c3c', '#f1c40f', '#2ecc71'], 
        labels={'case_name': 'Item Name', 'roi_percent': 'ROI (%)'},
        hover_data={'purchase_price': True, 'current_price': True} 
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cfd8dc'),
        xaxis_tickangle=-45,
        margin=dict(t=30, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Database not found. Please check your CSV file.")
except Exception as e:
    st.error(f"⚠️ System error occurred: {e}")
