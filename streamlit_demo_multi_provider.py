import streamlit as st
import requests
import json
import time
from io import BytesIO
import tempfile
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Voice Dating App - Multi-Provider Content Moderation Demo",
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
.provider-card {
    background-color: #ffffff;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.provider-selected {
    border-color: #007bff;
    background-color: #f8f9ff;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎤 Voice Dating App - Multi-Provider AI Content Moderation</h1>', unsafe_allow_html=True)

# API Configuration
API_BASE_URL = st.sidebar.text_input("API Base URL", value="http://localhost:8000")

# Provider selection in sidebar
st.sidebar.markdown("## 🔧 Provider Selection")

# Provider information
providers_info = {
    "OpenAI Whisper": {
        "description": "Industry standard, reliable transcription",
        "speed": "Medium (2-5 seconds)",
        "accuracy": "High (10.6% WER)",
        "cost": "$0.006/min",
        "features": ["Multilingual", "Robust", "Widely used"]
    },
    "Deepgram Nova-2": {
        "description": "Fastest, most accurate transcription",
        "speed": "Very Fast (<300ms streaming)",
        "accuracy": "Highest (8.4% WER)",
        "cost": "$0.0043/min",
        "features": ["Real-time streaming", "Speaker diarization", "36% better than Whisper"]
    },
    "Groq Whisper Turbo": {
        "description": "Ultra-fast processing, cost-effective",
        "speed": "Fastest (252x speed factor)",
        "accuracy": "Good (12% WER)",
        "cost": "$0.00067/min",
        "features": ["Lightning fast", "Very cheap", "Good for high volume"]
    }
}

selected_provider = st.sidebar.selectbox(
    "Choose Transcription Provider",
    list(providers_info.keys()),
    help="Select which AI provider to use for transcription"
)

# Display provider information
st.sidebar.markdown(f"### 📊 {selected_provider} Details")
provider_info = providers_info[selected_provider]
st.sidebar.markdown(f"**Description:** {provider_info['description']}")
st.sidebar.markdown(f"**Speed:** {provider_info['speed']}")
st.sidebar.markdown(f"**Accuracy:** {provider_info['accuracy']}")
st.sidebar.markdown(f"**Cost:** {provider_info['cost']}")
st.sidebar.markdown("**Features:**")
for feature in provider_info['features']:
    st.sidebar.markdown(f"• {feature}")

# Provider comparison section
st.markdown("## 🔍 Provider Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    card_class = "provider-card provider-selected" if selected_provider == "OpenAI Whisper" else "provider-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown("### 🤖 OpenAI Whisper")
    st.markdown("**Industry Standard**")
    st.metric("Speed", "Medium", "2-5s")
    st.metric("Accuracy", "High", "10.6% WER")
    st.metric("Cost", "$0.006/min", "")
    st.markdown("✅ Reliable & Robust")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    card_class = "provider-card provider-selected" if selected_provider == "Deepgram Nova-2" else "provider-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown("### ⚡ Deepgram Nova-2")
    st.markdown("**Best Performance**")
    st.metric("Speed", "Very Fast", "<300ms")
    st.metric("Accuracy", "Highest", "8.4% WER")
    st.metric("Cost", "$0.0043/min", "-28%")
    st.markdown("🏆 36% Better than Whisper")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    card_class = "provider-card provider-selected" if selected_provider == "Groq Whisper Turbo" else "provider-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown("### 🚀 Groq Whisper Turbo")
    st.markdown("**Ultra Fast & Cheap**")
    st.metric("Speed", "Fastest", "252x factor")
    st.metric("Accuracy", "Good", "12% WER")
    st.metric("Cost", "$0.00067/min", "-89%")
    st.markdown("💰 Most Cost Effective")
    st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Show selected provider info
    st.markdown(f"**Selected Provider:** {selected_provider}")
    st.markdown(f"**Expected Performance:** {provider_info['speed']}")
    st.markdown(f"**Expected Accuracy:** {provider_info['accuracy']}")
    
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
        - Converts audio to text
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
        with st.spinner(f"Processing voice message with {selected_provider}..."):
            start_time = time.time()
            
            try:
                if endpoint == "/transcribe-and-moderate":
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # Add provider selection to the request
                    data = {"provider": selected_provider.lower().replace(" ", "_")}
                    
                    # Make API request
                    response = requests.post(f"{API_BASE_URL}{endpoint}", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        processing_time = time.time() - start_time
                        
                        # Display results
                        st.markdown("## 📊 Moderation Results")
                        
                        # Provider and processing time
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Provider Used", selected_provider)
                        with col2:
                            st.metric("Processing Time", f"{processing_time:.2f}s")
                        with col3:
                            expected_range = {
                                "OpenAI Whisper": "2-5s",
                                "Deepgram Nova-2": "<1s",
                                "Groq Whisper Turbo": "<1s"
                            }
                            st.metric("Expected Range", expected_range[selected_provider])
                        
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
                        
                        # Performance comparison
                        st.markdown("### ⚡ Performance Analysis")
                        performance_data = {
                            "Provider": selected_provider,
                            "Processing Time": f"{processing_time:.2f}s",
                            "Expected Accuracy": provider_info['accuracy'],
                            "Cost per Minute": provider_info['cost'],
                            "Recommendation": recommendation.upper()
                        }
                        st.json(performance_data)
                        
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

# Performance comparison section
st.markdown("## 📈 Performance Comparison")

comparison_data = {
    "Provider": ["OpenAI Whisper", "Deepgram Nova-2", "Groq Whisper Turbo"],
    "Speed": ["Medium (2-5s)", "Very Fast (<300ms)", "Fastest (252x)"],
    "Accuracy (WER)": ["10.6%", "8.4%", "12%"],
    "Cost per Minute": ["$0.006", "$0.0043", "$0.00067"],
    "Best For": ["Reliability", "Performance", "Cost & Speed"]
}

st.table(comparison_data)

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
<p><strong>Voice Dating App - Multi-Provider AI Content Moderation Demo</strong></p>
<p>Powered by OpenAI Whisper, Deepgram Nova-2 & Groq Whisper Turbo | Built with FastAPI & Streamlit</p>
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

# Provider setup instructions
st.sidebar.markdown("## 🔑 Setup Instructions")
st.sidebar.markdown("""
**Required API Keys in .env file:**
```
openai_api_key=your_openai_key
deepgram_api_key=your_deepgram_key
groq_api_key=your_groq_key
```

**Free Trial Links:**
- [Deepgram: $200 free](https://console.deepgram.com/signup)
- [Groq: Free tier](https://console.groq.com/)
- [OpenAI: $5 free](https://platform.openai.com/)
""")