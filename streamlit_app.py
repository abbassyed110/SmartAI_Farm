import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Streamlit page config
st.set_page_config(
    page_title="SmartFarmAI - AI for Farmers",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar styling
st.markdown("""
    <style>
        .main { padding: 2rem; }
        .stMetric { background-color: #f0f0f0; padding: 1rem; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Backend URL (change to your deployed Flask URL)
BACKEND_URL = "http://127.0.0.1:5000"

# Session state for auth
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Main title
st.markdown("# 🌾 SmartFarmAI - AI-Powered Farming Solutions")
st.markdown("#### Empower your farm with AI-driven crop recommendations, disease detection & market access")

# Navigation
selected_page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📊 Dashboard",
        "🌱 Crop Recommendation",
        "🦠 Disease Detection",
        "⛅ Weather Alerts",
        "🛒 Marketplace",
        "📚 Knowledge Base",
        "👤 Profile",
        "🚪 Logout"
    ]
)

# ============================================
# HOME PAGE
# ============================================
if selected_page == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## Welcome to SmartFarmAI
        
        **Harness the power of AI to:**
        - 🌱 Get personalized crop recommendations based on soil & climate
        - 🦠 Detect plant diseases early with image analysis
        - ⛅ Receive weather alerts tailored to your farm
        - 🛒 Connect directly with buyers for fair prices
        - 📚 Access agricultural knowledge & best practices
        
        **Perfect for:** Small farmers | Marginal farms | Remote areas | Mobile-first users
        """)
        
        if st.button("🚀 Start Using SmartFarmAI", key="start_btn", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
    
    with col2:
        st.image("https://via.placeholder.com/400x300?text=SmartFarmAI+Dashboard", 
                use_column_width=True, caption="Manage your farm with ease")
    
    st.markdown("---")
    
    # Features grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Coverage", "All India", "50+ Languages")
    with col2:
        st.metric("📱 Offline", "Enabled", "Works Without Internet")
    with col3:
        st.metric("🤖 AI Models", "3 Active", "Real-time Predictions")
    with col4:
        st.metric("💰 Cost", "Free", "For Small Farmers")

# ============================================
# CROP RECOMMENDATION
# ============================================
elif selected_page == "🌱 Crop Recommendation":
    st.markdown("## 🌱 AI-Powered Crop Recommendation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        soil_type = st.selectbox(
            "Soil Type",
            ["clay", "sandy", "loamy", "silty", "peaty", "chalky", "black"]
        )
        ph_value = st.slider("Soil pH", 4.0, 9.0, 6.8, 0.1)
        rainfall = st.number_input("Annual Rainfall (mm)", 200, 2000, 850)
    
    with col2:
        temperature = st.number_input("Average Temperature (°C)", 5, 45, 26)
        humidity = st.slider("Average Humidity (%)", 30, 100, 65)
    
    if st.button("🔍 Get Crop Recommendations", use_container_width=True):
        payload = {
            "soil_type": soil_type,
            "ph_value": ph_value,
            "rainfall": rainfall,
            "temperature": temperature,
            "humidity": humidity
        }
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/crop_recommendation",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Recommendations Generated")
                
                # Display results
                for idx, crop in enumerate(data['recommended_crops'], 1):
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"### {idx}. {crop['crop'].title()}")
                        with col2:
                            st.metric("Confidence", f"{crop['confidence']*100:.1f}%")
                        with col3:
                            if st.button(f"➕ Add to Plan", key=f"add_{idx}"):
                                st.info(f"✅ {crop['crop']} added to your farm plan!")
                        
                        soil_match = "✅" if crop['suitable_for_soil'] else "❌"
                        ph_match = "✅" if crop['suitable_for_ph'] else "❌"
                        st.caption(f"{soil_match} Soil Match | {ph_match} pH Match")
            else:
                st.error("❌ Failed to get recommendations")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================
# DISEASE DETECTION
# ============================================
elif selected_page == "🦠 Disease Detection":
    st.markdown("## 🦠 Plant Disease Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Upload Plant Image")
        crop_name = st.selectbox(
            "Crop Type",
            ["rice", "wheat", "tomato", "potato", "maize", "other"]
        )
        uploaded_file = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔍 Analyze Disease", use_container_width=True):
                # In real scenario, save and send file path
                st.info("📤 Sending image to AI model...")
                st.success("✅ Disease Analysis Complete")
                st.markdown("""
                **Diagnosis:** Early Blight
                
                **Confidence:** 87%
                
                **Treatment:**
                - Remove infected leaves
                - Apply copper-based fungicides
                - Ensure proper air circulation
                """)
    
    with col2:
        st.markdown("### Previous Diagnoses")
        st.dataframe({
            "Crop": ["Tomato", "Potato", "Rice"],
            "Disease": ["Early Blight", "Late Blight", "Brown Spot"],
            "Date": ["2025-03-10", "2025-03-08", "2025-03-01"],
            "Status": ["Active", "Treated", "Resolved"]
        })

