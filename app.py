import streamlit as st
import pandas as pd

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Drip Guide", page_icon="💧", layout="wide")

st.title("💧 Drip Guide – Smart Fashion Recommender")
st.markdown("Find your perfect outfit based on your vibe, season, and trends ✨")

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("myntra_data.csv")
df.columns = df.columns.str.strip()

# --------------------------
# FILTER ONLY ITEMS WITH IMAGES
# --------------------------
valid_items = ["shirt", "t-shirt", "jeans", "dress", "jacket"]

df = df[df["Description"].str.lower().apply(
    lambda x: any(item in x for item in valid_items)
)]

# --------------------------
# ADD SEASON
# --------------------------
def assign_season(desc):
    desc = str(desc).lower()
    if "jacket" in desc:
        return "Winter"
    elif "t-shirt" in desc or "shirt" in desc:
        return "Summer"
    else:
        return "All Season"

df["Season"] = df["Description"].apply(assign_season)

# --------------------------
# IMAGE FUNCTION (ONLY VALID)
# --------------------------
def get_image(desc):
    desc = str(desc).lower()

    if "shirt" in desc:
        return "images/shirt.png"
    elif "t-shirt" in desc:
        return "images/tshirt.png"
    elif "jeans" in desc:
        return "images/jeans.png"
    elif "dress" in desc:
        return "images/dress.png"
    elif "jacket" in desc:
        return "images/jacket.png"
    else:
        return None  # IMPORTANT

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.header("🔍 Customize Your Style")

gender = st.sidebar.selectbox("Gender", df["Gender"].unique())
season = st.sidebar.selectbox("Season", df["Season"].unique())
color = st.sidebar.selectbox("Color", df["PrimaryColor"].dropna().unique())

price_range = st.sidebar.slider(
    "Price Range",
    int(df["Price (INR)"].min()),
    int(df["Price (INR)"].max()),
    (500, 2000)
)

# --------------------------
# FILTER DATA
# --------------------------
filtered_df = df[
    (df["Gender"] == gender) &
    (df["Season"] == season) &
    (df["PrimaryColor"] == color) &
    (df["Price (INR)"] >= price_range[0]) &
    (df["Price (INR)"] <= price_range[1])
]

# --------------------------
# TRENDING
# --------------------------
st.subheader("🔥 Trending Picks")

trending = df.sort_values(by="Price (INR)", ascending=False).head(10)

cols = st.columns(3)
count = 0

for _, row in trending.iterrows():
    img = get_image(row["Description"])

    if img:
        with cols[count % 3]:
            st.image(img, use_container_width=True)
            st.markdown(f"**{row['ProductName']}**")
            st.write(row['ProductBrand'])
            st.write(f"₹{row['Price (INR)']}")
        count += 1

st.markdown("---")

# --------------------------
# RECOMMENDATIONS
# --------------------------
st.subheader("🛍 Your Personalized Drip")

if not filtered_df.empty:
    cols = st.columns(3)
    count = 0

    for _, row in filtered_df.iterrows():
        img = get_image(row["Description"])

        if img:
            with cols[count % 3]:
                st.image(img, use_container_width=True)
                st.markdown(f"**{row['ProductName']}**")
                st.write(row['ProductBrand'])
                st.write(f"{row['PrimaryColor']} | {row['Season']}")
                st.write(f"₹{row['Price (INR)']}")
            count += 1

else:
    st.warning("No matches found. Try different filters.")

# --------------------------
# SMART SUGGESTION
# --------------------------
st.subheader("🤖 Smart Suggestion")

if not filtered_df.empty:
    suggestion = filtered_df.sample(1).iloc[0]
    img = get_image(suggestion["Description"])

    if img:
        st.image(img, width=200)
        st.success(
            f"Try **{suggestion['ProductName']}** from {suggestion['ProductBrand']} for a perfect {season} look!"
        )

# --------------------------
# FOOTER
# --------------------------
st.markdown("---")
st.caption("Drip Guide – Fashion Recommendation System 💧")
