import streamlit as st
from PIL import Image
from gradio_client import Client
import os

st.title("🧵 AI Virtual Try-On Studio")

fabric_file = st.file_uploader("Upload Fabric Pattern", type=["jpg", "png"])
model_file = st.file_uploader("Upload Client Photo", type=["jpg", "png"])

if st.button("✨ Generate Real AI Try-On"):
    if fabric_file and model_file:
        with st.spinner("Connecting to free public AI Try-On model on Hugging Face..."):
            try:
                # Save uploaded files temporarily
                with open("temp_fabric.jpg", "wb") as f:
                    f.write(fabric_file.getbuffer())
                with open("temp_model.jpg", "wb") as f:
                    f.write(model_file.getbuffer())

                # Connect to a public Hugging Face Virtual Try-On Space (e.g., IDM-VTON)
                client = Client("yisol/IDM-VTON")
                result = client.predict(
                    dict={"background": open("temp_model.jpg", "rb"), "layers": [], "composite": None},
                    garm_img=open("temp_fabric.jpg", "rb"),
                    garment_des="custom dress",
                    is_checked=True,
                    is_checked_crop=False,
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )

                # Display the resulting generated image
                generated_image = Image.open(result[0])
                st.image(generated_image, caption="AI Generated Try-On Result!")

            except Exception as e:
                st.error(f"Public server is busy or queue is full: {e}")
    else:
        st.warning("Please upload both fabric and client photos.")
