import streamlit as st
from PIL import Image, ImageOps
import zipfile
import io

# === SETTINGS ===
PORTRAIT_SIZE = (680, 1280)
AB_IMAGE_SIZE = (680, 640)
GRID_IMAGE_SIZE = (680, 640)
MOBILE_SAFE_CANVAS = (600, 1136)  # Safe for mobile view

st.title("Mobile-Friendly Image Converter")
st.write("Choose to convert info images, ABCD-style stim images, image grid sets, image highlights, or mobile-safe images into mobile-optimized format.")

# === RESIZE INFO IMAGE ===
def resize_info_image(img):
    img = img.convert("RGB")
    if img.width > img.height:
        img = img.rotate(270, expand=True)
    resized = ImageOps.contain(img, (int(PORTRAIT_SIZE[0] * 0.9), int(PORTRAIT_SIZE[1] * 0.9)))
    background = Image.new("RGB", PORTRAIT_SIZE, (255, 255, 255))
    offset = ((PORTRAIT_SIZE[0] - resized.width) // 2, (PORTRAIT_SIZE[1] - resized.height) // 2)
    background.paste(resized, offset)
    return background

# === RESIZE IMAGE HIGHLIGHT ===
def resize_highlight_image(img):
    img = img.convert("RGB")
    # No rotation - keep original orientation
    # Use smaller scale factor for landscape images to add more padding
    if img.width > img.height:
        # Landscape image - use more padding to prevent cutoff
        scale_factor = 0.75
    else:
        # Portrait image - standard padding
        scale_factor = 0.9
    
    target_size = (int(PORTRAIT_SIZE[0] * scale_factor), int(PORTRAIT_SIZE[1] * scale_factor))
    resized = ImageOps.contain(img, target_size)
    background = Image.new("RGB", PORTRAIT_SIZE, (255, 255, 255))
    offset = ((PORTRAIT_SIZE[0] - resized.width) // 2, (PORTRAIT_SIZE[1] - resized.height) // 2)
    background.paste(resized, offset)
    return background

# === RESIZE A/B/C/D IMAGE (MULTIPLE UPLOADS) ===
def resize_ab_image(img):
    img = img.convert("RGB")
    scale_factor = 0.9
    target_size = (int(AB_IMAGE_SIZE[0] * scale_factor), int(AB_IMAGE_SIZE[1] * scale_factor))
    resized = ImageOps.contain(img, target_size)
    background = Image.new("RGB", AB_IMAGE_SIZE, (255, 255, 255))
    offset = ((AB_IMAGE_SIZE[0] - resized.width) // 2, (AB_IMAGE_SIZE[1] - resized.height) // 2)
    background.paste(resized, offset)
    return background

# === RESIZE GRID IMAGE ===
def resize_grid_image(img):
    img = img.convert("RGB")
    scale_factor = 0.85
    target_size = (int(GRID_IMAGE_SIZE[0] * scale_factor), int(GRID_IMAGE_SIZE[1] * scale_factor))
    resized = ImageOps.contain(img, target_size)
    background = Image.new("RGB", GRID_IMAGE_SIZE, (255, 255, 255))
    offset = ((GRID_IMAGE_SIZE[0] - resized.width) // 2, (GRID_IMAGE_SIZE[1] - resized.height) // 2)
    background.paste(resized, offset)
    return background

# === RESIZE MOBILE-SAFE IMAGE ===
def resize_mobile_safe(img):
    img = img.convert("RGB")
    scale_factor = 0.9
    target_size = (int(MOBILE_SAFE_CANVAS[0] * scale_factor), int(MOBILE_SAFE_CANVAS[1] * scale_factor))
    resized = ImageOps.contain(img, target_size)
    background = Image.new("RGB", MOBILE_SAFE_CANVAS, (255, 255, 255))
    offset = ((MOBILE_SAFE_CANVAS[0] - resized.width) // 2,
              (MOBILE_SAFE_CANVAS[1] - resized.height) // 2)
    background.paste(resized, offset)
    return background

# === MODE SELECT ===
mode = st.radio("Choose mode:", [
    "Info image", 
    "Image highlight", 
    "ABCD images (multiple)", 
    "Image grid (multiple images)",
    "Mobile-safe images"
])

if mode == "Info image":
    uploaded_files = st.file_uploader("Upload image files", accept_multiple_files=True, type=['jpg', 'jpeg', 'png', 'webp'])
    if uploaded_files and st.button("Convert Info Images"):
        with st.spinner("Converting..."):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_files:
                    img = Image.open(uploaded_file)
                    converted = resize_info_image(img)
                    img_buffer = io.BytesIO()
                    converted.save(img_buffer, "JPEG", quality=95)
                    zip_file.writestr(f"{uploaded_file.name.rsplit('.', 1)[0]}_info.jpg", img_buffer.getvalue())
            st.download_button(
                "Download Converted Info Images (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="info_images.zip",
                mime="application/zip"
            )

elif mode == "Image highlight":
    uploaded_highlight_files = st.file_uploader(
        "Upload image highlight files (landscape images get extra padding)",
        accept_multiple_files=True,
        type=['jpg', 'jpeg', 'png', 'webp'],
        key="highlight"
    )
    if uploaded_highlight_files and st.button("Convert Image Highlights"):
        with st.spinner("Converting..."):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_highlight_files:
                    img = Image.open(uploaded_file)
                    converted = resize_highlight_image(img)
                    img_buffer = io.BytesIO()
                    converted.save(img_buffer, "JPEG", quality=95)
                    zip_file.writestr(f"{uploaded_file.name.rsplit('.', 1)[0]}_highlight.jpg", img_buffer.getvalue())
            st.download_button(
                "Download Image Highlights (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="highlight_images.zip",
                mime="application/zip"
            )

elif mode == "ABCD images (multiple)":
    uploaded_abcd_files = st.file_uploader(
        "Upload one or more ABCD images (each resized separately)",
        accept_multiple_files=True,
        type=['jpg', 'jpeg', 'png', 'webp'],
        key="abcd_multi"
    )

    if uploaded_abcd_files and st.button("Convert ABCD Images"):
        with st.spinner("Converting..."):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_abcd_files:
                    img = Image.open(uploaded_file)
                    converted = resize_ab_image(img)
                    img_buffer = io.BytesIO()
                    converted.save(img_buffer, "JPEG", quality=95)
                    filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_abcd.jpg"
                    zip_file.writestr(filename, img_buffer.getvalue())
            st.download_button(
                "Download ABCD Images (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="abcd_images.zip",
                mime="application/zip"
            )

elif mode == "Image grid (multiple images)":
    uploaded_grid_files = st.file_uploader(
        "Upload multiple images for grid layout (each will be resized individually)",
        accept_multiple_files=True,
        type=['jpg', 'jpeg', 'png', 'webp'],
        key="grid"
    )

    if uploaded_grid_files and st.button("Convert Grid Images"):
        with st.spinner("Converting..."):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_grid_files:
                    img = Image.open(uploaded_file)
                    converted = resize_grid_image(img)
                    img_buffer = io.BytesIO()
                    converted.save(img_buffer, "JPEG", quality=95)
                    zip_file.writestr(f"{uploaded_file.name.rsplit('.', 1)[0]}_grid.jpg", img_buffer.getvalue())
            st.download_button(
                "Download Grid Images (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="grid_images.zip",
                mime="application/zip"
            )

elif mode == "Mobile-safe images":
    uploaded_mobile_files = st.file_uploader(
        "Upload image(s) for mobile-safe conversion (600x1136 canvas)",
        accept_multiple_files=True,
        type=['jpg', 'jpeg', 'png', 'webp'],
        key="mobile_safe"
    )
    
    if uploaded_mobile_files and st.button("Convert Mobile-Safe Images"):
        with st.spinner("Converting..."):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in uploaded_mobile_files:
                    img = Image.open(uploaded_file)
                    converted = resize_mobile_safe(img)
                    img_buffer = io.BytesIO()
                    converted.save(img_buffer, "JPEG", quality=95)
                    filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_anon_web.jpg"
                    zip_file.writestr(filename, img_buffer.getvalue())
            st.download_button(
                "Download Mobile-Safe Images (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="Anon_Web_Images.zip",
                mime="application/zip"
            )
