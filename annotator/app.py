import streamlit as st
import pandas as pd
import json
import numpy as np
from gtts import gTTS
import base64
import os
from streamlit_chat import message
import requests
from collections import Counter
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
        
        /* Enhanced Button Styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #64B5F6, #1976D2) !important;
            color: white !important;
            padding: 15px 30px !important;
            font-size: 1.1em !important;
            font-weight: 500 !important;
            border: none !important;
            border-radius: 12px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2) !important;
            margin-top: 20px !important;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 10px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3) !important;
            background: linear-gradient(135deg, #82c4f8, #1976D2) !important;
            border-color: rgba(100, 181, 246, 0.4) !important;
        }

        .stButton > button:active {
            transform: translateY(1px) !important;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2) !important;
        }

        .stButton > button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                120deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            transition: all 0.6s ease;
        }

        .stButton > button:hover::before {
            left: 100%;
        }

        /* Save Button Container */
        .save-button-container {
            background: rgba(26, 41, 66, 0.7);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(100, 181, 246, 0.2);
            margin-top: 40px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Button Icon Animation */
        .stButton > button svg,
        .stButton > button img {
            transition: transform 0.3s ease;
        }

        .stButton > button:hover svg,
        .stButton > button:hover img {
            transform: scale(1.1);
        }

        /* Button Text Shadow */
        .stButton > button span {
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

        /* Status Badge Styles */
        .status-badge {
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 8px 0;
            transition: all 0.3s ease;
        }
        
        .status-badge:before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }
        
        .status-not-started {
            background: rgba(158, 158, 158, 0.1);
            color: #9E9E9E;
            border: 1px solid rgba(158, 158, 158, 0.2);
        }
        
        .status-not-started:before {
            background: #9E9E9E;
            box-shadow: 0 0 8px rgba(158, 158, 158, 0.5);
        }
        
        .status-in-progress {
            background: rgba(255, 193, 7, 0.1);
            color: #FFC107;
            border: 1px solid rgba(255, 193, 7, 0.2);
        }
        
        .status-in-progress:before {
            background: #FFC107;
            box-shadow: 0 0 8px rgba(255, 193, 7, 0.5);
        }
        
        .status-completed {
            background: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
            border: 1px solid rgba(76, 175, 80, 0.2);
        }
        
        .status-completed:before {
            background: #4CAF50;
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
        }
        
        /* Status Progress Bar */
        .status-progress {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            margin-top: 15px;
            overflow: hidden;
        }
        
        .status-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #64B5F6, #2196F3);
            border-radius: 2px;
            transition: width 0.3s ease;
        }
        
        /* Sidebar Status Styles */
        .sidebar-status-container {
            background: rgba(26, 41, 66, 0.7);
            border-radius: 12px;
            padding: 15px;
            margin: 20px 0;
            border: 1px solid rgba(100, 181, 246, 0.2);
            backdrop-filter: blur(10px);
        }
        
        .sidebar-status-header {
            color: #64B5F6;
            font-size: 0.9em;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        /* Horizontal Progress Container */
        .horizontal-progress-container {
            display: flex;
            align-items: center;
            gap: 20px;
            background: rgba(26, 41, 66, 0.7);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border: 1px solid rgba(100, 181, 246, 0.2);
        }
        
        .progress-stats {
            display: flex;
            gap: 15px;
            flex-grow: 1;
        }
        
        .progress-header {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 200px;
        }
        
        .horizontal-status-badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .horizontal-progress-bar {
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 10px;
            width: 100%;
        }
        
        /* Feedback Questions Container */
        .feedback-questions {
            background: rgba(26, 41, 66, 0.7);
            border: 1px solid rgba(100, 181, 246, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        /* Radio Button Container */
        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: rgba(26, 41, 66, 0.4);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(100, 181, 246, 0.1);
        }
        
        /* Individual Radio Option */
        .stRadio [role="radio"] {
            background: rgba(26, 41, 66, 0.7) !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            padding: 12px 20px !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
            color: #A4B5C6 !important;
        }
        
        /* Radio Option Hover */
        .stRadio [role="radio"]:hover {
            background: rgba(100, 181, 246, 0.1) !important;
            transform: translateX(5px);
        }
        
        /* Selected Radio Option */
        .stRadio [role="radio"][data-checked="true"] {
            background: rgba(100, 181, 246, 0.2) !important;
            border-color: #64B5F6 !important;
            color: #64B5F6 !important;
            transform: translateX(5px);
            box-shadow: 0 0 15px rgba(100, 181, 246, 0.1);
        }
        
        /* Question Label */
        .feedback-question-label {
            color: #64B5F6;
            font-size: 1em;
            font-weight: 500;
            margin-bottom: 10px;
            display: block;
        }
        
        /* Question Description */
        .feedback-question-desc {
            color: #A4B5C6;
            font-size: 0.9em;
            margin-bottom: 15px;
            display: block;
        }
        
        /* Question Group */
        .feedback-question-group {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(100, 181, 246, 0.1);
        }
        
        .feedback-question-group:last-child {
            border-bottom: none;
            padding-bottom: 0;
            margin-bottom: 0;
        }

        /* Main content area */
        .main .block-container {
            padding: 1rem !important;
            max-width: 100%;
        }

        /* Status Update Dropdown Styling */
        [data-testid="stSelectbox"] {
            margin-top: 10px;
        }

        [data-testid="stSelectbox"] > div > div {
            background: rgba(26, 41, 66, 0.7) !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            border-radius: 8px !important;
            color: #64B5F6 !important;
            min-height: 45px;
        }

        [data-testid="stSelectbox"] > div > div:hover {
            border-color: #64B5F6 !important;
            box-shadow: 0 0 0 1px rgba(100, 181, 246, 0.3) !important;
        }

        [data-testid="stSelectbox"] > div > div > div {
            color: #64B5F6 !important;
        }

        /* Dropdown options styling */
        [data-testid="stSelectbox"] ul {
            background-color: rgba(26, 41, 66, 0.95) !important;
            border: 1px solid rgba(100, 181, 246, 0.2) !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }

        [data-testid="stSelectbox"] ul li {
            background-color: transparent !important;
            color: #A4B5C6 !important;
            transition: all 0.2s ease;
        }

        [data-testid="stSelectbox"] ul li:hover {
            background-color: rgba(100, 181, 246, 0.1) !important;
            color: #64B5F6 !important;
        }

        [data-testid="stSelectbox"] ul li[aria-selected="true"] {
            background-color: rgba(100, 181, 246, 0.2) !important;
            color: #64B5F6 !important;
        }

        /* Status Update Label */
        .sidebar-status-update {
            color: #64B5F6;
            font-size: 0.9em;
            font-weight: 500;
            margin: 20px 0 5px 0;
            padding: 0;
            opacity: 0.9;
        }

        /* Status Container */
        .status-update-container {
            background: rgba(26, 41, 66, 0.7);
            border: 1px solid rgba(100, 181, 246, 0.2);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
        }

        /* Tooltip Styling */
        .tooltip-container {
            position: relative;
            display: inline-flex;
            align-items: center;
            margin-left: 4px;
        }

        .tooltip-container span {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 2px;
            border-radius: 50%;
            background: rgba(100, 181, 246, 0.1);
            transition: all 0.3s ease;
            cursor: help;
        }

        .tooltip-container:hover span {
            background: rgba(100, 181, 246, 0.2);
            transform: scale(1.1);
        }

        .tooltip-container svg {
            transition: all 0.3s ease;
        }

        .tooltip-container:hover svg {
            transform: scale(1.1);
        }

        .tooltip-container:hover svg circle,
        .tooltip-container:hover svg path {
            stroke-opacity: 1;
        }

        /* Tooltip Text */
        .tooltip-text {
            visibility: hidden;
            background: rgba(26, 41, 66, 0.98);
            color: #fff;
            text-align: left;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(100, 181, 246, 0.2);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            
            /* Position the tooltip */
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            
            /* Size constraints */
            min-width: 200px;
            max-width: 300px;
            
            /* Fade in animation */
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Tooltip Arrow */
        .tooltip-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: rgba(26, 41, 66, 0.98) transparent transparent transparent;
        }

        /* Show tooltip on hover */
        .tooltip-container:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(-5px);
        }

        /* Tooltip Title */
        .tooltip-title {
            color: #64B5F6;
            font-weight: 500;
            margin-bottom: 6px;
            font-size: 0.9em;
        }

        /* Tooltip Description */
        .tooltip-description {
            color: #A4B5C6;
            font-size: 0.85em;
            line-height: 1.5;
        }

        /* Nested Field Title Styling */
        .nested-field-title {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 5px;
        }

        .nested-field-title .section-name {
            color: #64B5F6;
            font-size: 0.9em;
            opacity: 0.8;
        }

        .nested-field-title .separator {
            color: #64B5F6;
            opacity: 0.5;
            margin: 0 4px;
        }

        .nested-field-title .field-name {
            color: #64B5F6;
            font-size: 0.9em;
        }

        /* Update the field container styling */
        .field-container {
            background: rgba(26, 41, 66, 0.4);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(100, 181, 246, 0.1);
            transition: all 0.3s ease;
        }

        .field-container:hover {
            background: rgba(26, 41, 66, 0.5);
            border-color: rgba(100, 181, 246, 0.2);
        }

        /* Update tooltip container for nested fields */
        .nested-field .tooltip-container {
            margin-left: 8px;
        }

        .nested-field .tooltip-text {
            min-width: 250px;
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
    """Get response from Ollama using Phi-2 model with streaming"""
    try:
        # Make request to Ollama API with streaming enabled
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'phi',
                'prompt': prompt,
                'stream': True  # Enable streaming
            },
            stream=True  # Enable streaming for requests
        )
        
        if response.status_code == 200:
            # Return a generator that yields chunks of text
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield chunk['response']
        else:
            yield f"Error: Unable to get response from Ollama (Status code: {response.status_code})"
    except Exception as e:
        yield f"Error generating response: {str(e)}"

