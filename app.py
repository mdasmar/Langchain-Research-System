
import streamlit as st
from datetime import datetime
from src.pipelines.pipeline import research_pipeline


# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------
# Custom styling
# ----------------------------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 1.8rem;
            border-radius: 16px;
            background: linear-gradient(120deg, #172554, #3730a3);
            color: white;
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            color: white;
            margin-bottom: 0.5rem;
        }

        .hero p {
            color: #e0e7ff;
            margin-bottom: 0;
            font-size: 1.05rem;
        }

        div[data-testid="stMetric"] {
            background: var(--secondary-background-color);
            padding: 1rem;
            border-radius: 12px;
        }

        div.stButton > button {
            border-radius: 10px;
            min-height: 2.8rem;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Session state
# ----------------------------
if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

if "research_history" not in st.session_state:
    st.session_state.research_history = []


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("🔬 Research Assistant")
    st.caption("Powered by LangChain and Azure OpenAI")

    st.divider()

    st.subheader("Research workflow")

    st.markdown(
        """
        1. 🔎 **Search Agent** — finds relevant information.
        2. 📄 **Reader Agent** — extracts useful web content.
        3. ✍️ **Writer Chain** — creates a structured report.
        4. 🧐 **Critic Chain** — evaluates report quality.
        """
    )

    st.divider()

    st.subheader("Configuration")
    st.info(
        "The application uses your existing backend and "
        "environment variables. Configure Azure OpenAI and "
        "Tavily credentials in your existing .env file."
    )

    if st.button("🗑️ Clear current results", use_container_width=True):
        st.session_state.research_result = None
        st.session_state.research_topic = ""
        st.rerun()

    st.caption("AI-generated research should be verified against original sources.")


# ----------------------------
# Main header
# ----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>AI Research Assistant</h1>
        <p>
            Research any topic using autonomous AI agents.
            Explore sources, generate reports, and evaluate quality.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Research input
# ----------------------------
st.subheader("What would you like to research?")

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder=(
            "Example: How generative AI is transforming "
            "healthcare, education, and business"
        ),
        height=110,
        help="Enter a clear topic to help the agents find relevant information.",
    )

    submitted = st.form_submit_button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True,
    )


# ----------------------------
# Execute existing pipeline
# ----------------------------
if submitted:
    topic = topic.strip()

    if not topic:
        st.warning("Please enter a research topic before continuing.")
    else:
        try:
            with st.status(
                "Research agents are working...",
                expanded=True,
            ) as status:
                st.write("🔎 Searching the web and collecting results...")
                st.write("📄 Reading relevant web content...")
                st.write("✍️ Generating the research report...")
                st.write("🧐 Evaluating report quality...")

                # Call your existing backend.
                result = research_pipeline(topic)

                if not isinstance(result, dict):
                    raise TypeError(
                        "research_pipeline() must return a dictionary."
                    )

                required_keys = [
                    "search_result",
                    "scrape_content",
                    "report",
                    "feedback",
                ]

                missing = [
                    key for key in required_keys
                    if key not in result
                ]

                if missing:
                    raise KeyError(
                        f"Pipeline result is missing: {', '.join(missing)}"
                    )

                st.session_state.research_result = result
                st.session_state.research_topic = topic

                st.session_state.research_history.insert(
                    0,
                    {
                        "topic": topic,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    },
                )

                status.update(
                    label="Research completed successfully!",
                    state="complete",
                    expanded=False,
                )

        except Exception as exc:
            st.error(
                "The research pipeline failed. Check your API credentials, "
                "model configuration, internet connection, and terminal logs."
            )
            st.exception(exc)


# ----------------------------
# Display research results
# ----------------------------
result = st.session_state.research_result

if result:
    current_topic = st.session_state.research_topic

    st.divider()

    st.subheader("📊 Research Overview")
    st.markdown(f"**Topic:** {current_topic}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Workflow", "Completed")
    col2.metric("Search Results", "Available")
    col3.metric("Web Content", "Available")
    col4.metric("Report", "Generated")

    # Result tabs
    search_tab, reader_tab, report_tab, critic_tab = st.tabs(
        [
            "🔎 Search Results",
            "📄 Extracted Content",
            "📝 Final Report",
            "🧐 Critic Review",
        ]
    )

    with search_tab:
        st.subheader("Search Agent Output")
        st.markdown(
            result["search_result"] or "No search results were returned."
        )

        st.download_button(
            "⬇️ Download search results",
            data=result["search_result"] or "",
            file_name="research_search_results.txt",
            mime="text/plain",
            key="download_search",
        )

    with reader_tab:
        st.subheader("Reader Agent Output")
        st.markdown(
            result["scrape_content"]
            or "No extracted content was returned."
        )

        st.download_button(
            "⬇️ Download extracted content",
            data=result["scrape_content"] or "",
            file_name="extracted_research.txt",
            mime="text/plain",
            key="download_reader",
        )

    with report_tab:
        st.subheader("Research Report")

        report = result["report"] or "No report was generated."

        st.markdown(report)

        st.download_button(
            "⬇️ Download report (.md)",
            data=f"# Research Report\n\nTopic: {current_topic}\n\n{report}",
            file_name="research_report.md",
            mime="text/markdown",
            type="primary",
            key="download_report",
        )

    with critic_tab:
        st.subheader("Critic Agent Evaluation")
        st.markdown(
            result["feedback"] or "No critic feedback was returned."
        )

        st.download_button(
            "⬇️ Download critic feedback",
            data=result["feedback"] or "",
            file_name="critic_feedback.txt",
            mime="text/plain",
            key="download_critic",
        )

else:
    st.info(
        "👋 Enter a research topic above and click **Start Research** "
        "to generate your first report."
    )

    st.markdown("### What you can do")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔎 Discover")
        st.write("Collect relevant information from web search.")

    with col2:
        st.markdown("#### 📝 Generate")
        st.write("Produce a structured research report.")

    with col3:
        st.markdown("#### 🧐 Evaluate")
        st.write("Review the report with your critic chain.")


# ----------------------------
# Recent research history
# ----------------------------
if st.session_state.research_history:
    with st.expander("🕘 Recent research topics"):
        for item in st.session_state.research_history[:10]:
            st.markdown(
                f"- **{item['topic']}** — {item['time']}"
            )
