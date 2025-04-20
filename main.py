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
fig_goal = None
persona = ""
df = None

# Daily input
today = str(datetime.date.today())

st.header("📘 Reading Session")
pages_read = st.number_input("How many pages did you read today?", min_value=0, step=1, format="%d")
time_spent = st.number_input("How many minutes did you spend reading?", min_value=0, step=1, format="%d")

if st.button("Calculate My Earnings"):
    # Overwrite today's data completely instead of adding to it
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
st.write("")
st.success(f"At this pace, you'll read **{int(yearly_estimate_pages)}** pages or about **{books_per_year:.1f}** books per year.")
st.info('“The man who moves a mountain begins by carrying away small stones." -Confucius')
st.write("")
st.write("")
st.write("")
# Reader Persona
st.subheader("🧙‍♂️ Your Reader Persona")
if avg_daily_pages < 15:
    persona = "📖 Casual Reader – You enjoy a light read now and then. Every page is a small step forward!"
elif avg_daily_pages < 30:
    persona = "📚 Steady Explorer – Books are part of your life. Keep up the consistent pace!"
elif avg_daily_pages < 50:
    persona = "🚀 Page Devourer – You're truly making the most of your time!"
else:
    persona = "🌟 Literary Beast – You read more than most people ever dream to. Legend!"
st.info(persona)
st.write("")
st.write("")
# When will you finish your next book?
st.subheader("⏳ Time to Finish a Book")
if avg_daily_pages > 0:
    days_to_finish = average_book_length / avg_daily_pages
    st.write(f"At this pace, you'll finish a 300-page book in approximately **{days_to_finish:.1f}** days.")

# Screen-time motivation
pages_per_minute = total_pages / total_minutes if total_minutes > 0 else 0
pages_in_30min = pages_per_minute * 30
pages_in_60min = pages_per_minute * 60
st.write("")
st.write("")
st.subheader("🍿 Compare to Watching TV")
st.write(f"Instead of watching one 30-minute episode, you could read approximately **{pages_in_30min:.1f}** pages.")
st.write(f"One hour of reading equals approximately **{pages_in_60min:.1f}** pages.")
st.write("")
st.write("")
# Lifetime projection graph (1 to 40 years)
if avg_daily_pages > 0:
    st.subheader("📈 Lifetime Reading Projection")
    years = list(range(1, 41))
    projected_books = [(avg_daily_pages * 365 * y) / average_book_length for y in years]

    fig_life, ax_life = plt.subplots()
    ax_life.plot(years, projected_books, marker="o", color="blue")
    ax_life.set_title("Estimated Total Books Read Over Time")
    ax_life.set_xlabel("Years from Now")
    ax_life.set_ylabel("Books Read")
    st.pyplot(fig_life)

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
st.write("")
st.write("")
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
if books_per_year >= 25:
    st.balloons()
    st.success("You're doing amazing! If you keep it up, you'll finish more than 20 books a year!")
elif books_per_year >= 15:
    st.info("You're doing well! Looks like you'll read at least 10 books this year.")
else:
    st.warning("Your pace is a bit low, but every page counts. Keep going! 💪")

# Personalized suggestions based on slight increases in effort
st.subheader("🚀 Small Effort, Big Impact")
extra_minutes = 10
additional_pages = pages_per_minute * extra_minutes
new_yearly_pages = (avg_daily_pages + additional_pages / 1) * 365
new_books_per_year = new_yearly_pages / average_book_length

st.info(f"If you read just **10 minutes more** each day, you'd read **{new_books_per_year:.1f}** books per year instead of **{books_per_year:.1f}**.")
st.info('"Victory belongs to those who can say little more."')

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
