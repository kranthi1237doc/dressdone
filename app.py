import streamlit as st
from PIL import Image, ImageOps
import time

# Page Configuration
st.set_page_config(
    page_title="Custom Indian & Western Dress Designer", 
    page_icon="🧵", 
    layout="centered"
)

# App Header
st.title("🧵 Custom Apparel & Design Studio")
st.write("Upload your fabric, choose your outfit style, input metric measurements, and preview your custom design!")

# --- STEP 1: Uploads ---
st.header("1. Upload Assets")
col_up1, col_up2 = st.columns(2)

with col_up1:
    fabric_file = st.file_uploader("Upload Fabric Pattern (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if fabric_file is not None:
        fabric_image = Image.open(fabric_file)
        st.image(fabric_image, caption="Fabric Sample", width=150)

with col_up2:
    model_file = st.file_uploader("Upload Client / Base Photo", type=["jpg", "jpeg", "png"])
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

# --- STEP 4: Generate Design & Meter Calculation ---
st.header("4. Generate Design Specification")

if st.button("✨ Calculate & Generate Design", type="primary"):
    if fabric_file is None:
        st.warning("⚠️ Please upload a fabric pattern image in Step 1 first!")
    else:
        with st.spinner("Analyzing fabric texture and computing metric blueprint..."):
            time.sleep(1.5) # Simulated smooth processing time
            st.success("🎉 Design blueprint successfully compiled!")

        # Display specifications summary
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.markdown(f"**Client Metrics:**")
            st.write(f"- **Chest/Bust:** {chest_bust} meters")
            st.write(f"- **Waist:** {waist} meters")
            st.write(f"- **Garment Length:** {length_req} meters")
        with sub_col2:
            st.markdown(f"**Tailoring Execution:**")
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
        st.subheader("🖼️ Project Layout Preview")
        
        # Show side-by-side comparison of Fabric and Client Photo if available
        if model_file is not None:
            prev_col1, prev_col2 = st.columns(2)
            with prev_col1:
                st.image(fabric_image, caption="Source Fabric", width=200)
            with prev_col2:
                st.image(model_image, caption=f"Target: {dress_style}", width=200)
            st.info("💡 **Prototype Note:** This layout pairs your fabric swatch with your client specifications and calculates exact meterage requirements for local tailoring.")
        else:
            st.image(fabric_image, caption=f"Fabric Swatch for {dress_style}", width=250)
            st.info("💡 Tip: Upload a client photo above to see the side-by-side design layout.")
            
        st.balloons()
