import os
import streamlit as st
import requests
import json

from dotenv import load_dotenv
load_dotenv()


# Configure the page
st.set_page_config(
    page_title="RAGfolio",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the deploy button and other Streamlit elements
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Backend API configuration
BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    print("backend url not found!")
    st.stop()

def estimate_tokens(text):
    """Estimate token count - roughly 4 characters per token"""
    return len(text.split())

def validate_token_limit(text, max_tokens=50):
    """Check if text exceeds token limit"""

    token_count = estimate_tokens(text)
    return token_count <= max_tokens, token_count

def query_backend(question):
    """Send query to backend and return response"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/rag_query",
            json={"user_query": question},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["ai_response"]
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to backend server. Please ensure the backend is running on localhost:8000"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid response from backend"}

# App title and description
st.title("RAGfolio")
st.markdown("## Hi, I'm Nishant 👋 — curious about me? Ask my AI buddy, it knows almost everything 😉")
st.markdown("---")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Predefined questions
st.subheader("💡 Common Questions")

# Create columns for the predefined questions
col1, col2 = st.columns(2)

with col1:
    if st.button("📋 What are the key skills and qualifications?", use_container_width=True):
        question = "What are the key skills and qualifications?"
        st.session_state.current_query = question
        
    if st.button("🎯 What projects or achievements stand out?", use_container_width=True):
        question = "What projects or achievements stand out?"
        st.session_state.current_query = question

with col2:
    if st.button("💼 What is the work experience summary?", use_container_width=True):
        question = "Can you provide a summary of the work experience?"
        st.session_state.current_query = question
        
    if st.button("🎓 What is the educational background?", use_container_width=True):
        question = "What is the educational background?"
        st.session_state.current_query = question

st.markdown("---")

# Manual query input
st.subheader("✍️ Ask Your Own Question")

# Add token limit information
st.info("💡 **Token Limit:** Please keep your questions under 50 tokens (approximately 50 words) for optimal processing.")

user_query = st.text_input(
    "Enter your question:",
    placeholder="Type your question about the resume here...",
    key="manual_query"
)

# Real-time token counter
if user_query:
    is_valid, token_count = validate_token_limit(user_query)
    
    if is_valid:
        st.success(f"✅ Token count: {token_count}/50")
    else:
        st.error(f"❌ Token count: {token_count}/50 - Please rephrase your question in smaller chunks!")

# Submit button for manual query
if st.button("🔍 Ask Question", type="primary", use_container_width=True):
    if user_query.strip():
        is_valid, token_count = validate_token_limit(user_query.strip())
        
        if not is_valid:
            st.error(f"❌ **Question too long!** Your question contains {token_count} tokens, but the limit is 50 tokens. Please rephrase your question in smaller chunks.")
        else:
            st.session_state.current_query = user_query.strip()

# Process the query if one exists
if 'current_query' in st.session_state and st.session_state.current_query:
    query = st.session_state.current_query
    
    # Display the question
    st.markdown("---")
    st.subheader("❓ Question:")
    st.write(query)
    
    # Show loading spinner while processing
    with st.spinner("🤔 Analyzing resume..."):
        response = query_backend(query)
    
    # Display the response
    st.subheader("💬 Answer:")
    
    if "error" in response:
        st.error(f"❌ {response['error']}")
    else:
        # Assuming the backend returns a response with an 'answer' field
        # Adjust this based on your actual backend response format
        if isinstance(response, dict):
            answer = response.get('answer', response.get('response', str(response)))
        else:
            answer = str(response)
        
        st.success("✅ Response received!")
        st.write(answer)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'question': query,
            'answer': answer
        })
    
    # Clear the current query
    del st.session_state.current_query

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("📚 Chat History")
    
    # Add a button to clear history
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Display history in reverse order (most recent first)
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Q{len(st.session_state.chat_history)-i}: {chat['question'][:50]}..."):
            st.write("**Question:**")
            st.write(chat['question'])
            st.write("**Answer:**")
            st.write(chat['answer'])

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        RAGfolio - AI-powered resume
    </div>
    """, 
    unsafe_allow_html=True
)

# Add some custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        height: 3em;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    
    .stExpander {
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)
