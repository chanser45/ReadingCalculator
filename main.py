import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Reading Tracker App", page_icon="📚")

# Temporary session storage
if "log" not in st.session_state:
    st.session_state.log = {}

# Predefine variables to avoid undefined reference
fig_life = None
fig_bar = None
df = None

# Daily input
today = str(datetime.date.today())

st.header("📘 Reading Session")
pages_read = st.number_input("How many pages did you read today?", min_value=0, step=1, format="%d")
time_spent = st.number_input("How many minutes did you spend reading?", min_value=0, step=1, format="%d")

if st.button("Save"):
    st.session_state.log[today] = {
        "pages": pages_read,
        "minutes": time_spent,
    }
    st.success(f"Saved: {pages_read} pages and {time_spent} minutes on {today}")

# Stats calculations
reading_log = st.session_state.log
total_pages = sum(day["pages"] for day in reading_log.values())
total_minutes = sum(day["minutes"] for day in reading_log.values())

# Avoid division by zero
days_active = len(reading_log)
avg_daily_pages = total_pages / days_active if days_active > 0 else 0
avg_minutes = total_minutes / days_active if days_active > 0 else 0

# Estimates
yearly_estimate_pages = avg_daily_pages * 365
average_book_length = 300
books_per_year = yearly_estimate_pages / average_book_length

st.header("📊 Your Reading Statistics")
st.write(f"Total pages read: **{total_pages}**")
st.write(f"Total minutes spent reading: **{total_minutes} minutes**")
st.write(f"Average pages per day: **{avg_daily_pages:.2f}**")
st.write(f"Average minutes per day: **{avg_minutes:.2f} minutes**")
st.write(f"At this pace, you'll read **{int(yearly_estimate_pages)}** pages or about **{books_per_year:.1f}** books per year.")

# Screen-time motivation
pages_per_minute = total_pages / total_minutes if total_minutes > 0 else 0
pages_in_30min = pages_per_minute * 30
pages_in_60min = pages_per_minute * 60

st.subheader("🍿 Compare to Watching TV")
st.write(f"Instead of watching one 30-minute episode, you could read approximately **{pages_in_30min:.1f}** pages.")
st.write(f"One hour of reading equals approximately **{pages_in_60min:.1f}** pages.")

# Lifetime projection graph (1 to 50 years)
if avg_daily_pages > 0:
    st.subheader("📈 Lifetime Reading Projection")
    years = list(range(1, 51))
    projected_books = [(avg_daily_pages * 365 * y) / average_book_length for y in years]

    fig_life, ax_life = plt.subplots()
    ax_life.plot(years, projected_books, marker="o", color="blue")
    ax_life.set_title("Estimated Total Books Read Over Time")
    ax_life.set_xlabel("Years from Now")
    ax_life.set_ylabel("Books Read")
    st.pyplot(fig_life)

# Trend charts
if reading_log:
    st.subheader("📈 Weekly and Monthly Reading Trends")
    df = pd.DataFrame(
        [(date, val["pages"]) for date, val in reading_log.items()],
        columns=["Date", "Pages"]
    )
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df.set_index("Date", inplace=True)
    df_weekly = df.resample("W").sum()
    df_monthly = df.resample("M").sum()

    fig_trend, ax_trend = plt.subplots()
    df_weekly.plot(kind="bar", ax=ax_trend, legend=False, color="skyblue")
    ax_trend.set_title("Weekly Pages Read")
    ax_trend.set_ylabel("Pages")
    st.pyplot(fig_trend)

    fig_monthly, ax_monthly = plt.subplots()
    df_monthly.plot(kind="bar", ax=ax_monthly, legend=False, color="green")
    ax_monthly.set_title("Monthly Pages Read")
    ax_monthly.set_ylabel("Pages")
    st.pyplot(fig_monthly)

# Global comparison
comparison_data = {
    "Average Person (Global)": 12,
    "CEO Average": 60,
    "Bill Gates": 50,
    "UK Average": 15,
    "Turkey Average": 6,
    "France Average": 14,
    "US Average": 17
}

st.subheader("📚 Where You Stand Compared to Others")
comp_df = pd.DataFrame({
    "Reader Type": list(comparison_data.keys()),
    "Books per Year": list(comparison_data.values())
})

# Add user to comparison and sort again
comp_df.loc[len(comp_df)] = ["You", books_per_year]
comp_df = comp_df.sort_values("Books per Year").reset_index(drop=True)

fig_bar, ax_bar = plt.subplots()
bars = ax_bar.barh(comp_df["Reader Type"], comp_df["Books per Year"])

# Highlight the user's bar in orange
for bar, label in zip(bars, comp_df["Reader Type"]):
    if label == "You":
        bar.set_color("orange")

ax_bar.set_xlabel("Books per Year")
st.pyplot(fig_bar)

# Motivational messages
if books_per_year >= 20:
    st.balloons()
    st.success("You're doing amazing! If you keep it up, you'll finish more than 20 books a year!")
elif books_per_year >= 10:
    st.info("You're doing well! Looks like you'll read at least 10 books this year.")
else:
    st.warning("Your pace is a bit low, but every page counts. Keep going! 💪")

# Personalized suggestions based on slight increases in effort
st.subheader("🚀 Small Effort, Big Impact")
extra_minutes = 15
additional_pages = pages_per_minute * extra_minutes
new_yearly_pages = (avg_daily_pages + additional_pages / 1) * 365
new_books_per_year = new_yearly_pages / average_book_length

st.info(f"If you read just **15 minutes more** each day, you'd read **{new_books_per_year:.1f}** books per year instead of **{books_per_year:.1f}**.")

# Public transport simulation
daily_commute_minutes = 30
daily_commute_pages = pages_per_minute * daily_commute_minutes
commute_books_yearly = (daily_commute_pages * 365) / average_book_length

st.success(f"If you read during a daily 30-minute commute, you could finish **{commute_books_yearly:.1f}** extra books in a year! 📈")

# Social sharing image download
st.subheader("📸 Share Your Progress")
def fig_to_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

if fig_life:
    img_buf_life = fig_to_image(fig_life)
    st.download_button(
        label="Download Lifetime Projection",
        data=img_buf_life,
        file_name="reading_lifetime_projection.png",
        mime="image/png"
    )

if fig_bar:
    img_buf2 = fig_to_image(fig_bar)
    st.download_button(
        label="Download Comparison Chart as Image",
        data=img_buf2,
        file_name="reading_comparison.png",
        mime="image/png"
    )

# Trend insight (if enough data exists)
if df is not None and len(df) >= 3:
    this_week = df.last("7D").sum().values[0]
    prev_week = df[df.index < (df.index.max() - pd.Timedelta(days=7))].last("7D").sum().values[0]

    if prev_week > 0:
        delta = this_week - prev_week
        st.subheader("📈 Weekly Progress Insight")
        if delta > 0:
            st.success(f"You read {delta} more pages than the previous week! 🎉")
        elif delta < 0:
            st.warning(f"You read {abs(delta)} fewer pages than the week before. Try bouncing back! 💪")
        else:
            st.info("You're consistent with your last week. Keep going!")
