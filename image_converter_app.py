import streamlit as st
from PIL import Image, ImageOps
import zipfile
import io

# === SETTINGS ===
PORTRAIT_SIZE = (680, 1280)
AB_IMAGE_SIZE = (680, 640)
GRID_IMAGE_SIZE = (680, 640)

st.title("Mobile-Friendly Image Converter")
st.write("Choose to convert info images, ABCD-style stim images, or image grid sets into mobile-optimized format.")

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

# === MODE SELECT ===
mode = st.radio("Choose mode:", ["Info image", "ABCD images (multiple)", "Image grid (multiple images)"])

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
