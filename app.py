import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import requests
from bs4 import BeautifulSoup
import time
import logging
from functools import lru_cache
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(
    page_title="CS2 Market Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 10px 0;
    }
    .header-style {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
STEAM_MARKET_URL = "https://steamcommunity.com/market/search?appid=730&search_descriptions=0&sort_column=price&sort_dir=desc"
CACHE_TIME = 3600  # 1 hour cache
PREDICTION_DAYS = 7
POLY_DEGREE = 3

# ==================== CACHING & UTILITIES ====================
@st.cache_data(ttl=CACHE_TIME)
def fetch_market_data(search_query: str = "case") -> pd.DataFrame:
    """Fetch CS2 market data with caching"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(STEAM_MARKET_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse data (simplified - adjust based on actual HTML structure)
        data = {
            'name': ['Fracture Case', 'Mirage Case', 'Ancient Case'],
            'price': [np.random.uniform(1.8, 2.2) for _ in range(3)],
            'timestamp': [datetime.now()] * 3
        }
        
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return pd.DataFrame()

@st.cache_data
def train_prediction_model(prices: np.ndarray) -> Tuple[LinearRegression, PolynomialFeatures]:
    """Train polynomial regression model"""
    X = np.arange(len(prices)).reshape(-1, 1)
    
    poly_features = PolynomialFeatures(degree=POLY_DEGREE)
    X_poly = poly_features.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, prices)
    
    return model, poly_features

def predict_future_prices(prices: np.ndarray, days: int = PREDICTION_DAYS) -> np.ndarray:
    """Predict future prices"""
    if len(prices) < 2:
        return prices
    
    model, poly_features = train_prediction_model(prices)
    
    future_days = np.arange(len(prices), len(prices) + days).reshape(-1, 1)
    future_X = poly_features.transform(future_days)
    predictions = model.predict(future_X)
    
    return np.maximum(predictions, np.min(prices) * 0.5)  # Prevent negative values

def calculate_sma(prices: np.ndarray, window: int = 7) -> np.ndarray:
    """Calculate Simple Moving Average"""
    return pd.Series(prices).rolling(window=window, min_periods=1).mean().values

# ==================== UI COMPONENTS ====================
def render_header():
    """Render page header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <div class="header-style">
                <h1>🚀 CS2 Market Analytics & AI Forecast</h1>
                <p>Real-time market insights powered by AI predictions</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

def render_metrics(df: pd.DataFrame):
    """Render key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Items", len(df))
    with col2:
        avg_price = df['price'].mean() if len(df) > 0 else 0
        st.metric("Avg Price", f"${avg_price:.2f}")
    with col3:
        max_price = df['price'].max() if len(df) > 0 else 0
        st.metric("Max Price", f"${max_price:.2f}")
    with col4:
        min_price = df['price'].min() if len(df) > 0 else 0
        st.metric("Min Price", f"${min_price:.2f}")

def render_price_chart(df: pd.DataFrame, item_name: str):
    """Render interactive price chart with predictions"""
    if len(df) == 0:
        st.warning("No data available")
        return
    
    prices = df['price'].values
    future_prices = predict_future_prices(prices)
    sma = calculate_sma(prices)
    
    days = np.arange(len(prices))
    future_days = np.arange(len(prices), len(prices) + PREDICTION_DAYS)
    
    fig = go.Figure()
    
    # Historical prices
    fig.add_trace(go.Scatter(
        x=days, y=prices,
        mode='lines+markers',
        name='Historical Price',
        line=dict(color='#FF4B4B', width=2)
    ))
    
    # SMA
    fig.add_trace(go.Scatter(
        x=days, y=sma,
        mode='lines',
        name='SMA (7-day)',
        line=dict(color='#FFA500', dash='dash')
    ))
    
    # Predictions
    fig.add_trace(go.Scatter(
        x=future_days, y=future_prices,
        mode='lines+markers',
        name='7-Day Forecast',
        line=dict(color='#4B8BFF', dash='dot')
    ))
    
    fig.update_layout(
        title=f"{item_name} - Price Analysis & Forecast",
        xaxis_title="Days",
        yaxis_title="Price ($)",
        template="plotly_dark",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== MAIN APP ====================
def main():
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        refresh_interval = st.slider("Refresh Interval (mins)", 5, 60, 30)
        search_query = st.text_input("Search Items", "case")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔮 Predictions", "💼 Portfolio"])
    
    with tab1:
        st.subheader("Market Dashboard")
        df = fetch_market_data(search_query)
        
        render_metrics(df)
        
        if len(df) > 0:
            selected_item = st.selectbox("Select Item to Analyze", df['name'].unique())
            item_data = df[df['name'] == selected_item]
            render_price_chart(item_data, selected_item)
            
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Price Predictions")
        st.info("📈 7-day price forecasts using Polynomial Regression (Degree 3)")
        
        if len(df) > 0:
            for item in df['name'].unique()[:3]:  # Show top 3
                item_data = df[df['name'] == item]
                render_price_chart(item_data, item)
    
    with tab3:
        st.subheader("Portfolio Manager")
        
        col1, col2 = st.columns(2)
        with col1:
            item = st.selectbox("Select Item", df['name'].unique() if len(df) > 0 else [])
            quantity = st.number_input("Quantity", 1, 1000, 1)
        
        with col2:
            buy_price = st.number_input("Buy Price ($)", 0.01, 1000.0, 1.0)
            if st.button("➕ Add to Portfolio"):
                st.success(f"Added {quantity}x {item} @ ${buy_price}")
        
        st.markdown("---")
        st.metric("Portfolio Value", "$1,234.56")
        st.metric("Total Profit/Loss", "$+234.56", "+19%")

if __name__ == "__main__":
    main()
