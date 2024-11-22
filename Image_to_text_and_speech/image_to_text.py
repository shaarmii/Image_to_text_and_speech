import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import io

# Set up API key
genai.configure(api_key="google_api_key")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Streamlit UI
st.title("Image to Text And Speech Generation")
st.subheader("Upload  the image!")

# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        img = Image.open(uploaded_file)
            # Prepare a prompt or text description for the image
        prompt = "Describe the content of this image without any symbols and if the image contains any text print those text and describe it.And in the image if there is any obstacle they it should alert the user first and then describe it where the obstacle is."  # You can modify this based on what you want to ask
        
        # Generate text based on the image and prompt
        response = model.generate_content([img, prompt])  # Pass both image and prompt to the model
        st.write(response.text)

        tts = gTTS(response.text, lang='en')
        
        # Save the speech to a file (in-memory)
        speech_file = "speech.mp3"  # Path to save the audio file
        tts.save(speech_file)
        
            # Display audio in Streamlit
        st.audio(speech_file, format="audio/mp3", start_time=0)

    # Inject JavaScript for autoplay
        # Inject JavaScript to autoplay the audio (works in some browsers)
        st.markdown(
        """
        <script>
        // Wait until the audio is ready, then play it
        var audio = document.querySelector('audio');
        if (audio) {
            audio.oncanplaythrough = function() {
                audio.play();  // Play once the audio is ready
            };
        }
        </script>
        """, 
        unsafe_allow_html=True
    )

