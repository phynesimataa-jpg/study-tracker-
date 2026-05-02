# study-tracker-
A Streamlit app to track study hours and visualize STEM progress. 
import pandas as pd
from datetime import datetime

class StudyTracker:
    def __init__(self, filename="study_log.csv"):
        self.filename = filename
        try:
            self.df = pd.read_csv(filename)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["Date", "Subject", "Duration_Min", "Topic"])

    def add_session(self, subject, duration, topic):
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Subject": subject,
            "Duration_Min": duration,
            "Topic": topic
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_entry])], ignore_index=True)
        self.df.to_csv(self.filename, index=False)
        print(f"✅ Logged {duration} minutes of {subject}!")

    def show_summary(self):
        # Groups by subject and sums the minutes
        summary = self.df.groupby("Subject")["Duration_Min"].sum()
        print("\n--- Study Summary ---")
        print(summary)

# Example Usage:
tracker = StudyTracker()
tracker.add_session("Physics", 60, "Kinematics")
tracker.add_session("Chemistry", 45, "Stoichiometry")
tracker.show_summary()


A Streamlit app to track study hours and visualize STEM progress.



