
import streamlit as st
import sys
import os
import re
from datetime import datetime

# =====================================================
# 1. PROJECT IMPORTS
# =====================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from pipelines.pipeline import run_research_pipeline


# =====================================================
# 2. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ResearchAI | AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 3. SESSION STATE
# =====================================================

defaults = {
    "research_data": None,
    "research_topic": "",
    "research_history": [],
    "page": "Dashboard",
    "running": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 4. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Global */

.stApp {
    background-color: #0B1020;
    color: #E5E7EB;
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, 0.9);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #10182B;
    border-right: 1px solid #27344D;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #E5E7EB;
}

/* Typography */

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -1.2px;
}

.hero-title span {
    color: #9B7BFF;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 15px;
    margin-top: 7px;
    margin-bottom: 25px;
}

.section-title {
    color: #F8FAFC;
    font-size: 21px;
    font-weight: 700;
    margin: 20px 0 15px 0;
}

/* Cards */

.metric-card {
    background: linear-gradient(145deg, #18243D, #121B30);
    border: 1px solid #2A3955;
    border-radius: 14px;
    padding: 19px;
    min-height: 110px;
}

.metric-label {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #F8FAFC;
    font-size: 26px;
    font-weight: 750;
    margin-top: 8px;
}

.agent-card {
    background: #151F33;
    border: 1px solid #293750;
    border-radius: 12px;
    padding: 17px;
    min-height: 130px;
}

.agent-icon {
    font-size: 27px;
}

.agent-name {
    color: #F8FAFC;
    font-size: 16px;
    font-weight: 700;
    margin-top: 10px;
}

.agent-description {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 5px;
}

/* Research panels */

.panel {
    background: #151F33;
    border: 1px solid #293750;
    border-radius: 14px;
    padding: 20px;
}

/* Buttons */

.stButton > button {
    border-radius: 9px;
    min-height: 43px;
    font-weight: 650;
    border: 1px solid #344563;
}

/* Text area */

.stTextArea textarea {
    background: #151F33 !important;
    color: #F8FAFC !important;
    border: 1px solid #344563 !important;
    border-radius: 10px !important;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: #111A2D;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    color: #CBD5E1;
}

.stTabs [aria-selected="true"] {
    color: #A78BFA !important;
}

/* Expander */

.streamlit-expanderHeader {
    background: #151F33;
    border-radius: 8px;
}

/* Footer */

.footer {
    color: #64748B;
    text-align: center;
    padding: 30px 0 10px 0;
    font-size: 12px;
}

hr {
    border-color: #27344D;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def display_text(content):
    """Safely display agent output."""

    if isinstance(content, str):
        st.markdown(content)
    else:
        st.write(content)


def get_critic_score(feedback):
    """Extract score from critic feedback."""

    match = re.search(
        r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10",
        str(feedback),
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return None


# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:15px 0;">
            <div style="font-size:40px;">🔬</div>
            <h2 style="color:#F8FAFC;margin-bottom:0;">
                ResearchAI
            </h2>
            <p style="color:#94A3B8;font-size:12px;">
                Intelligent Research Workspace
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### WORKSPACE")

    selected_page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Research Results",
            "Research History"
        ],
        key="page",
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### DISPLAY SETTINGS")

    show_search = st.toggle(
        "Show Search Results",
        value=True
    )

    show_reader = st.toggle(
        "Show Scraped Content",
        value=True
    )

    show_critic = st.toggle(
        "Show Critic Feedback",
        value=True
    )

    st.divider()

    st.markdown("### AI CONFIGURATION")

    st.caption("🧠 Model: NVIDIA Nemotron")

    st.caption("⚡ Provider: OpenRouter")

    st.caption("🔗 Framework: LangChain")

    st.divider()

    st.caption("ResearchAI v1.0")


# =====================================================
# 7. HEADER
# =====================================================

st.markdown(
    '<div class="hero-title">AI Research <span>Assistant</span></div>',
    unsafe_allow_html=True
)


# =====================================================
# 8. DASHBOARD
# =====================================================

if selected_page == "Dashboard":

    # AGENT OVERVIEW

    st.markdown(
        '<div class="section-title">Your AI Research Team</div>',
        unsafe_allow_html=True
    )

    agents = [
        ("🔍", "Search Agent", "Finds relevant web resources"),
        ("📖", "Reader Agent", "Extracts detailed information"),
        ("✍️", "Writer Chain", "Creates research reports"),
        ("🧠", "Critic Chain", "Evaluates report quality")
    ]

    agent_columns = st.columns(4)

    for col, (icon, name, description) in zip(
        agent_columns, agents
    ):

        with col:

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-icon">{icon}</div>
                    <div class="agent-name">{name}</div>
                    <div class="agent-description">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # NEW RESEARCH

    st.markdown(
        '<div class="section-title">🚀 Start a New Research</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        topic = st.text_area(
            "What would you like to research?",
            placeholder=(
                "Example: The impact of AI on the global "
                "job market in 2026..."
            ),
            height=110,
            key="topic_input"
        )

        st.caption(
            "Enter your research topic. Your four AI components "
            "will collaborate to generate a detailed report."
        )

        start_button = st.button(
            "🚀 Start Research",
            type="primary",
            use_container_width=True
        )

    # EXECUTION

    if start_button:

        if not topic.strip():

            st.warning("Please enter a research topic.")

        else:

            st.markdown(
                '<div class="section-title">Agent Execution</div>',
                unsafe_allow_html=True
            )

            progress_bar = st.progress(0)

            status = st.empty()

            tracker = st.container()

            stage_names = [
                ("🔍", "Search Agent", "Discovering relevant sources"),
                ("📖", "Reader Agent", "Extracting detailed information"),
                ("✍️", "Writer Chain", "Preparing research report"),
                ("🧠", "Critic Chain", "Reviewing report quality")
            ]

            def update_progress(step, message):

                progress_bar.progress(
                    min(step * 25, 100)
                )

                status.info(message)

                with tracker:

                    for index, (icon, name, description) in enumerate(
                        stage_names
                    ):

                        if index + 1 < step:
                            symbol = "✅"
                            state = "Completed"

                        elif index + 1 == step and step <= 4:
                            symbol = "🔄"
                            state = "Running"

                        else:
                            symbol = "⏳"
                            state = "Waiting"

                        st.write(
                            f"{symbol} {icon} **{name}** — {state}"
                        )

            try:

                with st.spinner("AI agents are working..."):

                    result = run_research_pipeline(
                        topic,
                        progress_callback=update_progress
                    )

                # Save results

                st.session_state.research_data = result

                st.session_state.research_topic = topic

                st.session_state.research_history.insert(
                    0,
                    {
                        "topic": topic,
                        "date": datetime.now().strftime(
                            "%d %b %Y, %I:%M %p"
                        ),
                        "data": result
                    }
                )

                progress_bar.progress(100)

                status.success(
                    "All four agents completed successfully!"
                )

                with tracker:

                    for icon, name, description in stage_names:
                        st.write(f"✅ {icon} **{name}** — Completed")

                st.success("Your research report is ready!")

                st.balloons()

                st.info(
                    "Open Research Results from the sidebar "
                    "to view your report."
                )

            except Exception as error:

                status.error("Research pipeline failed.")

                st.exception(error)

    # RECENT RESEARCH

    st.markdown(
        '<div class="section-title">📚 Recent Research</div>',
        unsafe_allow_html=True
    )

    if st.session_state.research_history:

        for item in st.session_state.research_history[:3]:

            with st.expander(item["topic"]):

                st.caption(item["date"])

                st.write(
                    str(item["data"]["report"])[:500] + "..."
                )

    else:

        st.info("Your research history will appear here.")


# =====================================================
# 9. RESEARCH RESULTS
# =====================================================

elif selected_page == "Research Results":

    data = st.session_state.research_data

    if data is None:

        st.info(
            "No research available. Start a new research project "
            "from the Dashboard."
        )

    else:

        st.markdown("## 📊 Research Results")

        st.markdown(
            f"**Research Topic:** {st.session_state.research_topic}"
        )

        # TABS

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔍 Search Results",
                "📖 Scraped Content",
                "📝 Final Report",
                "🧠 Critic Review"
            ]
        )

        # SEARCH RESULTS

        with tab1:

            st.markdown("### Search Agent Output")

            if show_search:

                display_text(data["search_results"])

            else:

                st.info("Search results are hidden in settings.")

        # SCRAPED CONTENT

        with tab2:

            st.markdown("### Reader Agent Output")

            if show_reader:

                display_text(data["scraped_content"])

            else:

                st.info("Scraped content is hidden in settings.")

        # FINAL REPORT

        with tab3:

            st.markdown("### Research Report")

            report = str(data["report"])

            display_text(report)

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(
                    "⬇️ Download Markdown",
                    data=report,
                    file_name="research_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with col2:

                st.download_button(
                    "⬇️ Download TXT",
                    data=report,
                    file_name="research_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        # CRITIC REVIEW

        with tab4:

            st.markdown("### Critic Evaluation")

            if show_critic:

                feedback = str(data["feedback"])

                score = get_critic_score(feedback)

                if score is not None:

                    st.metric(
                        "Research Quality Score",
                        f"{score}/10"
                    )

                display_text(feedback)

            else:

                st.info("Critic feedback is hidden in settings.")


# =====================================================
# 10. RESEARCH HISTORY
# =====================================================

elif selected_page == "Research History":

    st.markdown("## 📚 Research History")

    history = st.session_state.research_history

    if not history:

        st.info("No previous research projects found.")

    else:

        for index, item in enumerate(history):

            with st.expander(
                f"📄 {item['topic']} — {item['date']}"
            ):

                st.markdown("### Research Report")

                display_text(item["data"]["report"])

                st.download_button(
                    "⬇️ Download Report",
                    data=str(item["data"]["report"]),
                    file_name=f"research_{index + 1}.md",
                    mime="text/markdown",
                    key=f"download_{index}"
                )

                if st.button(
                    "Load Research",
                    key=f"load_{index}"
                ):

                    st.session_state.research_data = item["data"]

                    st.session_state.research_topic = item["topic"]

                    st.session_state.page = "Research Results"

                    st.rerun()


# =====================================================
# 11. FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        ResearchAI v1.0
        <br>
        Powered by LangChain • OpenRouter • Streamlit
        <br><br>
        Intelligent Research. Better Insights.
    </div>
    """,
    unsafe_allow_html=True
)
