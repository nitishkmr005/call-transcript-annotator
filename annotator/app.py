import streamlit as st
import pandas as pd
import json

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
        if message.startswith("Agent:"):
            st.markdown(
                f'<div class="timestamp">10:01</div>' +  # Add actual timestamp logic here
                f'<div class="agent-bubble"><strong>Agent (10:01):</strong> {message.split(":", 1)[1].strip()}</div>',
                unsafe_allow_html=True
            )
        elif message.startswith("Customer:"):
            st.markdown(
                f'<div class="timestamp" style="text-align: right;">10:02</div>' +  # Add actual timestamp logic here
                f'<div class="customer-bubble"><strong>Customer (10:02):</strong> {message.split(":", 1)[1].strip()}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

def save_annotations(df, output_file="annotations.json"):
    """Save annotations to JSON file"""
    annotations = []
    for _, row in df.iterrows():
        try:
            annotation_data = {
                "interaction_id": row["interaction_id"],
                "annotator": row["annotator"],
                "validation_data": json.loads(row["llm_output"])
            }
            annotations.append(annotation_data)
        except:
            continue
    
    with open(output_file, 'w') as f:
        json.dump(annotations, f, indent=2)

def load_annotations(file_path="annotations.json"):
    """Load annotations from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def format_validation_data(validation_data):
    """Format validation data for DataFrame display"""
    if not isinstance(validation_data, dict) or 'validation' not in validation_data:
        return {}
    
    flat_data = {}
    
    def flatten_dict(d, prefix=''):
        for key, value in d.items():
            if isinstance(value, dict):
                if 'is_correct' in value:
                    flat_data[f"{prefix}{key}_value"] = value['value']
                    flat_data[f"{prefix}{key}_status"] = '✅' if value['is_correct'] else '❌'
                    if not value['is_correct'] and value['remark']:
                        flat_data[f"{prefix}{key}_remark"] = value['remark']
                else:
                    flatten_dict(value, f"{prefix}{key}_")
    
    flatten_dict(validation_data['validation'])
    return flat_data

# Main app logic
def main():
    st.title("📞 Call Transcript Annotation Tool")
    add_custom_css()

    # Create tabs with only two options
    tabs = st.tabs(["📝 Transcript & Annotation", "📊 View Annotations"])
    
    with tabs[0]:
        # Sample Data
        data = [
            {
                "interaction_id": "INT001",
                "annotator": "Alice",
                "conversations": "Agent: Hello! Thank you for calling. How may I help you today?\nCustomer: Hi, I'm having issues with my account login.\nAgent: I understand. Can you please provide your account number?\nCustomer: Yes, it's 12345678.",
                "llm_output": json.dumps({
                    "call_details": {
                        "call_id": "12345",
                        "call_date": "2024-12-13",
                        "call_type": "Initial Consultation",
                    },
                    "client_profile": {
                        "client_age": 18,
                        "current_401k_balance": 0.0,
                        "years_to_retirement": 0
                    },
                    "retirement_goals": [
                        "retire early",
                        "retire in 10 years",
                        "retire in 20 years"
                    ]
                })
            },
            {
                "interaction_id": "INT002",
                "annotator": "Bob",
                "conversations": "Agent: Hello! How can I assist you today?\nCustomer: I'm interested in upgrading my plan.\nAgent: Sure, let me provide you with the available options.",
                "llm_output": json.dumps({
                    "call_details": {
                        "call_id": "12346",
                        "call_date": "2024-12-14",
                        "call_type": "Plan Upgrade",
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

        # ---------------------
        # STEP 1: FILTERS
        # ---------------------
        annotators = sorted(df['annotator'].unique())
        selected_annotator = st.selectbox("Select Annotator", annotators)

        # Filter DataFrame by selected annotator
        filtered_df = df[df['annotator'] == selected_annotator]
        interaction_ids = sorted(filtered_df['interaction_id'].unique())
        selected_interaction_id = st.selectbox("Select Interaction ID", interaction_ids)

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

                updated_output = {}
                
                # Render fields in a cleaner layout
                for key, value in llm_output_data.items():
                    with st.container():
                        updated_output[key] = render_field(key, value)

                submitted = st.form_submit_button("Submit Annotation")
                
                if submitted:
                    row_index = row_df.name
                    validation_output = {
                        "data": llm_output_data,
                        "validation": updated_output
                    }
                    
                    df.at[row_index, 'llm_output'] = json.dumps(validation_output, indent=2)
                    
                    # Save to JSON instead of Parquet
                    save_annotations(df)
                    st.success("Annotations saved successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("View All Annotations")
        
        # Load annotations
        annotations = load_annotations()
        if annotations:
            interaction_ids = [annotation["interaction_id"] for annotation in annotations]
            selected_interaction_id = st.selectbox("Select Interaction ID", interaction_ids)
            
            # Display the selected annotation as JSON
            selected_annotation = next((annotation for annotation in annotations if annotation["interaction_id"] == selected_interaction_id), None)
            if selected_annotation:
                st.json(selected_annotation)
        else:
            st.info("No annotations found.")

def render_field(key, value, parent_key=""):
    """Enhanced render_field function with validation controls"""
    field_id = f"{parent_key}_{key}".strip('_')
    
    if isinstance(value, (str, int, float)):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                input_value = st.text_input(f"{key.capitalize()}", value, key=f"input_{field_id}")
            with col2:
                is_correct = st.radio(
                    "Correct?",
                    ["Yes", "No"],
                    horizontal=True,
                    key=f"radio_{field_id}",
                    label_visibility="collapsed"
                )
            
            remark = ""
            if is_correct == "No":
                remark = st.text_area(
                    "Remark",
                    key=f"remark_{field_id}",
                    placeholder="Enter your remark here...",
                    height=100
                )
            
            return {
                "value": input_value,
                "is_correct": is_correct == "Yes",
                "remark": remark
            }
    
    elif isinstance(value, dict):
        st.markdown(f'<div class="section-header">{key.capitalize()}</div>', unsafe_allow_html=True)
        updated_dict = {}
        for sub_key, sub_value in value.items():
            with st.container():
                updated_dict[sub_key] = render_field(sub_key, sub_value, f"{parent_key}_{key}")
        return updated_dict
    
    elif isinstance(value, list):
        st.markdown(f'<div class="section-header">{key.capitalize()}</div>', unsafe_allow_html=True)
        updated_list = []
        for i, item in enumerate(value):
            with st.container():
                updated_list.append(render_field(f"{key}_{i}", item, parent_key))
        return updated_list
    
    else:
        return str(value)

if __name__ == "__main__":
    main()