import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="YouTube Influencer Analytics", layout="wide")

# ---- TITLE ----
st.title("📊 YouTube Influencer Performance Analysis")
st.write("MCA Mini Project – Streamlit Dashboard")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    return pd.read_csv("youtube_channel_info_v1.csv")

df = load_data()

st.success("Dataset Loaded Successfully")

# ---- SHOW DATA ----
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---- BASIC METRICS ----
st.subheader("Key Statistics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Channels", df.shape[0])
col2.metric("Total Subscribers", int(df['subscriber_count'].sum()))
col3.metric("Total Views", int(df['view_count'].sum()))

# ---- TOP SUBSCRIBERS ----
st.subheader("Top 10 Influencers by Subscribers")

top_subs = df.nlargest(10, 'subscriber_count')

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x='subscriber_count', y='channel_name', data=top_subs, ax=ax1)
ax1.set_xlabel("Subscribers")
ax1.set_ylabel("Channel")
st.pyplot(fig1)

# ---- TOP VIEWS ----
st.subheader("Top 10 Influencers by Views")

top_views = df.nlargest(10, 'view_count')

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(x='view_count', y='channel_name', data=top_views, ax=ax2)
ax2.set_xlabel("Views")
ax2.set_ylabel("Channel")
st.pyplot(fig2)

# ---- ENGAGEMENT ----
st.subheader("Engagement Analysis")

df['views_per_subscriber'] = df['view_count'] / df['subscriber_count']
top_engage = df.nlargest(10, 'views_per_subscriber')

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(x='views_per_subscriber', y='channel_name', data=top_engage, ax=ax3)
ax3.set_xlabel("Views per Subscriber")
ax3.set_ylabel("Channel")
st.pyplot(fig3)

st.success("Dashboard Loaded Successfully ✅")
