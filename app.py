import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="YouTube Influencer Analytics",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 YouTube Influencer Performance Analysis")
st.write("Interactive Streamlit Dashboard – MCA Mini Project")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("youtube_channel_info_v1.csv")

df = load_data()

# Data Cleaning
df['category'] = df['category'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df = df[df['subscriber_count'] > 0]

st.success("Dataset Loaded Successfully ✅")

# --------------------------------------------------
# SIDEBAR – USER INTERACTION
# --------------------------------------------------
st.sidebar.header("🎛 User Controls")

# Category filter
category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df['category'].unique())
)

# Country filter
country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df['country'].unique())
)

# Subscriber range slider
min_sub, max_sub = int(df['subscriber_count'].min()), int(df['subscriber_count'].max())
sub_range = st.sidebar.slider(
    "Subscriber Range",
    min_value=min_sub,
    max_value=max_sub,
    value=(min_sub, max_sub)
)

# Chart selector
chart_type = st.sidebar.radio(
    "Choose Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"]
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[filtered_df['category'] == category]

if country != "All":
    filtered_df = filtered_df[filtered_df['country'] == country]

filtered_df = filtered_df[
    (filtered_df['subscriber_count'] >= sub_range[0]) &
    (filtered_df['subscriber_count'] <= sub_range[1])
]

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------
st.subheader("📋 Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# --------------------------------------------------
# Key Metrics
# --------------------------------------------------
st.subheader("📌 Summary Statistics")

c1, c2, c3 = st.columns(3)
c1.metric("Channels", filtered_df.shape[0])
c2.metric("Total Subscribers", int(filtered_df['subscriber_count'].sum()))
c3.metric("Total Views", int(filtered_df['view_count'].sum()))

# --------------------------------------------------
# Chart Display (USER SELECTED)
# --------------------------------------------------
st.subheader("📈 Visualization Output")

top_data = filtered_df.nlargest(10, 'subscriber_count')

if chart_type == "Bar Chart":
    fig, ax = plt.subplots()
    sns.barplot(
        x='subscriber_count',
        y='channel_name',
        data=top_data,
        ax=ax
    )
    ax.set_title("Top 10 Influencers by Subscribers")
    st.pyplot(fig)

elif chart_type == "Line Chart":
    trend = filtered_df.sort_values("subscriber_count").head(50)
    st.line_chart(
        trend.set_index("subscriber_count")["view_count"]
    )

elif chart_type == "Scatter Plot":
    filtered_df['engagement'] = filtered_df['view_count'] / filtered_df['subscriber_count']
    fig, ax = plt.subplots()
    sns.scatterplot(
        x='subscriber_count',
        y='engagement',
        data=filtered_df.sample(min(300, len(filtered_df))),
        ax=ax
    )
    ax.set_title("Subscribers vs Engagement")
    st.pyplot(fig)

elif chart_type == "Histogram":
    fig, ax = plt.subplots()
    ax.hist(filtered_df['subscriber_count'], bins=30)
    ax.set_title("Subscriber Distribution")
    st.pyplot(fig)

# --------------------------------------------------
# Ranking Table (USER ACTION)
# --------------------------------------------------
st.subheader("🏆 Influencer Ranking")

filtered_df['norm_subs'] = filtered_df['subscriber_count'] / filtered_df['subscriber_count'].max()
filtered_df['norm_views'] = filtered_df['view_count'] / filtered_df['view_count'].max()
filtered_df['performance_score'] = filtered_df['norm_subs'] + filtered_df['norm_views']

top_ranked = filtered_df.sort_values(
    by='performance_score',
    ascending=False
).head(10)

st.dataframe(
    top_ranked[['channel_name', 'subscriber_count', 'view_count', 'performance_score']]
)

# --------------------------------------------------
# Download Button
# --------------------------------------------------
csv = top_ranked.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Top Influencers CSV",
    data=csv,
    file_name="top_youtube_influencers.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.success("Interactive Dashboard Loaded Successfully 🎉")
st.caption("YouTube Influencer Analytics | MCA Mini Project")
