import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set up Streamlit Page configuration
st.set_page_config(page_title="TrendHook: AI Caption Generator", page_icon="🚀", layout="centered")

# App Header Styling
st.markdown("<h1 style='text-align: center;'>🚀 TrendHook AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate viral captions tailored for LinkedIn, X (Twitter), or Instagram entirely for free.</p>", unsafe_allow_html=True)
st.write("---")

# 1. API Configuration Setup
# To keep it secure and free, users can supply their own Google AI Studio API key.
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password", help="Get a free key from Google AI Studio")
st.sidebar.markdown("[Get a Free Gemini API Key here](https://aistudio.google.com/)")

if not api_key:
    st.info("💡 Please enter your free Gemini API Key in the sidebar to get started!", icon="🔑")
else:
    # Initialize the Google Gemini API Client
    genai.configure(api_key=api_key)
    
    # 2. UI Inputs
    platform = st.selectbox("Select Target Social Media Platform", ["LinkedIn", "X (Twitter)", "Instagram"])
    
    tone = st.select_slider(
        "Select Tone of Voice",
        options=["Casual/Witty", "Professional/Thought Leader", "Hype/Energetic", "Storytelling/Raw"]
    )
    
    additional_context = st.text_area(
        "What is this post about? (Optional Context)", 
        placeholder="e.g., I just completed my cloud certification, or Here is a sneak peek of my new open-source tool..."
    )
    
    uploaded_file = st.file_uploader("Upload Media (Screenshot, Certificate, or Graphic)", type=["png", "jpg", "jpeg"])
    
    # Preview uploaded image if exists
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image Preview", use_container_width=True)
    
    # 3. Generate Action
    if st.button("✨ Generate Mind-Blowing Captions"):
        with st.spinner("Analyzing data, checking trends, and crafting hooks..."):
            try:
                # Initialize Gemini 2.5 Flash (Generous free tier with vision + search capabilities)
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    generation_config={"temperature": 0.7}
                )
                
                # Constructing a comprehensive system-level prompt for algorithm optimization
                prompt_content = f"""
                You are a world-class social media copywriter and growth hacker specializing in the {platform} algorithm.
                Your task is to write 3 distinct, highly engaging caption options that maximize click-through rate, watch-time/read-time, and engagement (comments and shares) based on contemporary algorithmic triggers.
                
                Platform constraints:
                - Target Platform: {platform}
                - Selected Tone: {tone}
                - User Context: {additional_context if additional_context else 'No additional context provided.'}
                
                Instructions:
                1. If an image is provided alongside this text, act as an OCR and analytical engine. Carefully read any certificates, code snippets, project UI elements, or text within the image. Incorporate details (credentials, names, dates, stats) seamlessly into the narrative.
                2. Use modern viral structures: strong, polarizing, or curiosity-inducing hooks (first 1-2 lines before the "see more" cutoff), white space for readability, and a psychological Call to Action (CTA).
                3. Keep it relatable, human-like, and devoid of cliché AI jargon (like "In today's fast-paced digital world" or "Delve").
                
                Format your output clearly with 'Option 1', 'Option 2', and 'Option 3', breaking down why each option is engineered to work well with the current algorithm.
                """
                
                # Combine Image and Text inputs for Multimodal processing
                if uploaded_file is not None:
                    # Pass both the PIL Image object and the text prompt instructions
                    response = model.generate_content([image, prompt_content])
                else:
                    response = model.generate_content(prompt_content)
                
                # Render the generated responses neatly
                st.success("🎉 Captions generated successfully!")
                st.markdown("### Your Custom Hook Variations")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.warning("Please verify your API key is correct and you haven't exceeded the free tier rate limits.")