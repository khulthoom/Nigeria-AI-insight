import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
power_df = pd.read_csv("power_supply.csv")
price_df = pd.read_csv("market_prices.csv")
transport_df = pd.read_csv("transport_delays.csv")
education_df = pd.read_csv("education_access.csv")
sentiment_df = pd.read_csv("social_sentiment.csv")

st.set_page_config(page_title="Naija Insight Solutions", layout="wide")
st.title("🇳🇬 Naija Insight Solutions")
st.markdown("AI-powered data insights for Nigerian living — from power to prices and more.")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["⚡ Power Supply", "🛒 Market Prices", "🚗 Transportation", "🎓 Education", "💬 Sentiment", "🤖 Ask AI"])

if page == "⚡ Power Supply":
    st.header("Power Supply Insights")
    fig = px.line(power_df, x="Month", y="Average_Supply_Hours", color="State", title="Average Power Supply (Hours per Day)")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🛒 Market Prices":
    st.header("Market Price Comparisons")
    selected_product = st.selectbox("Select Product", price_df["Product"].unique())
    filtered = price_df[price_df["Product"] == selected_product]
    fig = px.bar(filtered, x="Location", y="Current_Price_NGN", title=f"Current Price of {selected_product}")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🚗 Transportation":
    st.header("Transportation Delay Overview")
    fig = px.bar(transport_df, x="State", y="Average_Delay_Minutes", color="Month", barmode="group",
                 title="Average Transportation Delay (Minutes)")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🎓 Education":
    st.header("Education Access by State")
    fig = px.bar(education_df, x="State", y="Enrollment_Percentage", color="Education_Level",
                 barmode="group", title="Enrollment Rates by Education Level")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💬 Sentiment":
    st.header("Social Media Sentiment by Topic")
    fig = px.box(sentiment_df, x="Topic", y="Sentiment_Score", color="Topic", title="Sentiment on Social Media")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Ask AI":
    st.header("Ask Naija Insight AI 🤖")
    st.markdown("Ask about electricity, transport, market prices, education, or sentiment.")

    user_input = st.text_input("Your question:")
    if user_input:
        ui = user_input.lower()
        if "electricity" in ui or "power" in ui:
            st.success("🔌 Lagos and Abuja show higher average daily power supply compared to other states.")
        elif "transport" in ui or "delay" in ui:
            st.success("🚗 Transportation delays are worst in Kano and Rivers, with about 60–80 minutes average.")
        elif "price" in ui or "market" in ui:
            st.success("🛒 Rice and onions are most expensive in Lagos; prices are more stable in Kano.")
        elif "education" in ui or "enrollment" in ui:
            st.success("🎓 Tertiary enrollment is highest in Lagos (around 90%), while secondary is lower in northern states.")
        elif "sentiment" in ui or "social" in ui:
            st.success("💬 Public sentiment is more positive about education than electricity.")
        else:
            st.info("Sorry, I can’t answer that. Try asking about electricity, transport, market prices, education, or sentiment.")
