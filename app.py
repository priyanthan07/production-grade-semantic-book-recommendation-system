import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set page to wide layout for more space
st.set_page_config(layout="wide")

# ---------- Custom CSS for Glass Effect and Layout ----------
st.markdown(
    """
    <style>
    /* Glass container for sections */
    .glass-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
        position: relative;
    }
    /* Scrollable container for recommendations */
    .scroll-container {
        max-height: 400px;
        overflow-y: auto;
        margin-top: 10px;
    }
    /* Close button for the glass container */
    .close-btn {
        float: right;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        margin-top: -5px;
        margin-right: -5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Store search and recommendation data in session state
if "general_recs" not in st.session_state:
    st.session_state["general_recs"] = []
if "popular_recs" not in st.session_state:
    st.session_state["popular_recs"] = []
if "show_popular" not in st.session_state:
    st.session_state["show_popular"] = True

# ---------- Page Title ----------
st.title("Book Recommendation System")

# ---------- Layout: Left and Right Columns ----------
left_col, right_col = st.columns([1, 3], gap="large")

# ---------- Left Column: Search Controls ----------
with left_col:
    st.subheader("Enter a description of a book:")
    query = st.text_input("Book Description", placeholder="e.g., A story about forgiveness", label_visibility="hidden")
    
    st.subheader("Category")
    category = st.selectbox("Category", ["All", "Fiction", "Nonfiction"], label_visibility="visible")
    
    st.subheader("Tone")
    tone = st.selectbox("Tone", ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"], label_visibility="visible")
    
    if st.button("Search"):
        # Call your FastAPI general recommendation endpoint
        # Replace with your actual API URL, e.g., "http://localhost:8000/recommendation"
        payload = {"query": query, "category": category, "tone": tone}
        try:
            response = requests.post("http://localhost:8000/recommendations", json=payload)
            if response.status_code == 200:
                st.session_state["general_recs"] = response.json()  # list of [thumbnail_url, caption]
            else:
                st.error("Failed to retrieve general recommendations.")
        except Exception as e:
            st.error(f"Error calling recommendation API: {e}")

# ---------- Right Column: Two Glass Sections ----------
with right_col:
    # 1) Popular Recommendations Section (always visible unless closed)
    if st.session_state["show_popular"]:
        st.markdown('<div class="glass-container" id="popular-section">', unsafe_allow_html=True)
        st.markdown('<span class="close-btn" onClick="document.getElementById(\'popular-section\').style.display=\'none\';">'
                    '&times;</span>', unsafe_allow_html=True)
        st.subheader("Popular Recommendations")
        
        # Refresh button
        if st.button("Refresh Popular Recommendations"):
            try:
                pop_resp = requests.get("http://localhost:8000/popular_recommendations")
                if pop_resp.status_code == 200:
                    st.session_state["popular_recs"] = pop_resp.json()  # list of [thumbnail_url, caption]
                else:
                    st.error("Failed to retrieve popular recommendations.")
            except Exception as e:
                st.error(f"Error calling popular recommendation API: {e}")

        # Scrollable container for popular recs
        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        pop_cols = st.columns(4)
        for i, rec in enumerate(st.session_state["popular_recs"]):
            with pop_cols[i % 4]:
                try:
                    img_response = requests.get(rec[0])
                    img = Image.open(BytesIO(img_response.content))
                    st.image(img, use_container_width=True)
                except:
                    st.write("Image unavailable")
                st.caption(rec[1])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # end glass-container

    # 2) General Recommendations Section (only after user searches)
    if st.session_state["general_recs"]:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader("General Recommendations")
        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        gen_cols = st.columns(4)
        for i, rec in enumerate(st.session_state["general_recs"]):
            with gen_cols[i % 4]:
                try:
                    img_response = requests.get(rec[0])
                    img = Image.open(BytesIO(img_response.content))
                    st.image(img, use_container_width=True)
                except:
                    st.write("Image unavailable")
                st.caption(rec[1])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
