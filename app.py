# import streamlit as st
# import requests
# from PIL import Image
# from io import BytesIO

# # ---------- Custom CSS for Glass Effect -----------
# st.markdown(
#     """
#     <style>
#     /* Glass effect container */
#     .glass-card {
#         background: rgba(255, 255, 255, 0.2);
#         border-radius: 10px;
#         padding: 15px;
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
#         backdrop-filter: blur(8px);
#         -webkit-backdrop-filter: blur(8px);
#         border: 1px solid rgba(255, 255, 255, 0.18);
#         margin: 10px;
#     }
#     /* Scrollable container */
#     .scroll-container {
#         max-height: 600px;
#         overflow-y: auto;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ---------- Application Title ----------
# st.title("Book Recommendation System")

# # ---------- General Recommendation Section ----------
# st.header("General Recommendation")
# with st.container():
#     col_query, col_category, col_tone = st.columns([2, 1, 1])
    
#     query = st.text_input("Enter a description of a book:", placeholder="e.g., A story about forgiveness")
#     category = st.selectbox("Select a category:", options=["All", "Fiction", "Nonfiction"])
#     tone = st.selectbox("Select an emotional tone:", options=["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"])

#     if st.button("Find Recommendations"):
#         payload = {"query": query, "category": category, "tone": tone}
#         try:
#             # Replace with your FastAPI endpoint URL as needed
#             response = requests.post("http://localhost:8000/recommendation", json=payload)
#             if response.status_code == 200:
#                 recommendations = response.json()  # Expected to be a list of [thumbnail, caption] pairs
#                 st.markdown("### Recommendations")
#                 cols = st.columns(4)
#                 for i, rec in enumerate(recommendations):
#                     with cols[i % 4]:
#                         # Attempt to load image from URL
#                         try:
#                             img_response = requests.get(rec[0])
#                             img = Image.open(BytesIO(img_response.content))
#                             st.image(img, use_column_width=True)
#                         except Exception as e:
#                             st.write("Image unavailable")
#                         st.caption(rec[1])
#             else:
#                 st.error("Failed to retrieve recommendations.")
#         except Exception as e:
#             st.error(f"Error: {e}")

# # ---------- Popular Recommendation Section ----------
# st.header("Popular Recommendations")
# if st.button("Refresh Popular Recommendations"):
#     try:
#         # Replace with your FastAPI endpoint URL as needed
#         response_pop = requests.get("http://localhost:8000/popular_recommendation")
#         if response_pop.status_code == 200:
#             popular_recs = response_pop.json()  # Expected format similar to general recommendations
#             st.markdown("### Popular Recommendations")
#             # Use a scrollable container for popular recommendations
#             with st.container():
#                 st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
#                 cols = st.columns(4)
#                 for i, rec in enumerate(popular_recs):
#                     with cols[i % 4]:
#                         try:
#                             img_response = requests.get(rec[0])
#                             img = Image.open(BytesIO(img_response.content))
#                             st.image(img, use_column_width=True)
#                         except Exception as e:
#                             st.write("Image unavailable")
#                         st.caption(rec[1])
#                 st.markdown("</div>", unsafe_allow_html=True)
#         else:
#             st.error("Failed to retrieve popular recommendations.")
#     except Exception as e:
#         st.error(f"Error: {e}")

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
    query = st.text_input("", placeholder="e.g., A story about forgiveness")
    
    st.subheader("Category")
    category = st.selectbox("", ["All", "Fiction", "Nonfiction"])
    
    st.subheader("Tone")
    tone = st.selectbox("", ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"])
    
    if st.button("Search"):
        # Call your FastAPI general recommendation endpoint
        # Replace with your actual API URL, e.g., "http://localhost:8000/recommendation"
        payload = {"query": query, "category": category, "tone": tone}
        try:
            response = requests.post("http://localhost:8000/recommendation", json=payload)
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
                pop_resp = requests.get("http://localhost:8000/popular_recommendation")
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
                    st.image(img, use_column_width=True)
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
                    st.image(img, use_column_width=True)
                except:
                    st.write("Image unavailable")
                st.caption(rec[1])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
