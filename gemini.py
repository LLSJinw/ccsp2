import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DATA_FILE = "ccsp_study_log.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Domain and Resource Definitions ---
CCSP_DOMAINS = {
    "Domain 1: Cloud Concepts, Architecture, and Design (17%)": [],
    "Domain 2: Cloud Data Security (20%)": [],
    "Domain 3: Cloud Platform & Infrastructure Security (17%)": [],
    "Domain 4: Cloud Application Security (17%)": [],
    "Domain 5: Cloud Security Operations (16%)": [],
    "Domain 6: Legal, Risk, and Compliance (13%)": [
        "6.1 Articulate legal requirements and unique risks within the cloud environment",
        "6.2 Understand privacy issues",
        "6.3 Understand audit process, methodologies, and required adaptations for a cloud environment",
        "6.4 Understand implications of cloud to enterprise risk management",
        "6.5 Understand outsourcing and cloud contract design",
        "6.6 Execute vendor management"
    ]
}

SUGGESTED_RESOURCES = [
    "Gwen Bettwy’s Udemy Courses/Materials",
    "Pocket Prep CCSP App",
    "Boson ExSim-Max for CCSP",
    "(ISC)² Official Practice Tests",
    "CSA Security Guidance v5",
    "NIST SP 800-145",
    "NIST SP 800-146",
    "NIST SP 800-125",
    "(ISC)² CCSP CBK",
    "Destination Certification MindMaps",
    "SkillCertPro CCSP Cheat Sheet",
    "Mike Chapple's Review"
]

# --- File I/O Functions ---
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Timestamp", "Date", "Domain", "Sub-Objective",
            "Resources Used", "Time Spent (Minutes)", "Notes",
            "Confidence (1-5)", "Status"
        ])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    initialize_data_file()
    try:
        return pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=[
            "Timestamp", "Date", "Domain", "Sub-Objective",
            "Resources Used", "Time Spent (Minutes)", "Notes",
            "Confidence (1-5)", "Status"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_study_entry(entry_date, domain, sub_objective, resources_used, time_spent, notes, confidence, status):
    df = load_data()
    timestamp = datetime.now().strftime(DATE_FORMAT)
    new_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Date": entry_date.strftime("%Y-%m-%d"),
        "Domain": domain,
        "Sub-Objective": sub_objective,
        "Resources Used": ", ".join(resources_used),
        "Time Spent (Minutes)": time_spent,
        "Notes": notes,
        "Confidence (1-5)": confidence,
        "Status": status
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

# --- Streamlit UI ---
st.set_page_config(page_title="CCSP Study Tracker", layout="wide")
st.title("🚀 Personalized CCSP Certification Study Tracker")
st.markdown("Track your daily CCSP study sessions with structured logging and progress review.")

page = st.sidebar.radio("Navigation", ["Add Study Entry", "View Progress Log"])

if page == "Add Study Entry":
    st.header("📝 Add New Study Entry")
    with st.form("entry_form"):
        entry_date = st.date_input("Study Date", value=datetime.today())
        selected_domain = st.selectbox("Domain Studied", ["--Select a Domain--"] + list(CCSP_DOMAINS.keys()))

        sub_objectives = CCSP_DOMAINS.get(selected_domain, [])
        if sub_objectives:
            selected_sub = st.selectbox("Sub-Objective", sub_objectives)
        else:
            selected_sub = "General"

        resources = st.multiselect("Resources Used", options=SUGGESTED_RESOURCES)
        other_resource = st.text_input("Other Resource (if any)")

        time_spent = st.number_input("Time Spent (Minutes)", 1, 90, 60, 5)
        notes = st.text_area("Notes / Key Takeaways")
        confidence = st.slider("Confidence Level", 1, 5, 3)
        status = st.selectbox("Status", ["Not Started", "In Progress", "Needs Review", "Completed"])

        if st.form_submit_button("Add Entry"):
            if selected_domain == "--Select a Domain--":
                st.error("Please select a valid domain.")
            else:
                resources_used = resources.copy()
                if other_resource:
                    resources_used.append(other_resource.strip())
                add_study_entry(entry_date, selected_domain, selected_sub, resources_used, time_spent, notes, confidence, status)
                st.success("Entry added successfully!")

elif page == "View Progress Log":
    st.header("📊 Study Progress Log")
    df = load_data()

    if df.empty:
        st.info("No entries yet. Add your first study entry!")
    else:
        st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)

        st.subheader("📈 Summary")
        st.metric("Total Study Time (Hours)", f"{df['Time Spent (Minutes)'].sum() / 60:.2f}")
        st.metric("Average Confidence", f"{df['Confidence (1-5)'].mean():.2f} / 5")

        st.subheader("⏱ Time Spent per Domain")
        domain_chart = df.groupby("Domain")["Time Spent (Minutes)"].sum().sort_values(ascending=False)
        st.bar_chart(domain_chart)

        st.subheader("🚦 Status Overview")
        status_chart = df["Status"].value_counts()
        st.bar_chart(status_chart)

st.sidebar.markdown("---")
st.sidebar.markdown("Built to support your CCSP study journey. Good luck! 💪")
