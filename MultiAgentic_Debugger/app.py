import streamlit as st
from agentic_debugger.orchestrator import debug_code

st.set_page_config("Agentic AI Debugger", "🧠", layout="wide")
st.title("🧠 Agentic AI Debugger")
st.caption("Multi-Agent Python Debugging System")

code = st.text_area(
    "Paste Python code below",
    height=300,
    placeholder="Enter buggy Python code..."
)

if st.button("🚀 Run Debugger"):
    if not code.strip():
        st.warning("Please enter code")
    else:
        with st.spinner("Running Scanner → Fixer → Validator..."):
            result = debug_code(code)

        if result["status"] == "FIXED":
            st.success("✅ Code Fixed Successfully")
        elif result["status"] == "NO_ERRORS":
            st.info("ℹ️ No errors found")
        else:
            st.error("❌ Unable to fix code")

        st.subheader("🔍 Detected Issues")
        for err in result["detected_errors"]:
            st.error(f"{err['type']} | Line {err['line']} | {err['description']}")

        if result["status"] == "FIXED":
            col1, col2 = st.columns(2)
            with col1:
                st.code(code, language="python")
            with col2:
                st.code(result["final_code"], language="python")

            st.subheader("🧠 Explanation")
            st.info(result["fix_attempts"][-1]["explanation"])
