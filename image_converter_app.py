import streamlit as st
from PIL import Image, ImageOps
import zipfile
import io

# Page setup
st.title("📱 Mobile-Friendly Image Converter")
st.write("Upload images and convert them to mobile-friendly portrait format (680x1280)")

# Final portrait size that works well on all phones
TARGET_SIZE = (680, 1280)  # Width x Height

def resize_image_mobile_friendly(img):
    img = img.convert("RGB")
    width, height = img.size
    
    # 🔁 Rotate if landscape (so it fits portrait mode)
    if width > height:
        img = img.rotate(270, expand=True)
    
    # 🖼 Resize to fit within target portrait canvas
    smaller_target = (int(TARGET_SIZE[0] * 0.9), int(TARGET_SIZE[1] * 0.9))
    resized = ImageOps.contain(img, smaller_target)
    
    # 🧾 Create white background and center resized image
    background = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
    offset = ((TARGET_SIZE[0] - resized.width) // 2,
              (TARGET_SIZE[1] - resized.height) // 2)
    background.paste(resized, offset)
    
    return background

# File upload
uploaded_files = st.file_uploader(
    "Choose image files", 
    accept_multiple_files=True,
    type=['jpg', 'jpeg', 'png', 'webp']
)

if uploaded_files:
    st.write(f"📁 {len(uploaded_files)} files uploaded")
    
    if st.button("🔄 Convert Images"):
        with st.spinner("Converting images..."):
            # Create a zip file in memory
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_files:
                    # Process each image
                    img = Image.open(uploaded_file)
                    converted_img = resize_image_mobile_friendly(img)
                    
                    # Save to memory
                    img_buffer = io.BytesIO()
                    converted_img.save(img_buffer, "JPEG", quality=95)
                    
                    # Add to zip
                    filename = uploaded_file.name.rsplit(".", 1)[0] + ".jpg"
                    zip_file.writestr(filename, img_buffer.getvalue())
                    
                    st.success(f"✅ Converted: {filename}")
            
            # Download button
            st.download_button(
                label="📥 Download All Converted Images (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="mobile_friendly_images.zip",
                mime="application/zip"
            )
