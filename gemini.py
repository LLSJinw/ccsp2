import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DATA_FILE = "ccsp_study_log.csv"
TEST_LOG_FILE = "ccsp_test_log.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Domain and Sub-objective Definitions ---
CCSP_DOMAINS = {
    "Domain 1: Cloud Concepts, Architecture, and Design (17%)": [
        "1.1 Understand cloud computing concepts",
        "1.2 Describe cloud reference architecture",
        "1.3 Understand security concepts relevant to cloud computing",
        "1.4 Understand design principles of secure cloud computing"
    ],
    "Domain 2: Cloud Data Security (20%)": [
        "2.1 Describe cloud data lifecycle",
        "2.2 Design and implement cloud data storage architectures",
        "2.3 Design and apply data security strategies",
        "2.4 Understand data discovery and classification",
        "2.5 Design and implement data rights management",
        "2.6 Plan and implement data retention, deletion, and archiving policies",
        "2.7 Design and implement auditability, traceability, and accountability of data events"
    ],
    "Domain 3: Cloud Platform & Infrastructure Security (17%)": [
        "3.1 Comprehend cloud infrastructure components",
        "3.2 Design and plan security controls",
        "3.3 Plan disaster recovery and business continuity management"
    ],
    "Domain 4: Cloud Application Security (17%)": [
        "4.1 Advocate training and awareness for application security",
        "4.2 Describe the Software Development Lifecycle (SDLC) process",
        "4.3 Apply cloud software assurance and validation",
        "4.4 Use verified secure software",
        "4.5 Comprehend the specifics of cloud application architecture"
    ],
    "Domain 5: Cloud Security Operations (16%)": [
        "5.1 Implement and build physical and logical infrastructure for cloud environment",
        "5.2 Operate and maintain cloud environment securely",
        "5.3 Implement operational controls and standards",
        "5.4 Support digital forensics",
        "5.5 Manage communication with relevant parties"
    ],
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
    "Official Study Guide",
    "LearnZapp Practice Questions",
    "Pete Zerger YouTube",
    "Mike Chapple LinkedIn Learning",
    "NIST SP 800-145",
    "CCSP CBK Book"
]

MILESTONES = {
    "Domain 1": "Domain 1: Cloud Concepts, Architecture, and Design (17%)",
    "Domain 2": "Domain 2: Cloud Data Security (20%)",
    "Domain 3": "Domain 3: Cloud Platform & Infrastructure Security (17%)",
    "Domain 4": "Domain 4: Cloud Application Security (17%)",
    "Domain 5": "Domain 5: Cloud Security Operations (16%)",
    "Domain 6": "Domain 6: Legal, Risk, and Compliance (13%)"
}

# --- File I/O Functions ---
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Timestamp", "Date", "Domain", "Sub-Objective",
            "Resources Used", "Time Spent (Minutes)", "Notes",
            "Confidence (1-5)", "Status"
        ])
        df.to_csv(DATA_FILE, index=False)
    if not os.path.exists(TEST_LOG_FILE):
        df_test = pd.DataFrame(columns=[
            "Timestamp", "Date", "Domain(s)", "Number of Questions",
            "Score (%)", "Test Duration (Minutes)", "Test Type"
        ])
        df_test.to_csv(TEST_LOG_FILE, index=False)

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

def load_test_data():
    initialize_data_file()
    try:
        return pd.read_csv(TEST_LOG_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=[
            "Timestamp", "Date", "Domain(s)", "Number of Questions",
            "Score (%)", "Test Duration (Minutes)", "Test Type"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def save_test_data(df):
    df.to_csv(TEST_LOG_FILE, index=False)

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

def add_test_entry(entry_date, domains, num_questions, score, duration, test_type):
    df = load_test_data()
    timestamp = datetime.now().strftime(DATE_FORMAT)
    new_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Date": entry_date.strftime("%Y-%m-%d"),
        "Domain(s)": ", ".join(domains),
        "Number of Questions": num_questions,
        "Score (%)": score,
        "Test Duration (Minutes)": duration,
        "Test Type": test_type
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_test_data(df)

# --- Streamlit UI ---
st.set_page_config(page_title="CCSP Study Tracker", layout="wide")
st.title("📘 CCSP Study Tracker with Milestones and Test Logging")

page = st.sidebar.radio("Navigation", ["Add Study Entry", "View Progress Log", "Milestone Progress", "Log Practice Test"])

if page == "Add Study Entry":
    st.header("📝 Add New Study Entry")
    with st.form("entry_form"):
        entry_date = st.date_input("Study Date", value=datetime.today())
        selected_domain = st.selectbox("Domain Studied", ["--Select a Domain--"] + list(CCSP_DOMAINS.keys()))
        sub_objectives = CCSP_DOMAINS.get(selected_domain, [])
        selected_sub = st.selectbox("Sub-Objective", sub_objectives if sub_objectives else ["General"])
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
                final_resources = resources.copy()
                if other_resource:
                    final_resources.append(other_resource.strip())
                add_study_entry(entry_date, selected_domain, selected_sub, final_resources, time_spent, notes, confidence, status)
                st.success("Entry added successfully!")

elif page == "View Progress Log":
    st.header("📊 Study Progress Log")
    df = load_data()
    if df.empty:
        st.info("No entries yet.")
    else:
        st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
        st.subheader("Summary")
        st.metric("Total Study Time (Hours)", f"{df['Time Spent (Minutes)'].sum() / 60:.2f}")
        st.metric("Average Confidence", f"{df['Confidence (1-5)'].mean():.2f} / 5")
        st.bar_chart(df.groupby("Domain")["Time Spent (Minutes)"].sum().sort_values(ascending=False))

elif page == "Milestone Progress":
    st.header("🏁 Milestone Completion Tracker")
    df = load_data()
    if df.empty:
        st.info("No progress data available yet.")
    else:
        completed = {}
        for short_key, full_domain in MILESTONES.items():
            total = len(CCSP_DOMAINS[full_domain])
            filtered = df[(df["Domain"] == full_domain) & (df["Status"] == "Completed")]
            done = filtered["Sub-Objective"].nunique()
            percent = int((done / total) * 100) if total > 0 else 0
            completed[full_domain] = percent
        for domain_name, pct in completed.items():
            st.markdown(f"**{domain_name}**: {pct}% complete")
            st.progress(pct)

elif page == "Log Practice Test":
    st.header("🧠 Log a LearnZapp Custom Test")
    with st.form("test_log_form"):
        test_date = st.date_input("Test Date", value=datetime.today())
        selected_domains = st.multiselect("Domains Covered", options=list(CCSP_DOMAINS.keys()))
        num_questions = st.selectbox("Number of Questions", [5, 10, 25, 50, 100], index=2)
        score = st.slider("Score Achieved (%)", 0, 100, 75)
        test_duration = st.selectbox("Duration (Minutes)", [5, 10, 20, 30, 60], index=4)
        test_type = st.selectbox("Test Type", [
            "Default (Smart Logic)",
            "Questions I answered incorrectly",
            "Questions I have not yet answered",
            "Questions I bookmarked"
        ])

        if st.form_submit_button("Log Test Session"):
            add_test_entry(test_date, selected_domains, num_questions, score, test_duration, test_type)
            st.success("✅ Practice test logged successfully!")

    st.subheader("📈 Previous Test Sessions")
    df_test = load_test_data()
    if df_test.empty:
        st.info("No test logs found.")
    else:
        st.dataframe(df_test.sort_values(by="Timestamp", ascending=False), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("Built to support your CCSP study journey with priority tracking and milestone logic 🚀")
