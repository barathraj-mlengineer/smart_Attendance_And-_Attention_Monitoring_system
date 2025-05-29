import streamlit as st
from utils.db import get_attendance_data, get_attention_data
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title("Smart Classroom Dashboard")

tab1, tab2 = st.tabs(["Attendance", "Attention Monitoring"])

# Attendance Tab
with tab1:
    st.subheader("Attendance Records")
    df = get_attendance_data()
    st.dataframe(df)

    if not df.empty:
        # Attendance frequency per student (Histogram)
        fig1 = px.histogram(df, x="name", title="Attendance Frequency", color="name")
        st.plotly_chart(fig1, use_container_width=True)

        # Attendance over time (daily count line chart)
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        daily_counts = df.groupby("date").size().reset_index(name="Attendance Count")
        fig2 = px.line(daily_counts, x="date", y="Attendance Count", title="Daily Attendance Trend", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        # Attendance heatmap: students vs dates
        heatmap_df = df.copy()
        heatmap_df["date"] = pd.to_datetime(heatmap_df["timestamp"]).dt.date
        pivot = heatmap_df.pivot_table(index="name", columns="date", values="timestamp", aggfunc="count", fill_value=0)
        fig3 = px.imshow(pivot,
                         labels=dict(x="Date", y="Student", color="Attendance Count"),
                         title="Attendance Heatmap",
                         aspect="auto")
        st.plotly_chart(fig3, use_container_width=True)

# Attention Tab
with tab2:
    st.subheader("Attention Records")
    adf = get_attention_data()
    st.dataframe(adf)

    if not adf.empty:
        # Pie chart for overall attentive vs not attentive
        att_counts = adf["attentive"].value_counts().rename({True: "Attentive", False: "Not Attentive"})
        pie_df = att_counts.reset_index()
        pie_df.columns = ["Attention", "Count"]  # Correct column names
        fig4 = px.pie(pie_df, names="Attention", values="Count", title="Overall Attention Distribution")
        st.plotly_chart(fig4, use_container_width=True)

        # Bar chart: attention counts per student
        attention_stats = adf.groupby(["name", "attentive"]).size().unstack(fill_value=0)
        attentive_vals = attention_stats.get(True, pd.Series([0]*len(attention_stats), index=attention_stats.index))
        not_attentive_vals = attention_stats.get(False, pd.Series([0]*len(attention_stats), index=attention_stats.index))

        fig5 = go.Figure(data=[
            go.Bar(name="Attentive", x=attention_stats.index, y=attentive_vals),
            go.Bar(name="Not Attentive", x=attention_stats.index, y=not_attentive_vals)
        ])
        fig5.update_layout(barmode="stack", title="Attention by Student", xaxis_title="Student", yaxis_title="Count")
        st.plotly_chart(fig5, use_container_width=True)

        # Line chart: attention over time (hourly)
        adf["timestamp"] = pd.to_datetime(adf["timestamp"])
        time_df = adf.set_index("timestamp").groupby([pd.Grouper(freq="h"), "attentive"]).size().unstack(fill_value=0)
        fig6 = px.line(time_df, x=time_df.index, y=time_df.columns, title="Hourly Attention Trend")
        st.plotly_chart(fig6, use_container_width=True)
