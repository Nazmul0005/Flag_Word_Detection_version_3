import streamlit as st
import requests
import json
import time
from io import BytesIO
import tempfile
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Voice Dating App - Content Moderation Demo",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #FF6B6B;
    text-align: center;
    margin-bottom: 2rem;
}
.demo-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.danger-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.info-box {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    color: #0c5460;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎤 Voice Dating App - AI Content Moderation</h1>', unsafe_allow_html=True)

# API Configuration
API_BASE_URL = st.sidebar.text_input("API Base URL", value="http://localhost:8000")

# Sidebar with demo information
st.sidebar.markdown("## 📋 Demo Information")
st.sidebar.markdown("""
**What this demo shows:**
- Upload voice messages
- Real-time transcription using OpenAI Whisper
- Content moderation using OpenAI Moderation API
- Clear allow/block recommendations

**Perfect for:**
- Voice dating apps
- Social audio platforms
- Content safety systems
""")

# Main demo section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="demo-section">', unsafe_allow_html=True)
    st.markdown("### 🎵 Upload Voice Message")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Upload a voice message to test content moderation"
    )
    
    # Demo files section
    st.markdown("#### 📁 Or try these demo scenarios:")
    demo_option = st.selectbox(
        "Select a demo scenario",
        ["None", "Clean Message", "Inappropriate Content", "Borderline Content"]
    )
    
    if demo_option != "None":
        st.info(f"Demo scenario: {demo_option}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="demo-section">', unsafe_allow_html=True)
    st.markdown("### ⚙️ API Configuration")
    
    # API endpoint selection
    endpoint = st.selectbox(
        "Select API Endpoint",
        ["/transcribe-and-moderate", "/transcribe", "/moderate"]
    )
    
    # Show API documentation
    if endpoint == "/transcribe-and-moderate":
        st.markdown("""
        **Main endpoint for voice dating apps**
        - Transcribes audio to text
        - Analyzes content for inappropriate material
        - Returns clear allow/block recommendation
        """)
    elif endpoint == "/transcribe":
        st.markdown("""
        **Transcription only**
        - Converts audio to text using OpenAI Whisper
        - No content moderation
        """)
    else:
        st.markdown("""
        **Text moderation only**
        - Requires text input
        - Analyzes for inappropriate content
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process button and results
if uploaded_file is not None or demo_option != "None":
    if st.button("🚀 Process Voice Message", type="primary"):
        with st.spinner("Processing voice message..."):
            start_time = time.time()
            
            try:
                if endpoint == "/transcribe-and-moderate":
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # Make API request
                    response = requests.post(f"{API_BASE_URL}{endpoint}", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        processing_time = time.time() - start_time
                        
                        # Display results
                        st.markdown("## 📊 Moderation Results")
                        
                        # Processing time
                        st.metric("Processing Time", f"{processing_time:.2f} seconds")
                        
                        # Recommendation
                        recommendation = result.get("recommendation", "unknown")
                        if recommendation == "allow":
                            st.markdown(f'<div class="success-box"><strong>✅ RECOMMENDATION: ALLOW</strong><br>This voice message is safe to deliver.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="danger-box"><strong>🚫 RECOMMENDATION: BLOCK</strong><br>This voice message contains inappropriate content.</div>', unsafe_allow_html=True)
                        
                        # Transcription
                        st.markdown("### 📝 Transcription")
                        st.text_area("Transcribed Text", result.get("transcription", ""), height=100)
                        
                        # Moderation details
                        moderation = result.get("moderation", {})
                        
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown("### 🔍 Moderation Analysis")
                            st.json({
                                "flagged": moderation.get("flagged", False),
                                "categories": moderation.get("categories", {}),
                            })
                        
                        with col2:
                            st.markdown("### 📈 Confidence Scores")
                            scores = moderation.get("category_scores", {})
                            for category, score in scores.items():
                                if score > 0.01:  # Only show relevant scores
                                    st.metric(category.replace("_", " ").title(), f"{score:.3f}")
                        
                        # Raw API response
                        with st.expander("🔧 Raw API Response"):
                            st.json(result)
                    
                    else:
                        st.error(f"API Error: {response.status_code} - {response.text}")
                
                elif endpoint == "/moderate":
                    # For text moderation, show text input
                    text_input = st.text_area("Enter text to moderate:", height=100)
                    if text_input:
                        response = requests.post(f"{API_BASE_URL}{endpoint}", params={"text": text_input})
                        if response.status_code == 200:
                            result = response.json()
                            st.json(result)
                        else:
                            st.error(f"API Error: {response.status_code}")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure your FastAPI server is running!")
                st.markdown("""
                **To start the API server:**
                ```bash
                uvicorn com.mhire.app.main:app --reload --host 0.0.0.0 --port 8000
                ```
                """)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Demo scenarios section
st.markdown("## 🎭 Demo Scenarios")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### ✅ Clean Content
    - Normal conversation
    - Compliments and positive messages
    - General dating chat
    
    **Expected Result:** ALLOW
    """)

with col2:
    st.markdown("""
    ### ⚠️ Borderline Content
    - Slightly suggestive language
    - Mild profanity
    - Context-dependent content
    
    **Expected Result:** May vary
    """)

with col3:
    st.markdown("""
    ### 🚫 Inappropriate Content
    - Explicit sexual content
    - Harassment or threats
    - Hate speech
    
    **Expected Result:** BLOCK
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
<p><strong>Voice Dating App - AI Content Moderation Demo</strong></p>
<p>Powered by OpenAI Whisper & Moderation APIs | Built with FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Health check in sidebar
st.sidebar.markdown("## 🏥 API Health Check")
if st.sidebar.button("Check API Status"):
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            st.sidebar.success("✅ API is healthy!")
            st.sidebar.json(response.json())
        else:
            st.sidebar.error("❌ API health check failed")
    except:
        st.sidebar.error("❌ Cannot reach API")