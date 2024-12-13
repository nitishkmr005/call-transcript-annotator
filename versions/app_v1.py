import streamlit as st
import pandas as pd

# Custom CSS for better styling
def local_css():
    st.markdown("""
        <style>
        /* Theme-aware variables */
        :root {
            /* Updated modern dark theme */
            --form-bg: #1a1f2c;
            --input-bg: #2d3748;
            --input-text: #e2e8f0;
            --label-color: #a0aec0;
            
            /* Gradient backgrounds for messages */
            --message-bg-agent: linear-gradient(145deg, rgba(56, 178, 172, 0.15), rgba(49, 151, 149, 0.1));
            --message-bg-customer: linear-gradient(145deg, rgba(116, 66, 182, 0.15), rgba(104, 51, 138, 0.1));
            --message-text: #e2e8f0;
            
            /* New accent colors */
            --accent-primary: #38b2ac;
            --accent-secondary: #805ad5;
            --border-color: rgba(255, 255, 255, 0.1);
        }

        /* Updated message styling */
        .message-container {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            font-size: 1rem;
            line-height: 1.6;
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            max-width: 95%;
        }
        
        .agent-message {
            background: linear-gradient(145deg, rgba(29, 185, 184, 0.12), rgba(25, 167, 206, 0.05));
            border-left: 4px solid #1db9b8;
            margin-right: 5%;
        }
        
        .customer-message {
            background: linear-gradient(145deg, rgba(147, 51, 234, 0.12), rgba(192, 132, 252, 0.05));
            border-left: 4px solid #9333ea;
            margin-left: 5%;
        }
        
        .message-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        }

        /* Message text styling */
        .message-container b {
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.9;
        }

        .message-container small {
            font-size: 0.8rem;
            opacity: 0.7;
            margin-left: 8px;
        }

        .message-container br {
            margin-bottom: 8px;
            display: block;
            content: "";
        }

        /* Form input styling */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input,
        .stDateInput>div>div>input {
            background-color: var(--input-bg) !important;
            color: var(--input-text) !important;
            font-size: 1rem !important;
            font-weight: 400 !important;
        }

        /* Labels */
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stNumberInput label,
        .stDateInput label,
        .stSlider label {
            color: var(--label-color) !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin-bottom: 5px !important;
        }

        /* Selectbox */
        .stSelectbox>div>div>div {
            background-color: var(--input-bg) !important;
            color: var(--input-text) !important;
            font-size: 1rem !important;
        }

        /* Slider values */
        .stSlider [data-baseweb="slider"] div {
            color: var(--input-text) !important;
            font-size: 1rem !important;
        }

        /* Headers */
        .main-header, .section-header {
            color: var(--label-color) !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
        }

        /* Checkbox text */
        .stCheckbox label span {
            color: var(--label-color) !important;
            font-size: 1rem !important;
        }

        /* Submit button */
        .stButton>button {
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        /* Tab labels */
        .stTabs [data-baseweb="tab"] {
            color: var(--label-color) !important;
            font-size: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Call Transcript Annotation", page_icon="📞")
    local_css()
    
    # Initialize session state
    if 'annotations' not in st.session_state:
        st.session_state.annotations = []

    # Sample transcript data
    transcript = [
        {"speaker": "Agent", "text": "Hello! Thank you for calling. How may I help you today?", "time": "10:01"},
        {"speaker": "Customer", "text": "Hi, I'm having issues with my account login.", "time": "10:02"},
        {"speaker": "Agent", "text": "I understand. Can you please provide your account number?", "time": "10:02"},
        {"speaker": "Customer", "text": "Yes, it's 12345678.", "time": "10:03"}
    ]

    st.markdown('<h1 class="main-header">📞 Call Transcript Annotation Tool</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📝 Transcript & Annotation", "📊 View Annotations"])
    
    with tabs[0]:
        col1, col2 = st.columns([0.6, 0.4])
        
        with col1:
            st.markdown('<h3 class="section-header">Call Transcript</h3>', unsafe_allow_html=True)
            for entry in transcript:
                if entry["speaker"] == "Agent":
                    st.markdown(
                        f'<div class="message-container agent-message">'
                        f'<b>{entry["speaker"]}</b> <small>({entry["time"]})</small><br>'
                        f'{entry["text"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="message-container customer-message">'
                        f'<b>{entry["speaker"]}</b> <small>({entry["time"]})</small><br>'
                        f'{entry["text"]}</div>',
                        unsafe_allow_html=True
                    )

        with col2:
            st.markdown('<h3 class="section-header">Annotation Form</h3>', unsafe_allow_html=True)
            
            with st.form("annotation_form", clear_on_submit=True):
                col3, col4 = st.columns(2)
                
                with col3:
                    call_id = st.text_input("📞 Call ID")
                    customer_intent = st.text_input("🎯 Customer Intent")
                    agent_name = st.text_input("👤 Agent Name")
                
                with col4:
                    call_date = st.date_input("�� Call Date")
                    call_duration = st.text_input("⏱️ Call Duration")
                    customer_id = st.text_input("🆔 Customer ID")
                
                st.markdown("---")
                
                col5, col6 = st.columns(2)
                
                with col5:
                    issue_category = st.selectbox("🏷️ Issue Category", 
                        ["Technical", "Billing", "Account", "Product", "Other"])
                    resolution_status = st.selectbox("✅ Resolution Status", 
                        ["Resolved", "Pending", "Escalated", "Unresolved"])
                
                with col6:
                    priority_level = st.selectbox("🔥 Priority Level", 
                        ["Low", "Medium", "High"])
                    language = st.selectbox("���� Language", 
                        ["English", "Spanish", "French", "German", "Other"])
                
                st.markdown("---")
                
                col7, col8 = st.columns(2)
                
                with col7:
                    customer_satisfaction = st.slider("😊 Customer Satisfaction", 1, 5, 3)
                    technical_skills = st.slider("💻 Technical Skills", 1, 5, 3)
                
                with col8:
                    communication_skills = st.slider("🗣️ Communication Skills", 1, 5, 3)
                    problem_solving = st.slider("🧩 Problem Solving", 1, 5, 3)
                
                st.markdown("---")
                
                col9, col10 = st.columns(2)
                
                with col9:
                    first_call = st.checkbox("1️⃣ First Call Resolution")
                    follow_up = st.checkbox("📅 Follow-up Required")
                
                with col10:
                    transfer = st.checkbox("↗️ Transfer Required")
                    product_mentioned = st.text_input("🏷️ Product Mentioned")
                
                notes = st.text_area("📝 Additional Notes")
                reviewer = st.text_input("👤 Reviewer Name")
                
                submit_button = st.form_submit_button("Submit Annotation")
                
                if submit_button:
                    attributes = {
                        "Call ID": call_id,
                        "Customer Intent": customer_intent,
                        "Issue Category": issue_category,
                        "Resolution Status": resolution_status,
                        "Customer Satisfaction": customer_satisfaction,
                        "Agent Name": agent_name,
                        "Call Duration": call_duration,
                        "First Call Resolution": first_call,
                        "Follow-up Required": follow_up,
                        "Priority Level": priority_level,
                        "Product Mentioned": product_mentioned,
                        "Customer ID": customer_id,
                        "Call Date": call_date,
                        "Language": language,
                        "Transfer Required": transfer,
                        "Technical Skills": technical_skills,
                        "Communication Skills": communication_skills,
                        "Problem Solving": problem_solving,
                        "Notes": notes,
                        "Reviewer": reviewer
                    }
                    st.session_state.annotations.append(attributes)
                    st.success("✅ Annotation submitted successfully!")

    with tabs[1]:
        st.markdown('<h3 class="section-header">Submitted Annotations</h3>', unsafe_allow_html=True)
        if st.session_state.annotations:
            df = pd.DataFrame(st.session_state.annotations)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📝 No annotations submitted yet.")

if __name__ == "__main__":
    main()
