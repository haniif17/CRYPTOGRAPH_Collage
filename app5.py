import streamlit as st
import base64
import random
import string
from io import BytesIO


# Caesar Cipher 

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# OTP (OneTapPad)
def generate_otp_key(length):
    return bytes([random.randint(0, 255) for _ in range(length)])

def otp_encrypt(data, key):
    return bytes([b ^ k for b, k in zip(data, key)])


st.set_page_config(page_title="Project UTS | Daffa Syahdana", layout="centered")
st.title("Kriptografi Dua Algoritma (OTP + Caesar Cipher)")
st.caption("Project by Muhammad Daffa Syahdana Haniif | A11.2023.15284")

if 'cipher_data' not in st.session_state:
    st.session_state['cipher_data'] = None
if 'key_data' not in st.session_state:
    st.session_state['key_data'] = None


def clear_download_state():
    st.session_state['cipher_data'] = None
    st.session_state['key_data'] = None

mode = st.radio("Pilih Mode Operasi:", ["Enkripsi", "Dekripsi"])


# ENKRIPSI 
if mode == "Enkripsi":
    
    uploaded_file = st.file_uploader(
        "Upload file video (format .mp4)", 
        type=["mp4"],
        on_change=clear_download_state
    )
    use_caesar = st.checkbox("Gunakan Caesar Cipher untuk kunci?", value=False)
    shift = st.slider("Geser Caesar Cipher (shift)", 1, 25, 3)

    if uploaded_file:
        st.video(uploaded_file)

        if st.button("🔒 Enkripsi Sekarang"):
            with st.spinner("Mengenkripsi file..."):
                data = uploaded_file.read()
                key = generate_otp_key(len(data))
                cipher = otp_encrypt(data, key)

                
                key_b64 = base64.b64encode(key).decode("utf-8")
                if use_caesar:
                    key_b64 = caesar_encrypt(key_b64, shift)

                
                st.session_state['cipher_data'] = cipher
                st.session_state['key_data'] = key_b64.encode("utf-8")
                
                st.success("✅ Enkripsi Berhasil! Silakan unduh kedua file di bawah.")

    
    if st.session_state['cipher_data'] is not None:
        st.download_button(
            "Download Cipher (.bin)",
            data=st.session_state['cipher_data'],  # Ambil data dari state
            file_name="cipher.bin",
            mime="application/octet-stream"
        )
        st.download_button(
            "Download Key (.bin)",
            data=st.session_state['key_data'],  # Ambil data dari state
            file_name="key.bin",
            mime="application/octet-stream"
        )


# DEKRIPSI 
else:
    cipher_file = st.file_uploader("Upload cipher file (.bin)", type=["bin"])
    key_file = st.file_uploader("Upload key file (.bin)", type=["bin"])
    use_caesar = st.checkbox("Key menggunakan Caesar Cipher?", value=False)
    shift = st.slider("Geser Caesar Cipher (shift)", 1, 25, 3)

    if cipher_file and key_file:
        if st.button("🔓 Dekripsi Sekarang"):
            cipher = cipher_file.read()
            key_text = key_file.read().decode("utf-8")

            if use_caesar:
                key_text = caesar_decrypt(key_text, shift)

            try:
                key = base64.b64decode(key_text)
            except Exception as e:
                st.error("Gagal decode base64 dari key! Pastikan key benar.")
                st.stop()

            if len(cipher) != len(key):
                st.error("Panjang cipher dan key tidak sama!")
                st.stop()

            plain = otp_encrypt(cipher, key)

            st.success("✅ Dekripsi Berhasil!")

            st.download_button(
                "Download Video Hasil (.mp4)",
                data=plain,
                file_name="decrypted_video.mp4",
                mime="video/mp4"
            )

            try:
                st.video(BytesIO(plain))
            except Exception:
                st.warning("File sudah didekripsi tapi tidak bisa diputar di browser. Coba download dan buka manual.")