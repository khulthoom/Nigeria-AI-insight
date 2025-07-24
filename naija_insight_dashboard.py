
import streamlit as st
import pandas as pd
import plotly.express as px
import openai

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
    st.markdown("**Example:** *Where is fuel cheapest in Nigeria?*")

    openai.api_key = st.secrets["openai_api_key"]
    user_input = st.text_input("Ask a question about the data:")
    if user_input:
        context = f"""
        Power Supply: {power_df.groupby('State')['Average_Supply_Hours'].mean().to_dict()}
        Market Prices: {price_df.groupby('Product')['Current_Price_NGN'].mean().to_dict()}
        Transport Delays: {transport_df.groupby('State')['Average_Delay_Minutes'].mean().to_dict()}
        Education: {education_df.groupby('State')['Enrollment_Percentage'].mean().to_dict()}
        Sentiment: {sentiment_df.groupby('Topic')['Sentiment_Score'].mean().to_dict()}
        """
       elif selected == "Ask Insight":
    st.header("Ask Insight (Offline Assistant 🤖)")
    st.markdown("Ask about electricity, transportation, or market prices in Nigeria.")

    user_input = st.text_input("Ask me anything:")

    if user_input:
        user_input_lower = user_input.lower()

        if "electricity" in user_input_lower or "power" in user_input_lower:
            st.success("Electricity supply data shows variability across states. Lagos had the highest consistent supply, while Yobe experienced more outages.")

        elif "transport" in user_input_lower or "road" in user_input_lower:
            st.success("Transport costs have been increasing steadily, especially in the North-East zone due to fuel price hikes.")

        elif "market" in user_input_lower or "price" in user_input_lower:
            st.success("Market prices for food items like rice and garri are highest in Abuja and Lagos. Kano has the most stable prices overall.")

        else:
            st.info("I couldn’t find an answer to that. Try asking about electricity, transportation, or market prices.")