def chat_interface():
    """Create the chat interface with streaming support"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.markdown('<div class="subheader">Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64B5F6; font-size: 0.9em;'>I'm trained on the annotation guidelines and can help you with any questions about the annotation process.</p>", unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            message(msg["content"], is_user=msg["role"] == "user", key=f"msg_{hash(msg['content'])}")
    
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
            
            # Create a placeholder for streaming response
            with chat_container:
                message_placeholder = st.empty()
                full_response = ""
                
                # Stream the response
                for response_chunk in get_llm_response(user_message):
                    full_response += response_chunk
                    # Update the message placeholder with accumulated response
                    message_placeholder.markdown(full_response)
            
            # Add complete response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": full_response
            })
            
            # Clear input
            st.session_state.chat_input = ""
    
    st.text_input(
        "Ask me anything about the annotation process...",
        key="chat_input",
        on_change=handle_input
    )
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_metrics(df):
    """Calculate metrics from LLM and annotated outputs with sample data for visualization"""
    # Sample data for visualization
    metrics = {
        'total_annotations': 150,
        'completed_annotations': 120,
        'accuracy_metrics': {
            'overall_accuracy': 87.5,
            'precision': 86.3,  # Added precision
            'recall': 85.7,     # Added recall
            'f1_score': 86.0,   # Added f1_score
            'field_accuracy': 85.2,
            'section_accuracy': 89.3,
            'trend': [
                {'date': '2024-03-01', 'accuracy': 82.5, 'precision': 81.2, 'recall': 80.8},
                {'date': '2024-03-02', 'accuracy': 84.1, 'precision': 83.5, 'recall': 82.9},
                {'date': '2024-03-03', 'accuracy': 85.7, 'precision': 84.8, 'recall': 84.2},
                {'date': '2024-03-04', 'accuracy': 86.2, 'precision': 85.4, 'recall': 84.9},
                {'date': '2024-03-05', 'accuracy': 87.5, 'precision': 86.3, 'recall': 85.7}
            ]
        },
        'field_level_metrics': {
            'call_details.call_id': {
                'total_occurrences': 150,
                'correct_count': 142,
                'incorrect_count': 5,
                'missing_count': 3,
                'accuracy_rate': 94.7,
                'precision': 93.8,
                'recall': 92.5,
                'common_errors': ['Invalid format', 'Duplicate ID', 'Missing prefix'],
                'trend': [90.5, 92.1, 93.4, 94.7]
            },
            'client_profile.client_age': {
                'total_occurrences': 150,
                'correct_count': 138,
                'incorrect_count': 8,
                'missing_count': 4,
                'accuracy_rate': 92.0,
                'precision': 91.5,
                'recall': 90.8,
                'common_errors': ['Age mismatch', 'Invalid range', 'Typo in value'],
                'trend': [88.2, 89.5, 90.8, 92.0]
            },
            'retirement_test.retirement_age': {
                'total_occurrences': 150,
                'correct_count': 135,
                'incorrect_count': 10,
                'missing_count': 5,
                'accuracy_rate': 90.0,
                'precision': 89.5,
                'recall': 88.7,
                'common_errors': ['Unrealistic age', 'Inconsistent with goals', 'Below current age'],
                'trend': [86.5, 87.8, 89.1, 90.0]
            },
            'client_profile.current_401k_balance': {
                'total_occurrences': 150,
                'correct_count': 140,
                'incorrect_count': 7,
                'missing_count': 3,
                'accuracy_rate': 93.3,
                'precision': 92.8,
                'recall': 91.9,
                'common_errors': ['Format error', 'Negative value', 'Invalid currency'],
                'trend': [89.8, 91.2, 92.5, 93.3]
            }
        },
        'section_metrics': {
            'call_details': {
                'total_fields': 450,
                'correct_fields': 410,
                'incorrect_fields': 25,
                'missing_fields': 15,
                'accuracy_rate': 91.1,
                'trend': [87.5, 88.9, 90.2, 91.1],
                'error_distribution': {
                    'format_errors': 12,
                    'missing_data': 8,
                    'inconsistencies': 5
                }
            },
            'client_profile': {
                'total_fields': 450,
                'correct_fields': 395,
                'incorrect_fields': 35,
                'missing_fields': 20,
                'accuracy_rate': 87.8,
                'trend': [84.2, 85.5, 86.8, 87.8],
                'error_distribution': {
                    'format_errors': 15,
                    'missing_data': 12,
                    'inconsistencies': 8
                }
            },
            'retirement_test': {
                'total_fields': 450,
                'correct_fields': 380,
                'incorrect_fields': 45,
                'missing_fields': 25,
                'accuracy_rate': 84.4,
                'trend': [81.1, 82.4, 83.7, 84.4],
                'error_distribution': {
                    'format_errors': 18,
                    'missing_data': 15,
                    'inconsistencies': 12
                }
            }
        },
        'error_patterns': {
            'top_errors': [
                ('Format errors', 45),
                ('Missing data', 35),
                ('Inconsistencies', 25),
                ('Invalid values', 20),
                ('Duplicate entries', 15)
            ],
            'error_trends': {
                '2024-03-01': {'format': 12, 'missing': 10, 'invalid': 8},
                '2024-03-02': {'format': 10, 'missing': 8, 'invalid': 7},
                '2024-03-03': {'format': 8, 'missing': 7, 'invalid': 5},
                '2024-03-04': {'format': 7, 'missing': 5, 'invalid': 4},
                '2024-03-05': {'format': 5, 'missing': 4, 'invalid': 3}
            },
            'field_specific': {
                'call_details.call_id': [
                    ('Invalid format', 15),
                    ('Duplicate ID', 8),
                    ('Missing prefix', 5)
                ],
                'client_profile.client_age': [
                    ('Age mismatch', 12),
                    ('Invalid range', 10),
                    ('Typo in value', 6)
                ],
                'retirement_test.retirement_age': [
                    ('Unrealistic age', 18),
                    ('Inconsistent with goals', 12),
                    ('Below current age', 8)
                ]
            }
        },
        'time_metrics': {
            'avg_time_per_annotation': pd.Timedelta(minutes=15),
            'completion_trend': pd.Series({
                pd.Timestamp('2024-03-01'): 15,
                pd.Timestamp('2024-03-02'): 18,
                pd.Timestamp('2024-03-03'): 22,
                pd.Timestamp('2024-03-04'): 20,
                pd.Timestamp('2024-03-05'): 25,
                pd.Timestamp('2024-03-06'): 28,
                pd.Timestamp('2024-03-07'): 30
            }),
            'time_distribution': {
                '<10min': 25,
                '10-15min': 45,
                '15-20min': 35,
                '20-25min': 25,
                '>25min': 20
            },
            'daily_stats': {
                'avg_annotations_per_day': 21.4,
                'peak_day_count': 30,
                'low_day_count': 15
            },
            'efficiency_metrics': {
                'accuracy_vs_time': [
                    {'time_range': '<10min', 'accuracy': 82.5},
                    {'time_range': '10-15min', 'accuracy': 87.8},
                    {'time_range': '15-20min', 'accuracy': 89.2},
                    {'time_range': '20-25min', 'accuracy': 88.5},
                    {'time_range': '>25min', 'accuracy': 87.1}
                ]
            }
        },
        'quality_metrics': {
            'consistency_score': 92.5,
            'completeness_score': 88.7,
            'accuracy_by_annotator': {
                'Alice': 91.2,
                'Bob': 88.5,
                'Charlie': 89.7,
                'Diana': 90.3
            },
            'quality_trends': [
                {'date': '2024-03-01', 'score': 87.5},
                {'date': '2024-03-02', 'score': 88.2},
                {'date': '2024-03-03', 'score': 89.1},
                {'date': '2024-03-04', 'score': 89.8},
                {'date': '2024-03-05', 'score': 90.5}
            ],
            'review_metrics': {
                'reviewed_count': 85,
                'pending_review': 35,
                'approved_first_time': 72,
                'required_revision': 13
            }
        },
        'detailed_analysis': {
            'error_patterns': {
                'systematic_errors': [
                    {'error_type': 'Format Error', 'frequency': 45, 'impact': 'High', 'fields_affected': ['call_id', 'date']},
                    {'error_type': 'Missing Data', 'frequency': 35, 'impact': 'Medium', 'fields_affected': ['retirement_goals']},
                    {'error_type': 'Inconsistency', 'frequency': 25, 'impact': 'High', 'fields_affected': ['age', 'retirement_age']},
                    {'error_type': 'Invalid Values', 'frequency': 20, 'impact': 'Medium', 'fields_affected': ['401k_balance']}
                ],
                'error_correlations': [
                    {'primary_error': 'Format Error', 'correlated_error': 'Missing Data', 'correlation_strength': 0.75},
                    {'primary_error': 'Inconsistency', 'correlated_error': 'Invalid Values', 'correlation_strength': 0.65},
                    {'primary_error': 'Missing Data', 'correlated_error': 'Invalid Values', 'correlation_strength': 0.45}
                ]
            },
            'quality_indicators': {
                'completeness_score': 0.88,
                'consistency_score': 0.92,
                'accuracy_score': 0.85,
                'timeliness_score': 0.90
            },
            'error_distribution': {
                'by_field': {
                    'call_id': {'error_rate': 0.15, 'common_issues': ['format', 'missing']},
                    'client_age': {'error_rate': 0.12, 'common_issues': ['inconsistency', 'invalid']},
                    'retirement_goals': {'error_rate': 0.18, 'common_issues': ['missing', 'incomplete']}
                },
                'by_annotator': {
                    'Alice': {'error_rate': 0.10, 'strength': 'format validation'},
                    'Bob': {'error_rate': 0.15, 'strength': 'consistency check'},
                    'Charlie': {'error_rate': 0.12, 'strength': 'completeness'}
                }
            }
        },
        'feedback_analysis': {
            'sentiment_scores': {
                'Positive': 45,
                'Neutral': 35,
                'Negative': 20
            },
            'key_themes': [
                {'theme': 'Data Quality', 'frequency': 25, 'sentiment': 0.65},
                {'theme': 'Tool Usability', 'frequency': 20, 'sentiment': 0.75},
                {'theme': 'Guidelines Clarity', 'frequency': 15, 'sentiment': 0.55}
            ],
            'improvement_areas': [
                {'area': 'Format Validation', 'frequency': 15, 'impact_score': 0.85},
                {'area': 'Error Detection', 'frequency': 12, 'impact_score': 0.75},
                {'area': 'User Interface', 'frequency': 10, 'impact_score': 0.65}
            ]
        }
    }
    
    return metrics

def render_metrics_dashboard(df):
    """Render the metrics dashboard with advanced visualizations"""
    metrics = calculate_metrics(df)
    
    # Add custom CSS for metrics dashboard
    st.markdown("""
        <style>
        .metric-card {
            background: rgba(26, 41, 66, 0.7);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(100, 181, 246, 0.2);
        }
        
        .metric-header {
            color: #64B5F6;
            font-size: 1.2em;
            font-weight: 500;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(100, 181, 246, 0.1);
        }
        
        .metric-subheader {
            color: #A4B5C6;
            font-size: 1em;
            margin: 10px 0;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: 600;
            color: #64B5F6;
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #A4B5C6;
        }
        
        .progress-container {
            background: rgba(26, 41, 66, 0.3);
            border-radius: 5px;
            height: 6px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #64B5F6, #2196F3);
            transition: width 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    # Overall Metrics Section
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-header">Overall Performance</div>', unsafe_allow_html=True)
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        accuracy = metrics['accuracy_metrics']['overall_accuracy']
        st.markdown(
            f"""
            <div>
                <div class="metric-label">Overall Accuracy</div>
                <div class="metric-value">{accuracy:.1f}%</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {accuracy}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        precision = metrics['accuracy_metrics']['precision']
        st.markdown(
            f"""
            <div>
                <div class="metric-label">Precision</div>
                <div class="metric-value">{precision:.1f}%</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {precision}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        recall = metrics['accuracy_metrics']['recall']
        st.markdown(
            f"""
            <div>
                <div class="metric-label">Recall</div>
                <div class="metric-value">{recall:.1f}%</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {recall}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        f1_score = metrics['accuracy_metrics']['f1_score']
        st.markdown(
            f"""
            <div>
                <div class="metric-label">F1 Score</div>
                <div class="metric-value">{f1_score:.1f}%</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {f1_score}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Performance Trends
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-header">Performance Trends</div>', unsafe_allow_html=True)
    trend_data = pd.DataFrame(metrics['accuracy_metrics']['trend'])
    st.line_chart(trend_data.set_index('date')[['accuracy', 'precision', 'recall']])
    st.markdown('</div>', unsafe_allow_html=True)

    # Field-Level Analysis
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-header">Field-Level Analysis</div>', unsafe_allow_html=True)
    
    for field, metrics in metrics['field_level_metrics'].items():
        st.markdown(f'<div class="metric-subheader">{field}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Accuracy", f"{metrics['accuracy_rate']:.1f}%")
        with col2:
            st.metric("Precision", f"{metrics['precision']:.1f}%")
        with col3:
            st.metric("Recall", f"{metrics['recall']:.1f}%")
        
        # Subattribute Analysis
        if 'subattributes' in metrics:
            st.markdown('<div class="metric-subheader">Subattribute Analysis</div>', unsafe_allow_html=True)
            subattr_df = pd.DataFrame([
                {'Subattribute': k, 'Precision': v['precision'], 'Recall': v['recall']}
                for k, v in metrics['subattributes'].items()
            ])
            st.dataframe(subattr_df.style.format({'Precision': '{:.1f}%', 'Recall': '{:.1f}%'}))
    
    st.markdown('</div>', unsafe_allow_html=True)


# Main app logic
def main():
    st.title("📞 Call Transcript Annotation Tool")
    add_custom_css()
    
    # Initialize sample data with hardcoded values
    sample_data = {
        "interaction_id": ["INT001", "INT002"],
        "annotator": ["Alice", "Bob"],
        "status": ["Not Started", "In Progress"],  # Add status field
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
    
    try:
        annotations_df = pd.DataFrame(sample_data)
        
        # Add filters in the sidebar
        st.sidebar.markdown("## Filter Conversations")
        
        # Annotator selection with unique key
        selected_annotator = st.sidebar.selectbox(
            "Select Annotator",
            options=annotations_df['annotator'].unique(),
            key='sidebar_annotator_select'
        )
        
        # Interaction ID selection with unique key
        selected_interaction_id = st.sidebar.selectbox(
            "Select Interaction ID",
            options=annotations_df['interaction_id'].unique(),
            key='sidebar_interaction_select'
        )
        
        # Add separator
        st.sidebar.markdown("<hr style='margin: 25px 0; border: none; border-top: 1px solid rgba(100, 181, 246, 0.2);'>", unsafe_allow_html=True)
        
        # Get current status for selected annotation
        filtered_df = annotations_df[
            (annotations_df['annotator'] == selected_annotator) &
            (annotations_df['interaction_id'] == selected_interaction_id)
        ]
        
        if not filtered_df.empty:
            current_status = filtered_df['status'].iloc[0]
            
            # Add status selector in sidebar with unique key
            st.sidebar.markdown(
                f"""
                <div class="status-update-container">
                    <div class="sidebar-status-header">Current Annotation Status</div>
                    <div class="status-badge status-{current_status.lower().replace(' ', '-')}">
                        {current_status}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.sidebar.markdown('<div class="sidebar-status-update">Update Status</div>', unsafe_allow_html=True)
            # Status selector in sidebar with unique key
            new_status = st.sidebar.selectbox(
                "",
                options=["Not Started", "In Progress", "Completed"],
                index=["Not Started", "In Progress", "Completed"].index(current_status),
                key='sidebar_status_select',
                label_visibility="collapsed"
            )
            
            # Update status if changed
            if new_status != current_status:
                try:
                    row_index = filtered_df.index[0]
                    annotations_df.at[row_index, 'status'] = new_status
                    annotations_df.at[row_index, 'last_updated'] = pd.Timestamp.now()
                    st.session_state.df = annotations_df
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating status: {str(e)}")
        
        # Create tabs
        tabs = st.tabs([
            "📝 Transcript & Annotation", 
            "📊 View Annotations", 
            "📋 Annotation Guidelines",
            "💬 Chat Assistant",
            "📈 Metrics Dashboard"  # New tab
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
                    
                    # Create a container for annotations
                    annotation_container = st.container(border=True)
                    
                    with annotation_container:
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
                            
                            # Add feedback questions section
                            st.markdown(
                                """
                                <div style="margin: 30px 0;">
                                    <div style="color: #64B5F6; font-size: 1.2em; font-weight: 500; margin-bottom: 15px;">
                                        ⭐ Feedback Questions
                                    </div>
                                    <div style="color: #A4B5C6; font-size: 0.9em; margin-bottom: 20px;">
                                        Please rate the following aspects of the conversation.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Question 1: Call Quality
                            st.markdown('<div class="feedback-question-group">', unsafe_allow_html=True)
                            st.markdown('<label class="feedback-question-label">1. Overall Call Quality</label>', unsafe_allow_html=True)
                            st.markdown('<span class="feedback-question-desc">How would you rate the overall quality of the call interaction?</span>', unsafe_allow_html=True)
                            call_quality = st.radio(
                                "",
                                options=["Excellent", "Good", "Average", "Below Average", "Poor"],
                                key="call_quality",
                                label_visibility="collapsed"
                            )
                            if call_quality in ["Poor", "Below Average"]:
                                call_quality_feedback = st.text_area(
                                    "Please provide details about the call quality issues:",
                                    key="call_quality_feedback",
                                    height=100,
                                    placeholder="Explain what aspects of the call quality need improvement..."
                                )
                                updated_sections["call_quality_feedback"] = call_quality_feedback
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Question 2: Agent Performance
                            st.markdown('<div class="feedback-question-group">', unsafe_allow_html=True)
                            st.markdown('<label class="feedback-question-label">2. Agent Performance</label>', unsafe_allow_html=True)
                            st.markdown('<span class="feedback-question-desc">How effectively did the agent handle the customer\'s needs?</span>', unsafe_allow_html=True)
                            agent_performance = st.radio(
                                "",
                                options=["Exceptional", "Above Average", "Satisfactory", "Needs Improvement", "Unsatisfactory"],
                                key="agent_performance",
                                label_visibility="collapsed"
                            )
                            if agent_performance in ["Needs Improvement", "Unsatisfactory"]:
                                agent_feedback = st.text_area(
                                    "Please provide details about the agent's performance issues:",
                                    key="agent_feedback",
                                    height=100,
                                    placeholder="Explain what aspects of the agent's performance need improvement..."
                                )
                                updated_sections["agent_feedback"] = agent_feedback
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Question 3: Customer Satisfaction
                            st.markdown('<div class="feedback-question-group">', unsafe_allow_html=True)
                            st.markdown('<label class="feedback-question-label">3. Customer Satisfaction</label>', unsafe_allow_html=True)
                            st.markdown('<span class="feedback-question-desc">Based on the interaction, how satisfied do you think the customer was?</span>', unsafe_allow_html=True)
                            customer_satisfaction = st.radio(
                                "",
                                options=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
                                key="customer_satisfaction",
                                label_visibility="collapsed"
                            )
                            if customer_satisfaction in ["Dissatisfied", "Very Dissatisfied"]:
                                satisfaction_feedback = st.text_area(
                                    "Please provide details about the customer satisfaction issues:",
                                    key="satisfaction_feedback",
                                    height=100,
                                    placeholder="Explain what aspects led to customer dissatisfaction..."
                                )
                                updated_sections["satisfaction_feedback"] = satisfaction_feedback
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Question 4: Resolution Effectiveness
                            st.markdown('<div class="feedback-question-group">', unsafe_allow_html=True)
                            st.markdown('<label class="feedback-question-label">4. Resolution Effectiveness</label>', unsafe_allow_html=True)
                            st.markdown('<span class="feedback-question-desc">How effectively was the customer\'s issue resolved?</span>', unsafe_allow_html=True)
                            resolution_effectiveness = st.radio(
                                "",
                                options=["Completely Resolved", "Mostly Resolved", "Partially Resolved", "Minimally Resolved", "Not Resolved"],
                                key="resolution_effectiveness",
                                label_visibility="collapsed"
                            )
                            if resolution_effectiveness in ["Minimally Resolved", "Not Resolved", "Partially Resolved"]:
                                resolution_feedback = st.text_area(
                                    "Please provide details about the resolution issues:",
                                    key="resolution_feedback",
                                    height=100,
                                    placeholder="Explain what aspects of the resolution were inadequate..."
                                )
                                updated_sections["resolution_feedback"] = resolution_feedback
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Add the feedback ratings to updated_sections
                            updated_sections.update({
                                "call_quality_rating": call_quality,
                                "agent_performance_rating": agent_performance,
                                "customer_satisfaction_rating": customer_satisfaction,
                                "resolution_effectiveness_rating": resolution_effectiveness
                            })
                            
                            # Add Save button with enhanced styling
                            st.markdown(
                                """
                                <div class="save-button-container">
                                    <div style="text-align: center;">
                                        <div style="color: #64B5F6; font-size: 1.1em; font-weight: 500; margin-bottom: 8px;">
                                            Ready to Submit?
                                        </div>
                                        <div style="color: #A4B5C6; font-size: 0.9em; margin-bottom: 20px;">
                                            Save your annotations to submit them for review
                                        </div>
                                    </div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                if st.button(
                                    "💾  Save Annotations  ✨",
                                    key="save_annotations",
                                    type="primary",
                                    use_container_width=True,
                                ):
                                    try:
                                        row_index = row_df.name
                                        current_df = pd.read_parquet("annotations.parquet")
                                        current_df.at[row_index, 'annotated_output'] = json.dumps(updated_sections, indent=2)
                                        current_df.at[row_index, 'last_updated'] = pd.Timestamp.now()
                                        current_df.to_parquet("annotations.parquet", index=False)
                                        st.session_state.df = current_df
                                        
                                        # Show success message with animation
                                        st.markdown(
                                            """
                                            <div class="flash-message flash-success">
                                                ✅ Annotations saved successfully!
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                        st.experimental_rerun()
                                    except Exception as e:
                                        # Show error message with animation
                                        st.markdown(
                                            f"""
                                            <div class="flash-message flash-error">
                                                ❌ Error saving annotation: {str(e)}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                        st.experimental_rerun()
            else:
                st.warning("No data found for the selected filters.")

        with tabs[1]:
            st.subheader("View Submitted Annotations")
            
            # Calculate status counts
            total_annotations = len(annotations_df)
            completed = len(annotations_df[annotations_df['status'] == 'Completed'])
            in_progress = len(annotations_df[annotations_df['status'] == 'In Progress'])
            not_started = len(annotations_df[annotations_df['status'] == 'Not Started'])
            
            completion_percentage = (completed / total_annotations * 100) if total_annotations > 0 else 0
            
            # Add horizontal progress section
            st.markdown(
                f"""
                <div class="horizontal-progress-container">
                    <div class="progress-header">
                        <span style="font-size: 1.2em;">📊</span>
                        <div>
                            <div style="color: #64B5F6; font-weight: 500;">Annotation Progress</div>
                            <div style="font-size: 0.8em; color: #A4B5C6; margin-top: 4px;">
                                {completion_percentage:.1f}% Complete
                            </div>
                        </div>
                    </div>
                    <div class="progress-stats">
                        <div class="horizontal-status-badge status-completed">
                            <span style="min-width: 24px; text-align: right;">{completed}</span>
                            <span>Completed</span>
                        </div>
                        <div class="horizontal-status-badge status-in-progress">
                            <span style="min-width: 24px; text-align: right;">{in_progress}</span>
                            <span>In Progress</span>
                        </div>
                        <div class="horizontal-status-badge status-not-started">
                            <span style="min-width: 24px; text-align: right;">{not_started}</span>
                            <span>Not Started</span>
                        </div>
                    </div>
                </div>
                <div class="horizontal-progress-bar">
                    <div class="status-progress-bar" style="width: {completion_percentage}%;"></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # View annotations tab content
            if not annotations_df.empty:
                # Add filters with unique keys
                col1, col2, col3 = st.columns(3)
                with col1:
                    view_annotator = st.selectbox(
                        "Filter by Annotator",
                        options=['All'] + sorted(annotations_df['annotator'].unique().tolist()),
                        key='view_annotator_select'
                    )
                with col2:
                    view_interaction = st.selectbox(
                        "Filter by Interaction ID",
                        options=['All'] + sorted(annotations_df['interaction_id'].unique().tolist()),
                        key='view_interaction_select'
                    )
                with col3:
                    view_status = st.selectbox(
                        "Filter by Status",
                        options=['All', 'Not Started', 'In Progress', 'Completed'],
                        key='view_status_select'
                    )
                
                # Apply filters
                view_df = annotations_df.copy()
                if view_annotator != 'All':
                    view_df = view_df[view_df['annotator'] == view_annotator]
                if view_interaction != 'All':
                    view_df = view_df[view_df['interaction_id'] == view_interaction]
                if view_status != 'All':
                    view_df = view_df[view_df['status'] == view_status]
                
                # Display annotations with status
                if not view_df.empty:
                    for _, row in view_df.iterrows():
                        status_class = f"status-{row.get('status', 'Not Started').lower().replace(' ', '-')}"
                        with st.expander(
                            f"Interaction: {row['interaction_id']} - "
                            f"Annotator: {row['annotator']} - "
                            f"Status: {row.get('status', 'Not Started')} - "
                            f"Last Updated: {row.get('last_updated', 'Not updated')}"
                        ):
                            # Display status badge
                            st.markdown(
                                f"""
                                <div class="status-badge {status_class}">
                                    {row.get('status', 'Not Started')}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
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

        with tabs[4]:  # Metrics Dashboard tab
            st.title("📈 Annotation Metrics Dashboard")
            render_metrics_dashboard(annotations_df)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

def get_field_definition(key):
    """Return the tooltip definition for a given field"""
    definitions = {
        # Call Details
        "call_id": {
            "title": "Call Identifier",
            "description": "Unique identifier for the call. Must follow format: numeric string (e.g., '12345')"
        },
        "call_date": {
            "title": "Call Date",
            "description": "Date when the call took place. Must be in YYYY-MM-DD format and not in the future"
        },
        "call_type": {
            "title": "Call Type",
            "description": "Category of the call (e.g., Initial Consultation, Follow-up, Complaint)"
        },
        
        # Client Profile
        "client_age": {
            "title": "Client Age",
            "description": "Current age of the client. Must be between 18-100 years"
        },
        "current_401k_balance": {
            "title": "Current 401(k) Balance",
            "description": "Current balance in client's 401(k) account. Must be a non-negative number"
        },
        "years_to_retirement": {
            "title": "Years to Retirement",
            "description": "Number of years until planned retirement. Must be a positive integer"
        },
        
        # Retirement Goals
        "retirement_goal_flag": {
            "title": "Retirement Goal Flag",
            "description": "Indicates if client has specific retirement goals (True/False)"
        },
        "retirement_goals": {
            "title": "Retirement Goals",
            "description": "List of specific retirement goals mentioned by the client"
        },
        "retirement_age": {
            "title": "Target Retirement Age",
            "description": "Client's target age for retirement. Must be greater than current age"
        },
        
        # Feedback Ratings
        "call_quality_rating": {
            "title": "Call Quality Rating",
            "description": "Overall quality of the call interaction and audio clarity"
        },
        "agent_performance_rating": {
            "title": "Agent Performance Rating",
            "description": "How well the agent handled the customer's needs and followed procedures"
        },
        "customer_satisfaction_rating": {
            "title": "Customer Satisfaction",
            "description": "Perceived level of customer satisfaction based on the interaction"
        },
        "resolution_effectiveness_rating": {
            "title": "Resolution Effectiveness",
            "description": "How effectively the customer's issue or inquiry was resolved"
        }
    }
    
    return definitions.get(key.lower(), {
        "title": key.replace('_', ' ').title(),
        "description": "Please validate this field according to the guidelines"
    })

def get_section_title(key):
    """Return a user-friendly section title"""
    sections = {
        "call_details": "Call Details",
        "client_profile": "Client Profile",
        "retirement_test": "Retirement Goals",
        "feedback_ratings": "Feedback"
    }
    return sections.get(key.lower(), key.replace('_', ' ').title())

def render_field(key, value, parent_key="", is_subsection=False):
    """Enhanced render_field function with validation controls and tooltips"""
    field_id = f"{parent_key}_{key}".strip('_')
    field_def = get_field_definition(key)
    
    # Get the display title for the field
    if parent_key and not parent_key.endswith(key):
        parent_section = get_section_title(parent_key.split('_')[-1] if '_' in parent_key else parent_key)
        display_title = f"{parent_section} - {key.replace('_', ' ').title()}"
    else:
        display_title = key.replace('_', ' ').title()
    
    if isinstance(value, (str, int, float)):
        with st.container():
            # Create label with tooltip using modern SVG icon and nested title styling
            parent_section = get_section_title(parent_key.split('_')[-1] if '_' in parent_key else parent_key)
            field_name = key.replace('_', ' ').title()
            
            st.markdown(
                f"""
                <div class="field-container nested-field">
                    <div class="nested-field-title">
                        {f'<span class="section-name">{parent_section}</span><span class="separator">›</span>' if parent_key else ''}
                        <span class="field-name">{field_name}</span>
                        <div class="tooltip-container">
                            <span style="display: inline-flex; align-items: center; justify-content: center;">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="12" cy="12" r="9" stroke="#64B5F6" stroke-width="1.5" stroke-opacity="0.8"/>
                                    <circle cx="12" cy="18" r="0.5" fill="#64B5F6" fill-opacity="0.8"/>
                                    <path d="M12 16V14.5811C12 13.6369 12.5286 12.7708 13.3691 12.3459C14.2095 11.921 14.7382 11.0548 14.7382 10.1107C14.7382 8.83643 13.7117 7.81 12.4375 7.81C11.1632 7.81 10.1368 8.83643 10.1368 10.1107" stroke="#64B5F6" stroke-width="1.5" stroke-opacity="0.8"/>
                                </svg>
                            </span>
                            <div class="tooltip-text">
                                <div class="tooltip-title">{field_def['title']}</div>
                                <div class="tooltip-description">{field_def['description']}</div>
                            </div>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            # Adjusted column widths: main content takes more space, checkboxes take less
            col1, col2, col3 = st.columns([3, 0.5, 0.5])
            with col1:
                input_value = st.text_area("", value, key=f"input_{field_id}", label_visibility="collapsed")
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
        
        # Get field definition for list
        field_def = get_field_definition(key)
        
        # Add tooltip for list field with combined title
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="color: #64B5F6; font-size: 0.9em;">{display_title}</span>
                <div class="tooltip-container" style="margin-left: 4px;">
                    <span style="display: inline-flex; align-items: center; justify-content: center;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="9" stroke="#64B5F6" stroke-width="1.5" stroke-opacity="0.8"/>
                            <circle cx="12" cy="18" r="0.5" fill="#64B5F6" fill-opacity="0.8"/>
                            <path d="M12 16V14.5811C12 13.6369 12.5286 12.7708 13.3691 12.3459C14.2095 11.921 14.7382 11.0548 14.7382 10.1107C14.7382 8.83643 13.7117 7.81 12.4375 7.81C11.1632 7.81 10.1368 8.83643 10.1368 10.1107" stroke="#64B5F6" stroke-width="1.5" stroke-opacity="0.8"/>
                        </svg>
                    </span>
                    <div class="tooltip-text">
                        <div class="tooltip-title">{field_def['title']}</div>
                        <div class="tooltip-description">{field_def['description']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Initialize session state for list items
        if f"list_items_{field_id}" not in st.session_state:
            st.session_state[f"list_items_{field_id}"] = value.copy()
        
        updated_list = []
        
        # Display existing items
        for i, item in enumerate(st.session_state[f"list_items_{field_id}"]):
            with st.container():
                col1, col2, col3 = st.columns([3, 0.5, 0.5])
                with col1:
                    if f"input_{field_id}_{i}" not in st.session_state:
                        st.session_state[f"input_{field_id}_{i}"] = item
                    
                    input_value = st.text_area(
                        f"Item {i + 1}", 
                        value=st.session_state[f"input_{field_id}_{i}"],
                        key=f"text_{field_id}_{i}"
                    )
                    
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
        
        new_item = st.text_input(
            "",
            key=f"new_item_input_{field_id}",
            placeholder="Enter new item...",
            label_visibility="collapsed"
        )
        
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