import streamlit as st
import pandas as pd
import json
import numpy as np
from gtts import gTTS
import base64
import os
from streamlit_chat import message
import requests
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
        
        /* Sticky Audio Player Container */
        .sticky-audio {
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(26, 41, 66, 0.95);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 181, 246, 0.2);
        }
        
        /* Sticky Tabs */
        .stTabs {
            position: sticky !important;
            top: 0;
            z-index: 998;
            background: transparent;
        }
        
        /* Tab List Styling */
        .stTabs [data-baseweb="tab-list"] {
            position: sticky !important;
            top: 0;
            z-index: 998;
            background: rgba(26, 41, 66, 0.95) !important;
            padding: 15px 10px;
            border-radius: 15px;
            margin-bottom: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 181, 246, 0.1);
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

def text_to_speech(text):
    """Convert text to speech and return the audio player HTML"""
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create a temporary file to store the audio
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)
        
        # Read the audio file and encode it to base64
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()
        
        # Create audio player HTML with custom styling
        audio_player = f"""
            <div style="
                background: rgba(26, 41, 66, 0.7);
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(100, 181, 246, 0.2);
                margin: 10px 0;
            ">
                <audio controls style="width: 100%;">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
            </div>
        """
        return audio_player
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

def render_conversation(conversation):
    """Updated render_conversation function with text-to-speech functionality"""
    # Add text-to-speech button with play icon in a sticky container
    st.markdown(
        """
        <div class="sticky-audio">
            <div style="
                display: flex;
                align-items: center;
                gap: 15px;
            ">
                <div style="
                    background: rgba(100, 181, 246, 0.2);
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z" fill="#64B5F6"/>
                    </svg>
                </div>
                <div>
                    <h4 style="color: #64B5F6; margin: 0; font-size: 16px;">Listen to Full Conversation</h4>
                    <p style="color: #A4B5C6; margin: 5px 0 0 0; font-size: 12px;">Click play to hear the conversation</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Convert conversation text to speech-friendly format
    speech_text = conversation.replace("AGENT:", "Agent says:").replace("CUSTOMER:", "Customer says:")
    audio_player = text_to_speech(speech_text)
    if audio_player:
        st.markdown(audio_player, unsafe_allow_html=True)
    
    # Add custom CSS for audio player styling
    st.markdown(
        """
        <style>
        audio {
            filter: invert(100%) hue-rotate(180deg);
            width: 100%;
            height: 40px;
        }
        audio::-webkit-media-controls-panel {
            background-color: rgba(26, 41, 66, 0.7);
        }
        audio::-webkit-media-controls-play-button {
            background-color: #64B5F6;
            border-radius: 50%;
        }
        audio::-webkit-media-controls-play-button:hover {
            background-color: #82c4f8;
        }
        audio::-webkit-media-controls-current-time-display,
        audio::-webkit-media-controls-time-remaining-display {
            color: #64B5F6;
        }
        audio::-webkit-media-controls-timeline {
            background-color: #64B5F6;
            border-radius: 25px;
            margin-left: 10px;
            margin-right: 10px;
        }
        audio::-webkit-media-controls-volume-slider {
            background-color: #64B5F6;
            border-radius: 25px;
            padding-left: 8px;
            padding-right: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render individual messages
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

def get_annotation_guidelines():
    """Return the annotation guidelines as a string"""
    return """
    Annotation Guidelines for Call Transcript Analysis:

    General Principles:
    - Accuracy First: Always verify information before marking as correct
    - Consistency: Use same standards across all annotations
    - Documentation: Provide clear remarks for incorrect/missing information
    - Context Matters: Consider full conversation context
    - Objectivity: Base annotations solely on transcript content

    Section-Specific Guidelines:

    1. Call Details:
    - Call ID: Must match format (e.g., "12345")
    - Call Date: Must be YYYY-MM-DD format
    - Call Type: Must match predefined categories

    2. Client Profile:
    - Client Age: Must be between 18-100
    - Current Balance: Must be numeric and non-negative
    - Years to Retirement: Must be positive integer

    3. Retirement Goals:
    - Goal Flag: Must be boolean
    - Goal List: Must contain valid retirement goals
    - Target Age: Must be greater than current age

    Common Scenarios and Validations:
    - Mark incorrect if format doesn't match requirements
    - Mark missing if required information is not present
    - Document conflicts and inconsistencies
    - Flag ambiguous or unclear information
    - Note any assumptions made during annotation

    Best Practices:
    - Read entire transcript before annotating
    - Cross-reference information across sections
    - Verify numerical values
    - Document all assumptions
    - Review for consistency
    """

def get_llm_response(prompt):
    """Get response from Ollama using Phi-2 model"""
    try:
        # Make request to Ollama API
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'phi4',
                'prompt': prompt,
                'stream': False
            }
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error: Unable to get response from Ollama (Status code: {response.status_code})"
    except Exception as e:
        return f"Error generating response: {str(e)}"

def chat_interface():
    """Create the chat interface"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.markdown('<div class="subheader">Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64B5F6; font-size: 0.9em;'>I'm trained on the annotation guidelines and can help you with any questions about the annotation process.</p>", unsafe_allow_html=True)
    
    # Chat messages container
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        message(msg["content"], is_user=msg["role"] == "user")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input container
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    def handle_input():
        if st.session_state.chat_input and st.session_state.chat_input.strip():
            user_message = st.session_state.chat_input.strip()
            
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Get response from Ollama
            assistant_response = get_llm_response(user_message)
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            # Trigger rerun
            st.rerun()
    
    st.text_input(
        "Ask me anything about the annotation process...",
        key="chat_input",
        on_change=handle_input
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Main app logic
def main():
    st.title("📞 Call Transcript Annotation Tool")
    add_custom_css()
    
    # Initialize sample data with hardcoded values
    sample_data = {
        "interaction_id": ["INT001", "INT002"],
        "annotator": ["Alice", "Bob"],
        "conversations": [
            "AGENT: Hello! Thank you for calling. How may I help you today?\nCUSTOMER: Hi, I'm having issues with my account login.\nAGENT: I understand. Can you please provide your account number?\nCUSTOMER: Yes, it's 12345678.",
            "AGENT: Good morning! How can I assist you today?\nCUSTOMER: I'd like to discuss retirement planning.\nAGENT: I'd be happy to help with that. Could you please verify your account number?\nCUSTOMER: Sure, it's 87654321."
        ],
        "llm_output": [
            json.dumps({
                "call_details": {
                    "call_id": "12345",
                    "call_date": "2024-12-13",
                    "call_type": "Initial Consultation"
                },
                "client_profile": {
                    "client_age": 45,
                    "current_401k_balance": 100000.0,
                    "years_to_retirement": 20
                },
                "retirement_test": {
                    "retirement_goal_flag": True,
                    "retirement_goals": ["travel", "start business"],
                    "retirement_age": 65
                }
            }),
            json.dumps({
                "call_details": {
                    "call_id": "67890",
                    "call_date": "2024-12-14",
                    "call_type": "Follow-up"
                },
                "client_profile": {
                    "client_age": 35,
                    "current_401k_balance": 75000.0,
                    "years_to_retirement": 30
                },
                "retirement_test": {
                    "retirement_goal_flag": True,
                    "retirement_goals": ["early retirement", "passive income"],
                    "retirement_age": 55
                }
            })
        ],
        "annotated_output": [None, None],
        "last_updated": [pd.Timestamp.now(), pd.Timestamp.now()]
    }
    
    # Create DataFrame from sample data
    try:
        annotations_df = pd.DataFrame(sample_data)
        # Load annotations
        # annotations_df = load_annotations()
        
        # Add filters in the sidebar
        st.sidebar.markdown("## Filter Conversations")
        
        # Annotator selection
        selected_annotator = st.sidebar.selectbox(
            "Select Annotator",
            options=annotations_df['annotator'].unique(),
            key='annotator_select'
        )
        
        # Interaction ID selection
        selected_interaction_id = st.sidebar.selectbox(
            "Select Interaction ID",
            options=annotations_df['interaction_id'].unique(),
            key='interaction_select'
        )
        
        # Filter the dataframe
        filtered_df = annotations_df[
            (annotations_df['annotator'] == selected_annotator) &
            (annotations_df['interaction_id'] == selected_interaction_id)
        ]
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Create tabs
    tabs = st.tabs([
        "📝 Transcript & Annotation", 
        "📊 View Annotations", 
        "📋 Annotation Guidelines",
        "💬 Chat Assistant"
    ])
    
    with tabs[0]:
        if not filtered_df.empty:
            # Get the first (and should be only) row
            row_df = filtered_df.iloc[0]
            
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
        else:
            st.warning("No data found for the selected filters.")

    with tabs[1]:
        st.subheader("View Submitted Annotations")
        # View annotations tab content
        if not annotations_df.empty and 'llm_output' in annotations_df.columns and 'annotated_output' in annotations_df.columns:
            # Filter out rows where annotated_output is None or same as llm_output
            view_df = annotations_df[
                (annotations_df['annotated_output'].notna()) & 
                (annotations_df['llm_output'] != annotations_df['annotated_output'])
            ]
            
            if not view_df.empty:
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    view_annotator = st.selectbox(
                        "Filter by Annotator",
                        options=['All'] + sorted(view_df['annotator'].unique().tolist())
                    )
                with col2:
                    view_interaction = st.selectbox(
                        "Filter by Interaction ID",
                        options=['All'] + sorted(view_df['interaction_id'].unique().tolist())
                    )
                
                # Apply filters
                if view_annotator != 'All':
                    view_df = view_df[view_df['annotator'] == view_annotator]
                if view_interaction != 'All':
                    view_df = view_df[view_df['interaction_id'] == view_interaction]
                
                # Display annotations
                if not view_df.empty:
                    for _, row in view_df.iterrows():
                        with st.expander(
                            f"Interaction: {row['interaction_id']} - "
                            f"Annotator: {row['annotator']} - "
                            f"Last Updated: {row.get('last_updated', 'Not updated')}"
                        ):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### Original LLM Output")
                                st.json(json.loads(row['llm_output']))
                            with col2:
                                st.markdown("#### Annotated Output")
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

    with tabs[2]:
        st.markdown("""
        # 📋 Annotation Guidelines
        
        ## Overview
        This comprehensive guide outlines the standards and procedures for annotating call transcripts. Follow these guidelines carefully to ensure consistency and accuracy across all annotations.
        
        ## General Principles
        1. **Accuracy First**: Always verify information before marking it as correct
        2. **Consistency**: Use the same standards across all annotations
        3. **Documentation**: Provide clear remarks for any incorrect or missing information
        4. **Context Matters**: Consider the full conversation context when annotating
        5. **Objectivity**: Base annotations solely on transcript content, not assumptions
        
        ## Validation Controls
        - **❌ Incorrect Marker**: Use when information is present but incorrect
        - **⚠️ Missing Marker**: Use when required information is not present
        - **Remarks Field**: Required when marking items as incorrect or missing
        
        ## Section-Specific Guidelines
        
        ### 1. Call Details
        #### Required Fields:
        - **Call ID**: Must match the format (e.g., "12345")
        - **Call Date**: Must be in YYYY-MM-DD format
        - **Call Type**: Must match predefined categories
        
        #### Common Scenarios:
        - 🔍 **Incorrect Format**: Mark as incorrect if ID format doesn't match
        - 🔍 **Future Dates**: Mark as incorrect if date is in the future
        - 🔍 **Invalid Call Type**: Mark as incorrect if not in approved list
        
        ### 2. Client Profile
        #### Required Fields:
        - **Client Age**: Must be between 18-100
        - **Current Balance**: Must be numeric and non-negative
        - **Years to Retirement**: Must be positive integer
        
        #### Common Scenarios:
        - 🔍 **Age Discrepancy**: Mark if age conflicts with other information
        - 🔍 **Balance Format**: Mark if balance includes non-numeric characters
        - 🔍 **Retirement Timeline**: Mark if conflicts with age/goals
        
        ### 3. Retirement Goals
        #### Required Fields:
        - **Goal Flag**: Must be boolean
        - **Goal List**: Must contain valid retirement goals
        - **Target Age**: Must be greater than current age
        
        #### Common Scenarios:
        - 🔍 **Implicit Goals**: Only mark goals explicitly mentioned
        - 🔍 **Conflicting Goals**: Note contradictions in remarks
        - 🔍 **Unrealistic Timeline**: Flag if retirement age is unrealistic
        
        ## Quality Control Checklist
        
        ### Before Annotation:
        1. ✓ Read entire transcript thoroughly
        2. ✓ Note key information while reading
        3. ✓ Identify potential inconsistencies
        
        ### During Annotation:
        1. ✓ Cross-reference information across sections
        2. ✓ Verify numerical values
        3. ✓ Check for logical consistency
        4. ✓ Document all assumptions
        
        ### After Annotation:
        1. ✓ Review all marked items
        2. ✓ Verify all remarks are clear and specific
        3. ✓ Check for missing required fields
        4. ✓ Ensure consistency across sections
        
        ## Common Pitfalls to Avoid
        
        ### 1. Assumption Errors
        - ❌ Don't assume information not explicitly stated
        - ❌ Don't infer demographics without evidence
        - ❌ Don't extrapolate beyond given data
        
        ### 2. Validation Errors
        - ❌ Don't mark correct information as incorrect
        - ❌ Don't leave remarks empty for marked items
        - ❌ Don't ignore format requirements
        
        ### 3. Consistency Errors
        - ❌ Don't use different standards across calls
        - ❌ Don't ignore conflicts between sections
        - ❌ Don't skip validation steps
        
        ## Special Cases
        
        ### 1. Ambiguous Information
        - 📝 Document uncertainty in remarks
        - 📝 Note multiple possible interpretations
        - 📝 Flag for review if critically ambiguous
        
        ### 2. Missing Context
        - 📝 Mark information as missing
        - 📝 Note specific missing context
        - 📝 Don't make assumptions to fill gaps
        
        ### 3. Conflicting Information
        - 📝 Document all conflicts
        - 📝 Note which source seems more reliable
        - 📝 Flag for review if unresolvable
        
        ## Best Practices for Remarks
        
        ### 1. Writing Clear Remarks
        - ✍️ Be specific and concise
        - ✍️ Reference relevant transcript portions
        - ✍️ Use standard terminology
        
        ### 2. Documenting Issues
        - ✍️ State the specific problem
        - ✍️ Provide evidence from transcript
        - ✍️ Suggest correct information if known
        
        ### 3. Handling Uncertainty
        - ✍️ Note degree of uncertainty
        - ✍️ List alternative interpretations
        - ✍️ Explain impact on annotation
        
        ## Review Process
        
        ### 1. Self-Review
        1. 🔍 Review all marked items
        2. 🔍 Verify remark clarity
        3. 🔍 Check for missed issues
        
        ### 2. Peer Review
        1. 🔍 Another annotator reviews
        2. 🔍 Compare interpretations
        3. 🔍 Resolve disagreements
        
        ### 3. Final Validation
        1. 🔍 Check all required fields
        2. 🔍 Verify all marks have remarks
        3. 🔍 Ensure consistency
        
        ## Support and Questions
        
        If you encounter situations not covered by these guidelines or have questions:
        1. Consult with senior annotators
        2. Document the scenario for future reference
        3. Propose guideline updates if needed
        
        Remember: Quality annotations are crucial for improving our system. Take the time needed to ensure accuracy and completeness.
        """)

    with tabs[3]:
        chat_interface()

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
        
        # Initialize session state for list items if not already initialized
        if f"list_items_{field_id}" not in st.session_state:
            st.session_state[f"list_items_{field_id}"] = value.copy()
        
        updated_list = []
        
        # Display existing items
        for i, item in enumerate(st.session_state[f"list_items_{field_id}"]):
            with st.container():
                col1, col2, col3 = st.columns([3, 0.5, 0.5])
                with col1:
                    # Initialize session state for this item if not already done
                    if f"input_{field_id}_{i}" not in st.session_state:
                        st.session_state[f"input_{field_id}_{i}"] = item
                    
                    input_value = st.text_area(
                        f"Item {i + 1}", 
                        value=st.session_state[f"input_{field_id}_{i}"],
                        key=f"text_{field_id}_{i}"
                    )
                    
                    # Update session state
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
                    "value": input_value,
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
        
        # Add new item if there's input and form is submitted
        if new_item and st.session_state.get("form_submitted", False):
            st.session_state[f"list_items_{field_id}"].append(new_item)
            updated_list.append({
                "value": new_item,
                "is_correct": True,
                "is_missing": False,
                "remark": ""
            })
        
        return updated_list
    
    else:
        return str(value)

if __name__ == "__main__":
    main()