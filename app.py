import streamlit as st
from PIL import Image
from gradio_client import Client

# Page Configuration
st.set_page_config(
    page_title="Custom Indian & Western Dress Designer", 
    page_icon="🧵", 
    layout="centered"
)

# App Header
st.title("🧵 Custom Apparel & AI Virtual Try-On Studio")
st.write("Upload your fabric, select your outfit style, enter your metric measurements, and generate your custom AI try-on preview!")

# --- STEP 1: Uploads ---
st.header("1. Upload Assets")
col_up1, col_up2 = st.columns(2)

with col_up1:
    fabric_file = st.file_uploader("Upload Fabric Pattern (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if fabric_file is not None:
        fabric_image = Image.open(fabric_file)
        st.image(fabric_image, caption="Fabric Sample", width=150)

with col_up2:
    model_file = st.file_uploader("Upload Client / Avatar Photo", type=["jpg", "jpeg", "png"])
    if model_file is not None:
        model_image = Image.open(model_file)
        st.image(model_image, caption="Client Base Photo", width=150)

# --- STEP 2: Category & Style Selection ---
st.header("2. Choose Category & Garment Style")
target_gender = st.radio("Select Target Collection:", ["Women's Wear", "Men's Wear"], horizontal=True)

if target_gender == "Women's Wear":
    dress_style = st.selectbox(
        "Select Style:",
        ["Designer Blouse (Saree)", "Lehenga Choli Set", "Salwar Kameez Suit", "Anarkali Dress", "Western A-Line Midi"]
    )
else:
    dress_style = st.selectbox(
        "Select Shirt Style:",
        ["Classic Formal Shirt", "Casual Printed Shirt", "Mandarin Collar (Nehru) Shirt", "Festive Kurta Shirt"]
    )

# --- STEP 3: Body Measurements (in Meters) ---
st.header("3. Enter Your Measurements (in Meters)")
col1, col2, col3 = st.columns(3)

with col1:
    chest_bust = st.number_input("Chest / Bust (m)", min_value=0.5, max_value=2.0, value=0.90, step=0.01)
with col2:
    waist = st.number_input("Waist (m)", min_value=0.4, max_value=2.0, value=0.75, step=0.01)
with col3:
    length_req = st.number_input("Desired Length (m)", min_value=0.5, max_value=3.0, value=1.10, step=0.01)

# --- STEP 4: Generate Design Specification & AI Try-On ---
st.header("4. Generate Specification & AI Preview")

if st.button("✨ Run AI Try-On & Calculate Meterage", type="primary"):
    if fabric_file is None:
        st.warning("⚠️ Please upload a fabric pattern image in Step 1 first!")
    elif model_file is None:
        st.warning("⚠️ Please upload a client photo in Step 1 to generate the virtual try-on avatar!")
    else:
        with st.spinner(f"Connecting to AI pipeline to fit your {dress_style} onto the client avatar..."):
            try:
                # Save uploaded files temporarily as local paths
                temp_fabric_path = "temp_fabric.jpg"
                temp_model_path = "temp_model.jpg"
                
                with open(temp_fabric_path, "wb") as f:
                    f.write(fabric_file.getbuffer())
                with open(temp_model_path, "wb") as f:
                    f.write(model_file.getbuffer())
                
                # Connect to open-source Virtual Try-On model space using file path strings
                client = Client("yisol/IDM-VTON")
                result = client.predict(
                    dict={"background": temp_model_path, "layers": [], "composite": None},
                    garm_img=temp_fabric_path,
                    garment_des=f"A custom-tailored {dress_style} made for {target_gender}",
                    is_checked=True,
                    is_checked_crop=False,
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )
                
                ai_generated_img = Image.open(result[0])
                generation_success = True
            except Exception as e:
                generation_success = False
                error_message = str(e)

        # Display specifications summary
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.markdown(f"**Client Metrics:**")
            st.write(f"- **Chest/Bust:** {chest_bust} meters")
            st.write(f"- **Waist:** {waist} meters")
            st.write(f"- **Garment Length:** {length_req} meters")
        with sub_col2:
            st.markdown(f"**Tailoring Execution:**")
            st.write(f"- **Category:** {target_gender}")
            st.write(f"- **Outfit:** {dress_style}")
            
            # Dynamic fabric meter requirement logic
            if "Lehenga" in dress_style or "Anarkali" in dress_style:
                est_fabric = "3.5 to 5.0 meters"
            elif "Blouse" in dress_style:
                est_fabric = "0.8 to 1.2 meters"
            else:
                est_fabric = "2.2 to 2.8 meters"
                
            st.write(f"- **Total Fabric Required:** ~{est_fabric}")

        # Visual Output Display Area
        st.markdown("---")
        st.subheader("🖼️ AI-Generated Virtual Try-On Result")
        
        if generation_success:
            st.image(ai_generated_img, caption=f"AI Styled Avatar: {dress_style}", width=350)
            st.success("Successfully generated the virtual try-on mapping using your fabric pattern and garment style!")
        else:
            # Fallback display if public server queue is busy
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.image(model_image, caption="Original Client Reference", width=200)
            with res_col2:
                st.image(fabric_image, caption=f"Fabric Swatch for {dress_style}", width=200)
            st.warning(f"Public AI server queue is currently busy: {error_message}. Showing blueprint layout instead.")

        st.balloons()
