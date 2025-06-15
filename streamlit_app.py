import streamlit as st
import requests
import base64
import os
import json

# --- Configuration ---
# By default, this will point to the local FastAPI server.
# If your FastAPI is deployed (e.g., on Vercel), update this URL.
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/query")

# --- Helper Functions ---
def image_to_base64(image_file):
    """Converts an uploaded image file to a base64 encoded string."""
    if image_file is not None:
        try:
            # Read file bytes
            bytes_data = image_file.getvalue()
            # Encode to base64
            base64_encoded_data = base64.b64encode(bytes_data).decode('utf-8')
            return base64_encoded_data
        except Exception as e:
            st.error(f"Error encoding image: {e}")
            return None
    return None

# --- Streamlit UI ---
st.set_page_config(layout="wide")

st.title("🎓 Virtual TA Chatbot")
st.markdown("Ask questions about your courses, and I'll do my best to answer based on the available knowledge base.")

# --- User Inputs ---
question = st.text_input("❓ Your Question:", placeholder="e.g., What are the prerequisites for course CS101?")
uploaded_image = st.file_uploader("🖼️ Upload an image (optional):", type=["png", "jpg", "jpeg"])

# Display the uploaded image if any
if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", width=300)

submit_button = st.button("💬 Get Answer")

# --- Process Query and Display Results ---
if submit_button:
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking... 🧠"):
            payload = {"question": question}

            if uploaded_image:
                image_b64 = image_to_base64(uploaded_image)
                if image_b64:
                    payload["image"] = image_b64

            try:
                st.info(f"Sending query to backend: {BACKEND_URL}")
                response = requests.post(BACKEND_URL, json=payload, timeout=120) # Increased timeout
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                result = response.json()

                st.subheader("💡 Answer:")
                st.markdown(result.get("answer", "No answer provided."))

                links = result.get("links", [])
                if links:
                    st.subheader("🔗 Sources:")
                    for link_info in links:
                        # Ensure link_info is a dictionary and has 'url' and 'text'
                        if isinstance(link_info, dict):
                            url = link_info.get('url', '#')
                            text = link_info.get('text', 'Source')
                            st.markdown(f"- [{text}]({url})")
                        else:
                            # Handle cases where link_info might not be a dict (e.g., just a URL string)
                            st.markdown(f"- [{link_info}]({link_info})")
                else:
                    st.markdown("No sources provided.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")
                st.error(f"Backend URL: {BACKEND_URL}")
                st.error("Please ensure the FastAPI backend (`app.py`) is running and accessible.")
                # Attempt to print more details from the error if available
                if e.response is not None:
                    try:
                        error_detail = e.response.json()
                        st.error(f"Backend error detail: {error_detail}")
                    except json.JSONDecodeError:
                        st.error(f"Backend response content: {e.response.text}")


            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
st.markdown("Powered by Streamlit and FastAPI")