# ============================================
# WEATHER ALERTS
# ============================================
elif selected_page == "⛅ Weather Alerts":
    st.markdown("## ⛅ Weather Forecasting & Alerts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        lat = st.number_input("Farm Latitude", -90.0, 90.0, 12.9716)
        lon = st.number_input("Farm Longitude", -180.0, 180.0, 77.5946)
    
    with col2:
        if st.button("📍 Get Weather", use_container_width=True):
            try:
                response = requests.get(
                    f"{BACKEND_URL}/api/v1/weather_alerts",
                    params={"lat": lat, "lon": lon},
                    timeout=10
                )
                
                if response.status_code == 200:
                    alerts = response.json()['alerts']
                    
                    for alert in alerts:
                        if alert['severity'] == 'high':
                            icon = "🔴"
                        elif alert['severity'] == 'medium':
                            icon = "🟡"
                        else:
                            icon = "🟢"
                        
                        with st.container():
                            st.warning(f"{icon} {alert['type'].upper()}: {alert['message']}")
                            st.caption(f"Start: {alert['start_date']} | End: {alert['end_date']}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================
# MARKETPLACE
# ============================================
elif selected_page == "🛒 Marketplace":
    st.markdown("## 🛒 Agricultural Marketplace")
    
    st.markdown("### Buy & Sell Directly")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Sell Your Produce")
        crop = st.text_input("Crop Name", "Rice")
        quantity = st.number_input("Quantity (kg)", 100.0)
        price = st.number_input("Price per kg", 50.0)
        
        if st.button("📢 List for Sale", use_container_width=True):
            st.success(f"✅ Listed {quantity}kg of {crop} at ₹{price}/kg")
    
    with col2:
        st.markdown("### 🛍️ Browse Available Crops")
        st.dataframe({
            "Crop": ["Wheat", "Rice", "Cotton"],
            "Farmer": ["Mr. Singh", "Ms. Patel", "Mr. Kumar"],
            "Quantity": ["500kg", "200kg", "1000kg"],
            "Price": ["₹25/kg", "₹45/kg", "₹6000/kg"],
            "Location": ["Punjab", "Haryana", "Gujarat"]
        })

# ============================================
# KNOWLEDGE BASE
# ============================================
elif selected_page == "📚 Knowledge Base":
    st.markdown("## 📚 Agricultural Knowledge Base")
    
    category = st.selectbox(
        "Select Category",
        ["Crop Cultivation", "Disease Management", "Soil Health", "Water Management", "Market Trends"]
    )
    
    st.markdown(f"### Articles on {category}")
    
    articles = [
        {
            "title": "Best Practices for Rice Cultivation",
            "author": "Dr. Sharma",
            "date": "2025-03-10",
            "summary": "Learn the latest techniques for maximizing rice yield..."
        },
        {
            "title": "Managing Crop Diseases Naturally",
            "author": "Ms. Patel",
            "date": "2025-03-08",
            "summary": "Organic methods to prevent and treat common diseases..."
        }
    ]
    
    for article in articles:
        with st.container():
            st.markdown(f"### {article['title']}")
            st.caption(f"By {article['author']} • {article['date']}")
            st.write(article['summary'])
            st.markdown("[Read More →](#)")
            st.divider()

# ============================================
# PROFILE
# ============================================
elif selected_page == "👤 Profile":
    st.markdown("## 👤 Your Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Full Name", "Abbas Sayed")
        email = st.text_input("Email", "abbassayed7799@gmail.com")
        phone = st.text_input("Phone", "+91 9876543210")
        
        col1, col2 = st.columns(2)
        with col1:
            farm_size = st.number_input("Farm Size (acres)", 1.0, 100.0, 5.0)
            farm_location = st.text_input("Farm Location", "Maharashtra, India")
        
        with col2:
            latitude = st.number_input("Latitude", -90.0, 90.0, 19.0760)
            longitude = st.number_input("Longitude", -180.0, 180.0, 72.8856)
        
        language = st.selectbox("Preferred Language", ["English", "हिन्दी", "తెలుగు", "தமிழ்"])
        
        if st.form_submit_button("💾 Save Profile", use_container_width=True):
            st.success("✅ Profile updated successfully!")

# ============================================
# LOGOUT
# ============================================
elif selected_page == "🚪 Logout":
    st.markdown("## Logging out...")
    st.session_state.auth_token = None
    st.session_state.user = None
    st.info("✅ You have been logged out. Refresh to continue.")

# ============================================
# Footer
# ============================================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌾 SmartFarmAI")
with col2:
    st.caption("Empowering farmers with AI")
with col3:
    st.caption("© 2025 - All rights reserved")
