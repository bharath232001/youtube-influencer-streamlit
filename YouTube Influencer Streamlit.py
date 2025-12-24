# ============================================
# YouTube Influencer Performance Analysis
# MCA Mini Project
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------
# 1. Load Dataset
# --------------------------------------------
file_path = "youtube_channel_info_v1.csv"
df = pd.read_csv(file_path)

print("Dataset Loaded Successfully")
print(df.head())

# --------------------------------------------
# 2. Data Cleaning
# --------------------------------------------
df['category'] = df['category'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')

# Remove zero subscribers
df = df[df['subscriber_count'] > 0]

print("\nMissing Values Handled")

# --------------------------------------------
# 3. Basic Statistics
# --------------------------------------------
print("\nBasic Statistics:")
print(df[['subscriber_count', 'view_count', 'video_count']].describe())

# --------------------------------------------
# 4. Top 10 Influencers by Subscribers
# --------------------------------------------
top_subs = df.nlargest(10, 'subscriber_count')

plt.figure(figsize=(10,6))
sns.barplot(x='subscriber_count', y='channel_name', data=top_subs)
plt.title("Top 10 YouTube Influencers by Subscribers")
plt.xlabel("Subscribers")
plt.ylabel("Channel Name")
plt.tight_layout()
plt.savefig("top10_subscribers.png")
plt.close()

# --------------------------------------------
# 5. Top 10 Influencers by Views
# --------------------------------------------
top_views = df.nlargest(10, 'view_count')

plt.figure(figsize=(10,6))
sns.barplot(x='view_count', y='channel_name', data=top_views)
plt.title("Top 10 YouTube Influencers by Views")
plt.xlabel("Total Views")
plt.ylabel("Channel Name")
plt.tight_layout()
plt.savefig("top10_views.png")
plt.close()

# --------------------------------------------
# 6. Engagement Metric (Views per Subscriber)
# --------------------------------------------
df['views_per_subscriber'] = df['view_count'] / df['subscriber_count']

top_engagement = df.nlargest(10, 'views_per_subscriber')

plt.figure(figsize=(10,6))
sns.barplot(x='views_per_subscriber', y='channel_name', data=top_engagement)
plt.title("Top 10 Influencers by Engagement")
plt.xlabel("Views per Subscriber")
plt.ylabel("Channel Name")
plt.tight_layout()
plt.savefig("top10_engagement.png")
plt.close()

# --------------------------------------------
# 7. Subscribers vs Views Correlation
# --------------------------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(x='subscriber_count', y='view_count', data=df)
plt.title("Subscribers vs Views")
plt.xlabel("Subscribers")
plt.ylabel("Views")
plt.tight_layout()
plt.savefig("subscribers_vs_views.png")
plt.close()

correlation = df['subscriber_count'].corr(df['view_count'])
print("\nCorrelation between Subscribers and Views:", correlation)

# --------------------------------------------
# 8. Category-wise Distribution
# --------------------------------------------
plt.figure(figsize=(8,8))
df['category'].value_counts().head(10).plot.pie(autopct='%1.1f%%')
plt.title("Top YouTube Categories")
plt.ylabel("")
plt.tight_layout()
plt.savefig("category_distribution.png")
plt.close()

# --------------------------------------------
# 9. Country-wise Distribution
# --------------------------------------------
plt.figure(figsize=(10,6))
df['country'].value_counts().head(10).plot(kind='bar')
plt.title("Top Countries with YouTube Influencers")
plt.xlabel("Country")
plt.ylabel("Number of Channels")
plt.tight_layout()
plt.savefig("country_distribution.png")
plt.close()

# --------------------------------------------
# 10. Performance Score & Ranking
# --------------------------------------------
df['norm_subscribers'] = df['subscriber_count'] / df['subscriber_count'].max()
df['norm_views'] = df['view_count'] / df['view_count'].max()

df['performance_score'] = df['norm_subscribers'] + df['norm_views']

top_performers = df.sort_values(by='performance_score', ascending=False).head(10)

print("\nTop 10 Influencers by Performance Score:")
print(top_performers[['channel_name', 'subscriber_count', 'view_count', 'performance_score']])

# --------------------------------------------
# 11. End Message
# --------------------------------------------
print("\nYouTube Influencer Performance Analysis Completed Successfully")
print("Graphs saved as PNG files in project folder")
