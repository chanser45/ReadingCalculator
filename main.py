import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Reading Tracker App", page_icon="📚")

# Temporary session storage
if "log" not in st.session_state:
    st.session_state.log = {}

# Daily input
today = str(datetime.date.today())

st.header("📘 Reading Session")
pages_read = st.number_input("How many pages did you read today?", min_value=0, step=1)
time_spent = st.number_input("How many minutes did you spend reading?", min_value=0, step=1)

if st.button("Save"):
    st.session_state.log[today] = {
        "pages": st.session_state.log.get(today, {}).get("pages", 0) + pages_read,
        "minutes": st.session_state.log.get(today, {}).get("minutes", 0) + time_spent,
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

# Visualization: Histogram of daily pages
fig_hist = None
if reading_log:
    st.subheader("📊 Distribution of Pages Read per Day")
    df = pd.DataFrame(
        [(date, val["pages"]) for date, val in reading_log.items()],
        columns=["Date", "Pages"]
    )
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # Histogram
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(df["Pages"], bins=10)
    ax_hist.set_xlabel("Pages Read")
    ax_hist.set_ylabel("Number of Days")
    st.pyplot(fig_hist)

# Global comparison
comparison_data = {
    "Average Person (Global)": 12,
    "CEO Average": 60,
    "Bill Gates": 50,
    "UK Average": 15,
    "India Average": 16,
    "Finland Average": 16,
    "France Average": 14,
    "US Average": 17
}

st.subheader("📚 Where You Stand Compared to Others")
comp_df = pd.DataFrame({
    "Reader Type": list(comparison_data.keys()) + ["You"],
    "Books per Year": list(comparison_data.values()) + [books_per_year]
})
comp_df = comp_df.sort_values("Books per Year")

fig_bar, ax_bar = plt.subplots()
bars = ax_bar.barh(comp_df["Reader Type"], comp_df["Books per Year"])
bars[-1].set_color("orange")  # Highlight user
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

# Social sharing image download
st.subheader("📸 Share Your Progress")
def fig_to_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

if fig_hist:
    img_buf = fig_to_image(fig_hist)
    st.download_button(
        label="Download Histogram as Image",
        data=img_buf,
        file_name="reading_progress.png",
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