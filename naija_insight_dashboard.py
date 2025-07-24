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

# Streamlit config
st.set_page_config(page_title="Naija Insight Solutions", layout="wide")
st.title("🇳🇬 Naija Insight Solutions")
st.markdown("AI-powered data insights for Nigerian living — from power to prices and more.")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["⚡ Power Supply", "🛒 Market Prices", "🚗 Transportation", "🎓 Education", "💬 Sentiment", "🤖 Ask AI"])

# Pages
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

    # 🔐 Load API key securely
    openai.api_key = st.secrets["openai_api_key"]

    user_input = st.text_input("Ask a question about the data:")
    if user_input:
        # Create data context
        context = f"""
        Power Supply: {power_df.groupby('State')['Average_Supply_Hours'].mean().to_dict()}
        Market Prices: {price_df.groupby('Product')['Current_Price_NGN'].mean().to_dict()}
        Transport Delays: {transport_df.groupby('State')['Average_Delay_Minutes'].mean().to_dict()}
        Education: {education_df.groupby('State')['Enrollment_Percentage'].mean().to_dict()}
        Sentiment: {sentiment_df.groupby('Topic')['Sentiment_Score'].mean().to_dict()}
        """

        prompt = f"""
        You are a Nigerian data assistant. Use the data below to answer the user's question clearly and concisely.

        {context}

        User question: {user_input}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message["content"]
            st.success(answer)
        except Exception as e:
            st.error("⚠️ OpenAI API call failed or missing API key.")
