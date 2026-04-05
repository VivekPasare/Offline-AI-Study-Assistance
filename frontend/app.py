import streamlit as st
import requests
import json
import time

# Set Page Config
st.set_page_config(
    page_title="Offline AI Study Assistant",
    page_icon="🎓",
    layout="wide",
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "theme" not in st.session_state:
    st.session_state.theme = "dark" # Default to dark

# Load External CSS
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply Theme Class to App
theme_class = "dark-mode" if st.session_state.theme == "dark" else "light-mode"
st.markdown(f" <style>div.stApp {{ @extend .{theme_class}; }} </style> ", unsafe_allow_html=True)
# Direct injection for better reliability in Streamlit
st.markdown(f'<script>document.body.parentElement.className = "{theme_class}";</script>', unsafe_allow_html=True)
st.markdown(f"""
    <script>
        var body = window.parent.document.querySelector(".stApp");
        body.className = "stApp {theme_class}";
    </script>
""", unsafe_allow_html=True)

# --- Login Page ---
def show_login():
    st.markdown(
        """
        <div style="text-align: center; margin-top: 3rem;">
            <h1 style="font-size: 3rem; background: linear-gradient(to right, #818cf8, #34d399); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">
                Welcome Back
            </h1>
            <p style="color: #94a3b8; font-size: 1.2rem;">Sign in to your offline study space</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-container fade-in" style="margin-top: 1rem;">', unsafe_allow_html=True)
        
        # Social login as a Streamlit button with custom icon/text
        if st.button("🚀 Continue with Google", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_email = "google-student@gmail.com"
            st.rerun()
            
        st.markdown("<p style='text-align: center; color: #475569; margin: 1rem 0;'>──────── OR ────────</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="student@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.info("Please enter your credentials to continue.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login()
    st.stop()

# --- Main App (Internal) ---

# Define API URL
BACKEND_URL = "http://localhost:8000"

# --- Sidebar / Navigation ---
st.sidebar.markdown(
    f"""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 1.8rem; margin-bottom: 0;'>🎓 Offline Tutor</h1>
        <p style='color: #94a3b8;'>Welcome, {st.session_state.user_email.split('@')[0]}!</p>
    </div>
    <hr style='border-color: rgba(255,255,255,0.1);'>
    """, 
    unsafe_allow_html=True
)

st.sidebar.title("App Settings")

# Theme Toggle
current_theme = st.session_state.theme
theme_label = "🌙 Dark Mode" if current_theme == "dark" else "☀️ Light Mode"
if st.sidebar.button(f"Switch to {'Light' if current_theme == 'dark' else 'Dark'} Mode"):
    st.session_state.theme = "light" if current_theme == "dark" else "dark"
    st.rerun()

# Learning Mode Selection
learning_mode = st.sidebar.selectbox(
    "Select Learning Mode",
    ["Normal", "Simple", "Example"],
    help="Normal: Standard explanation\nSimple: Very easy (ELI10)\nExample: Focus on real-life applications"
)

# Language Selection
language = st.sidebar.radio(
    "Choose Language",
    ["English", "Hindi"],
    horizontal=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_chat():
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("Clear Conversation", type="primary", use_container_width=True):
    clear_chat()

# Info Box
st.sidebar.info(
    "Using local Gemma:2b with no internet required."
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🚪 Sign Out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    # Clear history on logout for privacy
    st.session_state.messages = []
    st.rerun()

# --- Main Dashboard ---

# Title Section
st.markdown(
    """
    <div class="header-container fade-in">
        <h1 class="title-text">Offline AI Study Assistant</h1>
        <p class="subtitle-text">Empowering students with smart learning, anywhere, anytime.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Tab Selection
main_tab, summary_tab = st.tabs(["💬 Personal Tutor Chat", "📝 Smart Summarizer"])

# --- Tab 1: Chat interface ---
with main_tab:
    # Display message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Add mode badge if it's the assistant's previous message
            if message["role"] == "assistant" and "mode" in message:
                mode_class = f"mode-{message['mode'].lower()}"
                st.markdown(f"<span class='mode-badge {mode_class}'>{message['mode']} Mode</span>", unsafe_allow_html=True)
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a doubt... (e.g. What is photosynthesis?)"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add to session history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process with AI
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.status(f"Thinking in {learning_mode} mode ({language})...", expanded=False) as status:
                try:
                    payload = {
                        "query": prompt,
                        "mode": learning_mode,
                        "language": language,
                        "history": st.session_state.messages[-4:-1] if len(st.session_state.messages) > 1 else []
                    }
                    
                    response = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        data = response.json()
                        full_response = data["answer"]
                        status.update(label="Response generated!", state="complete")
                    else:
                        st.error(f"Backend error: {response.text}")
                        status.update(label="Generation failed.", state="error")
                
                except requests.exceptions.ConnectionError:
                    st.error("Error: Could not connect to the Backend server. Ensure both FastAPI and Ollama are running.")
                    status.update(label="Server disconnected.", state="error")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    status.update(label="An error occurred.", state="error")

            # Final Display
            if full_response:
                mode_class = f"mode-{learning_mode.lower()}"
                st.markdown(f"<span class='mode-badge {mode_class}'>{learning_mode} Mode</span>", unsafe_allow_html=True)
                message_placeholder.markdown(full_response)
                # Store assistant response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response, 
                    "mode": learning_mode
                })

# --- Tab 2: Summarizer ---
with summary_tab:
    st.subheader("Convert long notes into bullet points")
    st.write("Perfect for exam revision or summarizing lengthy textbook chapters.")
    
    notes_text = st.text_area("Paste your study material here...", height=250)
    
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        summarize_btn = st.button("Generate Summary", type="primary", use_container_width=True)
    with col2:
        sum_lang = st.radio("Summary Language", ["English", "Hindi"], horizontal=True, key="sum_lang")
        
    if summarize_btn:
        if not notes_text.strip():
            st.warning("Please paste some text to summarize.")
        else:
            with st.spinner("Processing text..."):
                try:
                    payload = {"text": notes_text, "language": sum_lang}
                    response = requests.post(f"{BACKEND_URL}/summarize", json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        st.success("Summary Ready!")
                        st.markdown("### 📝 Study Summary")
                        st.info(response.json()["summary"])
                    else:
                        st.error("Error during summarization.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>
        Developed with ❤️ for Offline Education. Powered by Gemma 2b & Streamlit.
    </div>
    """, 
    unsafe_allow_html=True
)
