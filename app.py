import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Custom CSS for better styling
def local_css():
    st.markdown("""
        <style>
        /* Modern Theme Variables */
        :root {
            /* Base colors */
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            
            /* Accent colors */
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-teal: #14b8a6;
            --accent-pink: #ec4899;
            
            /* Gradients */
            --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%);
            --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
            
            /* Shadows */
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        /* Global Styles */
        .stApp {
            background: var(--bg-primary);
        }

        /* Headers */
        .main-header {
            background: var(--gradient-blue);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 2rem !important;
            text-align: center;
        }

        .section-header {
            color: var(--text-primary) !important;
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            margin-bottom: 1.5rem !important;
        }

        /* Message Containers */
        .message-container {
            margin: 15px 0;
            padding: 20px 25px;
            border-radius: 16px;
            box-shadow: var(--shadow-md);
            font-size: 1rem;
            line-height: 1.6;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 92%;
        }

        .agent-message {
            background: linear-gradient(145deg, rgba(59, 130, 246, 0.15), rgba(45, 212, 191, 0.1));
            border-left: 4px solid var(--accent-blue);
            margin-right: 8%;
        }

        .customer-message {
            background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.1));
            border-left: 4px solid var(--accent-purple);
            margin-left: 8%;
        }

        .message-container:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }

        /* Form Styling */
        .stForm {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
        }

        /* Input Fields */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            transition: all 0.2s ease;
        }

        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }

        /* Select Boxes */
        .stSelectbox>div>div>div {
            background: var(--bg-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
        }

        /* Sliders */
        .stSlider>div>div>div {
            background: var(--gradient-blue) !important;
        }

        .stSlider>div>div>div>div {
            background: white !important;
            border: 2px solid var(--accent-blue) !important;
        }

        /* Buttons */
        .stButton>button {
            background: var(--gradient-blue) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-secondary) !important;
            border-radius: 12px !important;
            padding: 8px !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: var(--text-secondary) !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: var(--gradient-blue) !important;
            color: white !important;
        }

        /* Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.1) !important;
            margin: 2rem 0 !important;
        }

        /* Success/Info Messages */
        .stSuccess, .stInfo {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* DataFrames */
        .dataframe {
            background: var(--bg-secondary) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Checkbox */
        .stCheckbox {
            color: var(--text-secondary) !important;
        }

        .stCheckbox>div>div>div>div {
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* LLM Evaluation Styles */
        .subsection-header {
            color: var(--text-primary) !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 1px solid var(--border-color);
        }
        
        /* Metric cards */
        .metric-card {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid var(--border-color);
        }
        
        /* Comparison indicators */
        .match-indicator {
            font-size: 1.2rem;
            margin-left: 0.5rem;
        }
        
        /* Metrics expander styling */
        .metrics-expander {
            background: linear-gradient(145deg, var(--bg-secondary), var(--bg-primary));
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin: 0.5rem 0
        </style>
    """, unsafe_allow_html=True)

def load_annotations_from_parquet():
    """Load annotations from parquet file if it exists, otherwise return empty list"""
    file_path = Path("annotations.parquet")
    if file_path.exists():
        return pd.read_parquet(file_path).to_dict('records')
    return []

