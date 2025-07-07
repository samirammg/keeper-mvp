import streamlit as st
import os
from datetime import datetime

# Feedback text


st.markdown("---")
st.markdown("### 💬 We'd love your feedback on this section")



# Feedback text
    
feedback_text = st.text_area(
    "💬 Your thoughts",
    placeholder="What did you like? What's unclear or missing?"
)

# Importance: Nice-to-have → Must-have
need_labels = ["Must-have", "", "Nice-to-have"]
need_level = st.select_slider(
    "🔧 How important is this section to you?",
    options=[0, 1, 2],
    format_func=lambda x: need_labels[x],
    help="Slide from left to right to rate how necessary this feels"
)

# Differentiation: Generic → Differentiator
unique_labels = ["Differentiator", "", "Generic"]
unique_level = st.select_slider(
    "🎯 How unique or differentiating does this feel?",
    options=[0, 1, 2],
    format_func=lambda x: unique_labels[x],
    help="Slide from left to right to rate how much this stands out"
)

# Submit feedback
if st.button("📩 Submit Feedback"):
    if not feedback_text.strip():
        st.warning("Please write your feedback before submitting.")
    else:
        user = st.session_state.get("user_name", "unknown")
        email = st.session_state.get("user_email", "unknown")
        role = st.session_state.get("user_role", "unknown")
        page_id = __name__.replace("pages.", "").replace(".py", "")

        os.makedirs("feedback", exist_ok=True)
        file_path = f"feedback/{page_id}_feedback.csv"

        with open(file_path, "a") as f:
            f.write(f"{datetime.now()},{user},{email},{role},{page_id},{need_level},{unique_level},{feedback_text.strip()}\n")

        st.success("✅ Thanks! Your feedback was recorded.")

# Close the styled box
st.markdown("</div>", unsafe_allow_html=True)
