import streamlit as st
import pandas as pd
import json
import numpy as np

# Set page configuration for wide layout
st.set_page_config(layout="wide", page_title="Call Transcript Annotation Tool")

# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Page Background with gradient */
        .stApp {
            background: linear-gradient(to bottom, #0A192F, #112240);
        }
        
        /* Header Styling */
        .stApp header {
            background: transparent;
            border-bottom: 1px solid rgba(100, 181, 246, 0.2);
        }
        
        /* Title Styling */
        h1 {
            color: #64B5F6;
            font-size: 28px !important;
            font-weight: 600 !important;
            margin-bottom: 30px;
            text-align: center;
            text-shadow: 0 0 10px rgba(100, 181, 246, 0.3);
        }
        
        /* Subheader Styling */
        h2, h3 {
            color: #64B5F6;
            font-weight: 500 !important;
            margin-bottom: 20px;
            border: none !important;
            padding-bottom: 0 !important;
        }
        
        /* Remove any default border/bar styling */
        .stMarkdown h2::after, .stMarkdown h3::after {
            display: none !important;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(26, 41, 66, 0.7);
            padding: 15px 10px;
            border-radius: 15px;
            margin-bottom: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 181, 246, 0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #64B5F6;
            background-color: transparent;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(42, 63, 95, 0.7);
            transform: translateY(-2px);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: rgba(100, 181, 246, 0.2);
            border: 1px solid rgba(100, 181, 246, 0.3);
        }
        
        /* Call Transcript Styles */
        .conversation-container {
            background: rgba(26, 41, 66, 0.7);
            padding: 25px;
            border-radius: 20px;
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid rgba(100, 181, 246, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
        }
        
        .agent-bubble {
            background: linear-gradient(135deg, #1E3A8A, #1E3A9A);
            color: white;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 15px;
            width: fit-content;
            max-width: 80%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .customer-bubble {
            background: linear-gradient(135deg, #2D2D62, #2D2D72);
            color: white;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 15px;
            width: fit-content;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Form Styling */
        .form-container {
            background: rgba(26, 41, 66, 0.8);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(100, 181, 246, 0.2);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .form-container:hover {
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        
        .form-section {
            background: rgba(26, 41, 66, 0.5);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 15px;
            border: 1px solid rgba(100, 181, 246, 0.1);
            transition: all 0.3s ease;
        }
        
        .form-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Input Fields */
        .stTextInput input, .stSelectbox select, .stNumberInput input {
            background: rgba(10, 25, 47, 0.7) !important;
            color: white !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            height: 45px !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
            border-color: #64B5F6 !important;
            box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2) !important;
        }
        
        /* Slider Styling */
        .stSlider {
            padding: 15px 0;
        }
        
        .stSlider .slider-track {
            background-color: rgba(42, 63, 95, 0.7) !important;
            height: 6px !important;
        }
        
        .stSlider .slider-handle {
            background-color: #64B5F6 !important;
            border: 2px solid white !important;
            box-shadow: 0 0 10px rgba(100, 181, 246, 0.3) !important;
        }
        
        /* Submit Button */
        .stButton button {
            background: linear-gradient(135deg, #64B5F6, #2196F3) !important;
            color: white !important;
            border: none !important;
            padding: 12px 30px !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Timestamp Styling */
        .timestamp {
            color: #64B5F6;
            font-size: 12px;
            margin-bottom: 5px;
            opacity: 0.8;
        }
        
        /* Selectbox Styling */
        .stSelectbox > div > div {
            background: rgba(10, 25, 47, 0.7) !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            border-radius: 8px !important;
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(26, 41, 66, 0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(100, 181, 246, 0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(100, 181, 246, 0.5);
        }
        
        /* Remove black highlight */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: transparent !important;
        }
        
        /* Form section styling update */
        .form-section {
            background: rgba(26, 41, 66, 0.5);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 15px;
            border: 1px solid rgba(100, 181, 246, 0.1);
            transition: all 0.3s ease;
        }
        
        /* Section headers */
        .section-header {
            color: #64B5F6;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        /* Input container styling */
        .input-container {
            background: rgba(26, 41, 66, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        /* Clean subheader styling */
        .subheader {
            color: #64B5F6;
            font-size: 1.5em;
            font-weight: 500;
            margin-bottom: 20px;
            padding: 0;
            border: none;
        }
        
        .stRadio [role="radiogroup"] {
            flex-direction: row !important;
            gap: 1rem;
        }
        
        .stRadio [role="radio"] {
            background: rgba(26, 41, 66, 0.7) !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }
        
        .stRadio [role="radio"][data-checked="true"] {
            background: rgba(100, 181, 246, 0.2) !important;
            border-color: #64B5F6 !important;
        }
        
        .stTextArea textarea {
            background: rgba(10, 25, 47, 0.7) !important;
            color: white !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            transition: all 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #64B5F6 !important;
            box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Render the conversation with bubbles
def render_conversation(conversation):
    messages = conversation.split("\n")
    for message in messages:
        if message.startswith("AGENT:"):
            st.markdown(
                f'<div class="agent-bubble"><strong>AGENT:</strong> {message.split(":", 1)[1].strip()}</div>',
                unsafe_allow_html=True
            )
        elif message.startswith("CUSTOMER:"):
            st.markdown(
                f'<div class="customer-bubble"><strong>CUSTOMER:</strong> {message.split(":", 1)[1].strip()}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

def save_annotations(df, output_file="annotations.parquet"):
    """Save annotations to parquet file"""
    try:
        # Ensure last_updated is set
        if 'last_updated' not in df.columns:
            df['last_updated'] = pd.Timestamp.now()
        elif df['last_updated'].isnull().any():
            df.loc[df['last_updated'].isnull(), 'last_updated'] = pd.Timestamp.now()
            
        # Save to parquet
        df.to_parquet(output_file, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving annotations file: {str(e)}")
        return False

def load_annotations(file_path="annotations.parquet"):
    """Load annotations from parquet file"""
    try:
        df = pd.read_parquet(file_path)
        required_columns = ['interaction_id', 'annotator', 'llm_output', 'annotated_output']
        
        # Check if all required columns exist
        if not all(col in df.columns for col in required_columns):
            return pd.DataFrame(columns=required_columns + ['last_updated'])
            
        # Add last_updated column if it doesn't exist
        if 'last_updated' not in df.columns:
            df['last_updated'] = pd.Timestamp.now()
        
        # Sort by last_updated to show most recent annotations first
        return df.sort_values('last_updated', ascending=False)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            'interaction_id', 
            'annotator', 
            'llm_output',
            'annotated_output',
            'last_updated'
        ])

def show_flash_message(message, type="success"):
    """Show a flash message that automatically disappears"""
    styles = {
        "success": """
            <div style="
                position: fixed;
                top: 50px;
                left: 50%;
                transform: translateX(-50%);
                padding: 15px 30px;
                background-color: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                border-radius: 5px;
                color: #00ff00;
                font-size: 16px;
                z-index: 1000;
                animation: fadeOut 3s forwards;
            ">
                ✅ """ + message + """
            </div>
            <style>
                @keyframes fadeOut {
                    0% { opacity: 1; }
                    70% { opacity: 1; }
                    100% { opacity: 0; }
                }
            </style>
        """,
        "error": """
            <div style="
                position: fixed;
                top: 50px;
                left: 50%;
                transform: translateX(-50%);
                padding: 15px 30px;
                background-color: rgba(255, 0, 0, 0.1);
                border: 1px solid #ff0000;
                border-radius: 5px;
                color: #ff0000;
                font-size: 16px;
                z-index: 1000;
                animation: fadeOut 3s forwards;
            ">
                ❌ """ + message + """
            </div>
            <style>
                @keyframes fadeOut {
                    0% { opacity: 1; }
                    70% { opacity: 1; }
                    100% { opacity: 0; }
                }
            </style>
        """
    }
    st.markdown(styles[type], unsafe_allow_html=True)

# Main app logic
def main():
    st.title("📞 Call Transcript Annotation Tool")
    add_custom_css()

    # Always try to load from parquet file
    try:
        df = pd.read_parquet("annotations1.parquet")
    except FileNotFoundError:
        # If file doesn't exist, initialize with sample data
        data = [
            {
                "interaction_id": "INT001",
                "annotator": "Alice",
                "conversations": "AGENT: Hello! Thank you for calling. How may I help you today?\nCUSTOMER: Hi, I'm having issues with my account login.\nAGENT: I understand. Can you please provide your account number?\nCUSTOMER: Yes, it's 12345678.",
                "llm_output": json.dumps({
                    "call_details": {
                        "call_id": "12345Hello! Thank you for calling. How may I help you todaHello! Thank you for calling. How may I help you todaHello! Thank you for calling. How may I help you todaHello! Thank you for calling. How may I help you toda",
                        "call_timestamp":{"call_date": "2024-12-13"},
                        "call_type": "Initial Consultation"
                    },
                    "client_profile": {
                        "client_age": 18,
                        "current_401k_balance": 0.0,
                        "years_to_retirement": np.nan
                        },
                    "retirement_test": [{"retirement_goal_flag": True},{"retirement_goals": ["travel after retirement"]},{"retirement_age": 65}],
                    "retirement_goals": ["travel after retirement"]
                })
            },
            {
                "interaction_id": "INT002",
                "annotator": "Bob",
                "conversations": "AGENT: Hello! How can I assist you today?\nCUSTOMER: I'm interested in upgrading my plan.\nAGENT: Sure, let me provide you with the available options.",
                "llm_output": json.dumps({
                    "call_details": {
                        "call_id": "12346",
                        "call_timestamp":{"call_date": "2024-12-14"},
                        "call_type": "Plan Upgrade"
                    },
                    "client_profile": {
                        "client_age": 35,
                        "current_401k_balance": 50000.0,
                        "years_to_retirement": 30
                    },
                    "retirement_goals": [
                        "retire early",
                        "retire in 10 years",
                        "retire in 20 years"
                    ]
                })
            }
        ]
        df = pd.DataFrame(data)
        # Save initial data
        df.to_parquet("annotations.parquet", index=False)

    # Store in session state only for form handling
    st.session_state.df = df

    if st.session_state.get("show_flash", False):
        show_flash_message(
            st.session_state["flash_message"], 
            st.session_state["flash_type"]
        )
        # Clear the flash message
        st.session_state["show_flash"] = False

    # Move filters to sidebar
    with st.sidebar:
        st.markdown('<div class="subheader">Filter Conversations</div>', unsafe_allow_html=True)
        
        annotators = sorted(df['annotator'].unique())
        selected_annotator = st.selectbox("Select Annotator", annotators)

        # Filter DataFrame by selected annotator
        filtered_df = df[df['annotator'] == selected_annotator]
        interaction_ids = sorted(filtered_df['interaction_id'].unique())
        selected_interaction_id = st.selectbox("Select Interaction ID", interaction_ids)

    # Create tabs with only two options
    tabs = st.tabs(["📝 Transcript & Annotation", "📊 View Annotations"])
    
    with tabs[0]:
        # Retrieve the row based on selected annotator & interaction ID
        row_df = filtered_df[
            (filtered_df['annotator'] == selected_annotator) &
            (filtered_df['interaction_id'] == selected_interaction_id)
        ].iloc[0]

        # ---------------------
        # STEP 2: LEFT & RIGHT LAYOUT
        # ---------------------
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="subheader">Call Transcript</div>', unsafe_allow_html=True)
            render_conversation(row_df['conversations'])

        with col2:
            st.markdown('<div class="subheader">Call Annotation</div>', unsafe_allow_html=True)
            with st.form("annotation_form"):
                try:
                    llm_output_data = json.loads(row_df['llm_output'])
                except json.JSONDecodeError:
                    llm_output_data = {}

                # Dynamically create tabs based on the subsections in llm_output_data
                subsections = list(llm_output_data.keys())
                if not subsections:
                    st.warning("No annotation sections found in the data")
                else:
                    # Create tabs dynamically
                    annotation_tabs = st.tabs([section.replace('_', ' ').title() for section in subsections])
                    
                    # Dictionary to store updates for each section
                    updated_sections = {}
                    
                    # Render each section in its corresponding tab
                    for tab, section in zip(annotation_tabs, subsections):
                        with tab:
                            st.markdown(f'<div class="section-header">{section.replace("_", " ").title()}</div>', 
                                      unsafe_allow_html=True)
                            updated_sections[section] = render_field(section, llm_output_data.get(section, {}), is_subsection=True)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.session_state["form_submitted"] = True
                        try:
                            row_index = row_df.name
                            current_df = pd.read_parquet("annotations.parquet")
                            current_df.at[row_index, 'annotated_output'] = json.dumps(updated_sections, indent=2)
                            current_df.at[row_index, 'last_updated'] = pd.Timestamp.now()
                            current_df.to_parquet("annotations.parquet", index=False)
                            st.session_state.df = current_df
                            st.session_state["show_flash"] = True
                            st.session_state["flash_message"] = "Annotations saved successfully!"
                            st.session_state["flash_type"] = "success"
                            st.rerun()
                        except Exception as e:
                            st.session_state["show_flash"] = True
                            st.session_state["flash_message"] = f"Error saving annotation: {str(e)}"
                            st.session_state["flash_type"] = "error"
                            st.rerun()
                    else:
                        st.session_state["form_submitted"] = False
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("View Submitted Annotations")
        
        # Load annotations
        annotations_df = load_annotations()
        
        if not annotations_df.empty and 'llm_output' in annotations_df.columns and 'annotated_output' in annotations_df.columns:
            # Filter out rows where annotated_output is None or same as llm_output
            annotations_df = annotations_df[
                (annotations_df['annotated_output'].notna()) & 
                (annotations_df['llm_output'] != annotations_df['annotated_output'])
            ]
            
            if not annotations_df.empty:
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    selected_annotator = st.selectbox(
                        "Filter by Annotator",
                        options=['All'] + sorted(annotations_df['annotator'].unique().tolist())
                    )
                with col2:
                    selected_interaction = st.selectbox(
                        "Filter by Interaction ID",
                        options=['All'] + sorted(annotations_df['interaction_id'].unique().tolist())
                    )
                
                # Apply filters
                filtered_df = annotations_df.copy()
                if selected_annotator != 'All':
                    filtered_df = filtered_df[filtered_df['annotator'] == selected_annotator]
                if selected_interaction != 'All':
                    filtered_df = filtered_df[filtered_df['interaction_id'] == selected_interaction]
                
                # Display annotations
                if not filtered_df.empty:
                    for _, row in filtered_df.iterrows():
                        # Format the last_updated timestamp, handling None case
                        last_updated_str = (
                            row['last_updated'].strftime('%Y-%m-%d %H:%M:%S') 
                            if pd.notnull(row['last_updated']) 
                            else "Not updated yet"
                        )
                        
                        with st.expander(
                            f"Interaction: {row['interaction_id']} - "
                            f"Annotator: {row['annotator']} - "
                            f"Last Updated: {last_updated_str}"
                        ):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### Original LLM Output")
                                st.json(json.loads(row['llm_output']))
                            with col2:
                                st.markdown("#### Annotated Output")
                                # Handle None case for annotated_output
                                if pd.notnull(row['annotated_output']):
                                    st.json(json.loads(row['annotated_output']))
                                else:
                                    st.info("No annotations yet")
                else:
                    st.info("No annotations found with selected filters.")
            else:
                st.info("No submitted annotations found.")
        else:
            st.info("No annotations available yet.")

def render_field(key, value, parent_key="", is_subsection=False):
    """Enhanced render_field function with validation controls"""
    field_id = f"{parent_key}_{key}".strip('_')
    
    if isinstance(value, (str, int, float)):
        with st.container():
            # Adjusted column widths: main content takes more space, checkboxes take less
            col1, col2, col3 = st.columns([3, 0.5, 0.5])
            with col1:
                input_value = st.text_area(f"{key.capitalize()}", value, key=f"input_{field_id}")
            with col2:
                is_incorrect = st.checkbox(
                    "❌",
                    key=f"incorrect_{field_id}",
                    label_visibility="collapsed",
                    help="Click to mark as incorrect"
                )
            with col3:
                is_missing = st.checkbox(
                    "⚠️",
                    key=f"missing_{field_id}",
                    label_visibility="collapsed",
                    help="Click to mark as missing"
                )
            
            remark = ""
            if is_incorrect or is_missing:
                remark = st.text_area(
                    "Remark",
                    key=f"remark_{field_id}",
                    placeholder="Enter your remark here...",
                    height=100
                )
            
            return {
                "value": input_value,
                "is_correct": not is_incorrect,
                "is_missing": is_missing,
                "remark": remark
            }
    
    elif isinstance(value, dict):
        if is_subsection:
            # Adjusted header column widths to match
            col1, col2, col3 = st.columns([3, 0.5, 0.5])
            with col2:
                st.markdown('<div style="text-align: left; color: #64B5F6; font-size: 0.8em; margin-bottom: 5px;">Incorrect</div>', 
                          unsafe_allow_html=True)
            with col3:
                st.markdown('<div style="text-align: left; color: #64B5F6; font-size: 0.8em; margin-bottom: 5px;">Missing</div>', 
                          unsafe_allow_html=True)
        
        updated_dict = {}
        for sub_key, sub_value in value.items():
            with st.container():
                updated_dict[sub_key] = render_field(sub_key, sub_value, f"{parent_key}_{key}", False)
        return updated_dict
    
    elif isinstance(value, list):
        if is_subsection:
            col1, col2, col3 = st.columns([3, 0.5, 0.5])
            with col2:
                st.markdown('<div style="text-align: left; color: #64B5F6; font-size: 0.8em; margin-bottom: 5px;">Incorrect</div>', 
                          unsafe_allow_html=True)
            with col3:
                st.markdown('<div style="text-align: left; color: #64B5F6; font-size: 0.8em; margin-bottom: 5px;">Missing</div>', 
                          unsafe_allow_html=True)
        
        # Initialize session state for list items
        if f"list_items_{field_id}" not in st.session_state:
            st.session_state[f"list_items_{field_id}"] = value.copy()
        if f"new_item_{field_id}" not in st.session_state:
            st.session_state[f"new_item_{field_id}"] = ""
        
        # Show list summary
        num_items = len(st.session_state[f"list_items_{field_id}"])
        with st.expander(f"📋 {key.replace('_', ' ').title()} ({num_items} items)", expanded=False):
            updated_list = []
            
            # Display existing items
            for i, item in enumerate(st.session_state[f"list_items_{field_id}"]):
                with st.container():
                    col1, col2, col3 = st.columns([3, 0.5, 0.5])
                    with col1:
                        # Store the input value in session state
                        if f"input_{field_id}_{i}" not in st.session_state:
                            st.session_state[f"input_{field_id}_{i}"] = item
                        
                        input_value = st.text_area(
                            f"Item {i + 1}", 
                            value=st.session_state[f"input_{field_id}_{i}"],
                            key=f"text_{field_id}_{i}",
                            on_change=lambda i=i, v=st.session_state[f"text_{field_id}_{i}"]: 
                                setattr(st.session_state, f"input_{field_id}_{i}", v)
                        )
                        
                        # Update session state with new value
                        st.session_state[f"input_{field_id}_{i}"] = input_value
                    
                    with col2:
                        is_incorrect = st.checkbox(
                            "❌",
                            key=f"incorrect_{field_id}_{i}",
                            label_visibility="collapsed",
                            help="Click to mark as incorrect"
                        )
                    with col3:
                        is_missing = st.checkbox(
                            "⚠️",
                            key=f"missing_{field_id}_{i}",
                            label_visibility="collapsed",
                            help="Click to mark as missing"
                        )
                    
                    remark = ""
                    if is_incorrect or is_missing:
                        remark = st.text_area(
                            "Remark",
                            key=f"remark_{field_id}_{i}",
                            placeholder="Enter your remark here...",
                            height=100
                        )
                    
                    updated_list.append({
                        "value": st.session_state[f"input_{field_id}_{i}"],  # Use session state value
                        "is_correct": not is_incorrect,
                        "is_missing": is_missing,
                        "remark": remark
                    })
            
            # Add new item section
            st.markdown(
                '''
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(100, 181, 246, 0.2);">
                    <div style="color: #64B5F6; font-size: 0.9em; margin-bottom: 10px;">Add New Item</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
            
            # New item input
            new_item = st.text_input(
                "",
                key=f"new_item_input_{field_id}",
                placeholder="Enter new item...",
                label_visibility="collapsed"
            )
            
            # Store new item in session state
            if new_item:
                st.session_state[f"new_item_{field_id}"] = new_item
            
            # Process changes when form is submitted
            if st.session_state.get("form_submitted", False):
                # Update list items with current text area values
                st.session_state[f"list_items_{field_id}"] = [
                    st.session_state[f"input_{field_id}_{i}"]
                    for i in range(len(st.session_state[f"list_items_{field_id}"]))
                ]
                
                # Add new item if exists
                if st.session_state[f"new_item_{field_id}"]:
                    st.session_state[f"list_items_{field_id}"].append(
                        st.session_state[f"new_item_{field_id}"]
                    )
                    st.session_state[f"new_item_{field_id}"] = ""
            
        return updated_list
    
    else:
        return str(value)

if __name__ == "__main__":
    main()