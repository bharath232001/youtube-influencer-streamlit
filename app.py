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
st.write("Interactive Brand-Oriented Dashboard | MCA Mini Project")

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

# Brand Selection
brand_type = st.sidebar.selectbox(
    "Select Brand Type",
    ["Tech", "Fashion", "Food"]
)

# Category Filter
category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df['category'].unique())
)

# Country Filter
country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df['country'].unique())
)

# Subscriber Range
min_sub, max_sub = int(df['subscriber_count'].min()), int(df['subscriber_count'].max())
sub_range = st.sidebar.slider(
    "Subscriber Range",
    min_value=min_sub,
    max_value=max_sub,
    value=(min_sub, max_sub)
)

# Chart Type Selector
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
# Brand → Category Mapping
# --------------------------------------------------
brand_category_map = {
    "Tech": ["Technology", "Education"],
    "Fashion": ["Fashion", "Lifestyle", "Beauty"],
    "Food": ["Food", "Cooking"]
}

preferred_categories = brand_category_map.get(brand_type, [])
brand_df = filtered_df.copy()

if preferred_categories:
    brand_df = brand_df[brand_df['category'].isin(preferred_categories)]

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
# Visualization Section
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
# Influencer Suitability Score
# --------------------------------------------------
st.subheader("🧮 Influencer Suitability Score")

brand_df['engagement'] = brand_df['view_count'] / brand_df['subscriber_count']
brand_df['norm_views'] = brand_df['view_count'] / brand_df['view_count'].max()
brand_df['norm_subs'] = brand_df['subscriber_count'] / brand_df['subscriber_count'].max()

brand_df['suitability_score'] = (
    0.5 * brand_df['engagement'] +
    0.3 * brand_df['norm_views'] +
    0.2 * brand_df['norm_subs']
)

# --------------------------------------------------
# Recommended for Brand Button
# --------------------------------------------------
st.subheader("🎯 Recommended Influencers for Brand")

if st.button("🔍 Recommend Influencers for Brand"):
    recommended = brand_df.sort_values(
        by='suitability_score',
        ascending=False
    ).head(10)

    st.success(f"Top Influencers Recommended for {brand_type} Brand")

    st.dataframe(
        recommended[[
            'channel_name',
            'category',
            'subscriber_count',
            'view_count',
            'suitability_score'
        ]]
    )

    # Download Option
    csv = recommended.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Recommended Influencers",
        data=csv,
        file_name=f"{brand_type.lower()}_brand_recommendations.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.success("Interactive Brand-Aware Dashboard Loaded Successfully 🎉")
st.caption("YouTube Influencer Performance Analysis | MCA Mini Project")
