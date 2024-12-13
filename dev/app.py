import streamlit as st
import pandas as pd

# Custom CSS for better styling
def local_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 20px;
        }
        
        /* Header styling */
        .main-header {
            color: #1E3D59;
            text-align: center;
            padding: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid #E8F0FE;
        }
        
        /* Transcript message styling */
        .message-container {
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            color: black !important;
        }
        
        .agent-message {
            background-color: #E3F2FD;
            border-left: 5px solid #2196F3;
            color: black !important;
        }
        
        .customer-message {
            background-color: #F5F5F5;
            border-left: 5px solid #9E9E9E;
            color: black !important;
        }
        
        /* Make sure all text elements inside messages are black */
        .message-container b,
        .message-container small,
        .message-container span {
            color: black !important;
        }
        
        /* Form styling */
        .stForm {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stButton>button {
            background-color: #2196F3;
            color: white;
            width: 100%;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            margin-top: 20px;
        }
        
        .stButton>button:hover {
            background-color: #1976D2;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border-radius: 5px;
        }
        
        /* Success message styling */
        .stSuccess {
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
        
        /* Dataframe styling */
        .dataframe {
            border: none !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Section headers */
        .section-header {
            color: #1E3D59;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #E8F0FE;
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
                    language = st.selectbox("🌐 Language", 
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