def save_annotations_to_parquet(annotations):
    """Save annotations to parquet file, appending to existing data"""
    file_path = Path("annotations.parquet")
    new_df = pd.DataFrame(annotations)
    
    if file_path.exists():
        existing_df = pd.read_parquet(file_path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    combined_df.to_parquet(file_path, index=False)

def load_dummy_llm_data():
    """Load dummy LLM annotations for testing - matching human annotation structure"""
    dummy_data = {
        "Call Info": {
            "Call ID": "CALL_001",
            "Advisor": "John Smith",
            "Date": "2024-03-20",
            "Duration": "30 minutes",
            "Type": "Retirement Planning",
            "Client ID": "C12345"
        },
        "Client Profile": {
            "Age": 45,
            "Risk Tolerance": "Moderate",
            "Current Balance": 250000,
            "Years to Retirement": 20
        },
        "Retirement Goals": {
            "Goals List": ["Travel Plans", "Healthcare Coverage", "Legacy Planning"],
            "Monthly Income Target": 5000,
            "Location": "Different State",
            "Lifestyle": "Comfortable"
        },
        "Investment Allocation": {
            "Stocks": {"percentage": 60, "amount": 150000},
            "Bonds": {"percentage": 30, "amount": 75000},
            "Cash": {"percentage": 10, "amount": 25000},
            "Real Estate": {"percentage": 0, "amount": 0},
            "Other": {"percentage": 0, "amount": 0}
        },
        "Interaction Summary": {
            "Topics": ["Contribution Rates", "Investment Options", "Risk Management"],
            "Recommendations": "Increase contribution rate to maximize employer match",
            "Action Items": ["Increase Contributions", "Review Investment Mix"]
        },
        "Follow-up": {
            "Required": True,
            "Date": "2024-04-20",
            "Priority": "High",
            "Type": "Portfolio Review"
        },
        "Notes": {
            "Special Considerations": "Client interested in ESG investments",
            "Compliance Notes": "All disclosures provided"
        }
    }
    return dummy_data

def main():
    st.set_page_config(layout="wide", page_title="Call Transcript Annotation", page_icon="📞")
    local_css()
    
    # Initialize session state from parquet file
    if 'annotations' not in st.session_state:
        st.session_state.annotations = load_annotations_from_parquet()

    # Sample transcript data
    transcript = [
        {"speaker": "Agent", "text": "Hello! Thank you for calling. How may I help you today?", "time": "10:01"},
        {"speaker": "Customer", "text": "Hi, I'm having issues with my account login.", "time": "10:02"},
        {"speaker": "Agent", "text": "I understand. Can you please provide your account number?", "time": "10:02"},
        {"speaker": "Customer", "text": "Yes, it's 12345678.", "time": "10:03"}
    ]

    st.markdown('<h1 class="main-header">📞 Call Transcript Annotation Tool</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📝 Transcript & Annotation", "📊 View Annotations", "🤖 LLM Evaluation"])
    
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
            st.markdown('<h3 class="section-header">401k Planning Call Annotation</h3>', unsafe_allow_html=True)
            
            with st.form("annotation_form", clear_on_submit=True):
                # Basic Call Information
                with st.expander("📞 Basic Call Information", expanded=True):
                    col3, col4 = st.columns(2)
                    with col3:
                        call_id = st.text_input("Call ID")
                        agent_name = st.text_input("Financial Advisor Name")
                        call_duration = st.text_input("Call Duration")
                    with col4:
                        call_date = st.date_input("Call Date")
                        customer_id = st.text_input("Client ID")
                        call_type = st.selectbox("Call Type", 
                            ["Initial Consultation", "Portfolio Review", "Retirement Planning", "Investment Adjustment", "General Inquiry"])

                # Client Profile
                with st.expander("👤 Client Profile", expanded=True):
                    col5, col6 = st.columns(2)
                    with col5:
                        age = st.number_input("Client Age", min_value=18, max_value=100)
                        risk_tolerance = st.select_slider("Risk Tolerance", 
                            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"])
                    with col6:
                        current_401k_balance = st.number_input("Current 401k Balance ($)")
                        years_to_retirement = st.number_input("Years to Retirement", min_value=0, max_value=50)

                # Retirement Goals
                with st.expander("🎯 Retirement Goals", expanded=True):
                    retirement_goals = st.multiselect("Selected Retirement Goals",
                        ["Early Retirement", "Travel Plans", "Healthcare Coverage", 
                         "Legacy Planning", "Debt-Free Retirement", "Part-time Work",
                         "Relocate/Downsize", "Start Business", "Education Funding",
                         "Charitable Giving"])
                    
                    monthly_retirement_income = st.number_input("Desired Monthly Retirement Income ($)")
                    
                    col7, col8 = st.columns(2)
                    with col7:
                        retirement_location = st.selectbox("Planned Retirement Location",
                            ["Current Location", "Different State", "International", "Undecided"])
                    with col8:
                        lifestyle_expectation = st.select_slider("Lifestyle Expectation",
                            options=["Basic", "Comfortable", "Luxurious"])

                # Investment Breakdown
                with st.expander("💰 Investment Allocation", expanded=True):
                    st.markdown("##### Current Portfolio Allocation")
                    
                    investment_types = ["Stocks", "Bonds", "Cash", "Real Estate", "Other"]
                    investment_data = {}
                    
                    for i in range(0, len(investment_types), 2):
                        col9, col10 = st.columns(2)
                        with col9:
                            if i < len(investment_types):
                                investment_data[investment_types[i]] = {
                                    "percentage": st.slider(f"{investment_types[i]} (%)", 0, 100, 0),
                                    "amount": st.number_input(f"{investment_types[i]} Amount ($)", min_value=0.0)
                                }
                        with col10:
                            if i + 1 < len(investment_types):
                                investment_data[investment_types[i + 1]] = {
                                    "percentage": st.slider(f"{investment_types[i + 1]} (%)", 0, 100, 0),
                                    "amount": st.number_input(f"{investment_types[i + 1]} Amount ($)", min_value=0.0)
                                }

                # Interaction Summary
                with st.expander("📝 Interaction Summary", expanded=True):
                    key_topics_discussed = st.multiselect("Key Topics Discussed",
                        ["Contribution Rates", "Investment Options", "Risk Management",
                         "Tax Implications", "Employer Match", "Fund Selection",
                         "Rebalancing Strategy", "Distribution Planning", "Rollover Options",
                         "Social Security Integration"])
                    
                    recommendations = st.text_area("Advisor Recommendations")
                    
                    action_items = st.multiselect("Action Items",
                        ["Increase Contributions", "Rebalance Portfolio", "Update Beneficiaries",
                         "Review Investment Mix", "Schedule Follow-up", "Document Updates",
                         "Risk Assessment", "Create Financial Plan"])

                # Follow-up Details
                with st.expander("📅 Follow-up Details", expanded=True):
                    col11, col12 = st.columns(2)
                    with col11:
                        follow_up_needed = st.checkbox("Follow-up Required")
                        follow_up_date = st.date_input("Follow-up Date") if follow_up_needed else None
                    with col12:
                        priority_level = st.select_slider("Priority Level",
                            options=["Low", "Medium", "High"])
                        follow_up_type = st.selectbox("Follow-up Type",
                            ["Portfolio Review", "Document Collection", "Plan Update",
                             "Investment Changes", "General Check-in"]) if follow_up_needed else None

                # Additional Notes
                with st.expander("📌 Additional Notes", expanded=True):
                    special_considerations = st.text_area("Special Considerations")
                    compliance_notes = st.text_area("Compliance Notes")
                    
                submit_button = st.form_submit_button("Submit Annotation")
                
                if submit_button:
                    attributes = {
                        "Call Info": {
                            "Call ID": call_id,
                            "Advisor": agent_name,
                            "Date": call_date,
                            "Duration": call_duration,
                            "Type": call_type,
                            "Client ID": customer_id
                        },
                        "Client Profile": {
                            "Age": age,
                            "Risk Tolerance": risk_tolerance,
                            "Current Balance": current_401k_balance,
                            "Years to Retirement": years_to_retirement
                        },
                        "Retirement Goals": {
                            "Goals List": retirement_goals,
                            "Monthly Income Target": monthly_retirement_income,
                            "Location": retirement_location,
                            "Lifestyle": lifestyle_expectation
                        },
                        "Investment Allocation": investment_data,
                        "Interaction Summary": {
                            "Topics": key_topics_discussed,
                            "Recommendations": recommendations,
                            "Action Items": action_items
                        },
                        "Follow-up": {
                            "Required": follow_up_needed,
                            "Date": follow_up_date,
                            "Priority": priority_level,
                            "Type": follow_up_type
                        },
                        "Notes": {
                            "Special Considerations": special_considerations,
                            "Compliance Notes": compliance_notes
                        }
                    }
                    st.session_state.annotations.append(attributes)
                    
                    # Save to parquet file
                    try:
                        save_annotations_to_parquet([attributes])
                        st.success("✅ 401k Planning Call Annotation Submitted Successfully and Saved to Database!")
                    except Exception as e:
                        st.error(f"Error saving annotation: {str(e)}")

    with tabs[1]:
        st.markdown('<h3 class="section-header">Submitted Annotations</h3>', unsafe_allow_html=True)
        if st.session_state.annotations:
            df = pd.DataFrame(st.session_state.annotations)
            
            # Add download buttons
            col1, col2 = st.columns(2)
            with col1:
                # Download as Parquet
                if st.button("📥 Download as Parquet"):
                    temp_file = "temp_annotations.parquet"
                    df.to_parquet(temp_file, index=False)
                    with open(temp_file, 'rb') as f:
                        st.download_button(
                            "Click to Download",
                            f,
                            file_name="annotations.parquet",
                            mime="application/octet-stream"
                        )
                    os.remove(temp_file)
            
            with col2:
                # Download as CSV
                if st.button("📥 Download as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Click to Download",
                        csv,
                        file_name="annotations.csv",
                        mime="text/csv"
                    )
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📝 No annotations submitted yet.")

    with tabs[2]:
        st.markdown('<h3 class="section-header">LLM Evaluation Comparison</h3>', unsafe_allow_html=True)
        
        if st.session_state.annotations:
            # Create three columns for comparison
            col_human, col_llm, col_metrics = st.columns(3)
            
            with col_human:
                st.markdown('<h4 class="subsection-header">Human Annotation</h4>', unsafe_allow_html=True)
                human_annotation = st.session_state.annotations[-1]  # Get latest annotation
                
                # Display human annotations in an organized way
                for section, data in human_annotation.items():
                    with st.expander(f"📋 {section}", expanded=True):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                st.write(f"**{key}:** {value}")
                        else:
                            st.write(f"**{section}:** {data}")
            
            with col_llm:
                st.markdown('<h4 class="subsection-header">LLM Generated Annotation</h4>', unsafe_allow_html=True)
                llm_annotation = load_dummy_llm_data()
                
                # Display LLM annotations
                for section, data in llm_annotation.items():
                    with st.expander(f"🤖 {section}", expanded=True):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                st.write(f"**{key}:** {value}")
                        else:
                            st.write(f"**{section}:** {data}")
            
            with col_metrics:
                st.markdown('<h4 class="subsection-header">Comparison Metrics</h4>', unsafe_allow_html=True)
                
                def calculate_metrics(human_value, llm_value):
                    if isinstance(human_value, (str, int, float)):
                        match = human_value == llm_value
                        return {
                            "precision": 1.0 if match else 0.0,
                            "recall": 1.0 if match else 0.0,
                            "match": "✅" if match else "❌"
                        }
                    elif isinstance(human_value, list):
                        if not human_value or not llm_value:
                            return {"precision": 0.0, "recall": 0.0, "match": "❌"}
                        common = set(human_value) & set(llm_value)
                        precision = len(common) / len(llm_value) if llm_value else 0
                        recall = len(common) / len(human_value) if human_value else 0
                        return {
                            "precision": precision,
                            "recall": recall,
                            "match": "✅" if precision == recall == 1.0 else "⚠���"
                        }
                    return {"precision": 0.0, "recall": 0.0, "match": "❓"}
                
                # Calculate and display metrics for each section
                overall_metrics = {"precision": [], "recall": []}
                
                for section, human_data in human_annotation.items():
                    with st.expander(f"📊 {section} Metrics", expanded=True):
                        if isinstance(human_data, dict):
                            for key, human_value in human_data.items():
                                llm_value = llm_annotation.get(section, {}).get(key)
                                metrics = calculate_metrics(human_value, llm_value)
                                
                                st.write(f"**{key}** {metrics['match']}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Precision", f"{metrics['precision']:.2%}")
                                with col2:
                                    st.metric("Recall", f"{metrics['recall']:.2%}")
                                
                                overall_metrics["precision"].append(metrics["precision"])
                                overall_metrics["recall"].append(metrics["recall"])
                
                # Display overall metrics
                st.markdown("### Overall Performance")
                avg_precision = sum(overall_metrics["precision"]) / len(overall_metrics["precision"])
                avg_recall = sum(overall_metrics["recall"]) / len(overall_metrics["recall"])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average Precision", f"{avg_precision:.2%}")
                with col2:
                    st.metric("Average Recall", f"{avg_recall:.2%}")
        else:
            st.info("📝 No annotations available for comparison.")

if __name__ == "__main__":
    main()
