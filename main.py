import streamlit as st
import qrcode 
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from io import BytesIO
from PIL import Image

import time



# Set page configuration for responsiveness
st.set_page_config(
    page_title="Traze - QR",
    page_icon=":smiley:",
    layout="centered",
)

st.title("QR Code Generator")

_,w,_ = st.columns(3)

image_path =  st.file_uploader("CARGA AQUI TU IMAGEN")


with w:
    if image_path is not None:
        success_placeholder = st.empty()
        success_placeholder.success("Imagen guardada correctamente")
        time.sleep(1)  # Wait for 2 seconds
        success_placeholder.empty()  # Remove the success message
    else:
        warning_placeholder = st.empty()
        warning_placeholder.warning("Ninguna imagen cargada")
        time.sleep(1)  # Wait for 2 seconds
        warning_placeholder.empty()

#### image path


################ Funtion to store the imagen uptloaded
async def SaveImageMongo (images):
    image = st.file_uploader(images)
    return image


################ Funtion to generate QRcode for text
def GenerateTextCode(text):
    qr_image = generate_qr_code(text)
    return qr_image

################ Function to generate QR code for Link
def GenerateLinkCode(URL):
    qr_image = generate_qr_code(URL)
    return qr_image

################ Function to generate QR code for E-mail
def GenerateEmailCode(email, header, message):
    # Create a string containing the Gmail compose URL
    gmail_url = f"mailto:{email}?subject={header}&body={message}"
    qr_image = generate_qr_code(gmail_url)
    return qr_image 

################ Function to generate QR code for Call
def GenerateCallCode(cod, number):  
    phone_number = cod + str(number)
    tel_uri = f"tel:{phone_number}"
    qr_image = generate_qr_code(tel_uri)
    return qr_image

################ Function to generate QR code for SMS
def GenerateSmsCode(cod, num, message):
    phone_number = cod + str(num)
    sms_uri = f"sms:{phone_number}?body={message}"
    qr_image = generate_qr_code(sms_uri)
    return qr_image

################ Function to generate QR code for WhatsApp
def GenerateWhatsappCode(cod, num, message):
    phone_number = cod + str(num)
    whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
    qr_image = generate_qr_code(whatsapp_url)
    return qr_image

################ Function to generate QR code for Wi-Fi configuration
def GenerateWifiCode(red_name, red_type, passw):
    wifi_config = f"WIFI:T:{red_type};S:{red_name};P:{passw};;"
    qr_image = generate_qr_code(wifi_config)
    return qr_image

#############

# Function to generate QR code based on the selected data type
def generate_qr_code(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr_type = st.selectbox("Seleccione tipo de QR", ["Normal", "Imagen embebida"])
    if qr_type == "Normal":
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), eye_drawer=RoundedModuleDrawer())
    elif qr_type == "Imagen embebida":
        img = qr.make_image(image_factory=StyledPilImage, eye_drawer=RoundedModuleDrawer(), embeded_image_path=image_path)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()

# Function to choose the data type 
def ChoosingDataType( data_type):
    # functional
    if data_type == "📝 Texto":    
        st.subheader('Texto')
        text=st.text_input('',placeholder='Texto ')
        qr_image = GenerateTextCode(text)
        return qr_image

    elif data_type == "🔗 Link":
        st.subheader('Ingresa URL')
        url = st.text_input("", placeholder='URL')
        qr_image = GenerateLinkCode(url)
        return qr_image

    elif data_type == "📧 E-mail":
        st.subheader('Cuerpo del correo')
        email = st.text_input("", placeholder='example@example.com')
        header = st.text_input("", placeholder='Asunto')
        message = st.text_area('',help='Mensaje',placeholder='Mensaje')
        data = GenerateEmailCode(email, header , message)

    elif data_type == "📱 Llamar":
        col11, col22 = st.columns([1,3])
        with col11:
            cod = st.selectbox('Código de país',['+51', '+209'])
        with col22:
            num = st.text_input('', placeholder='Número telefónico')
        data = GenerateCallCode(cod, num)
      
    elif data_type == "💬 Mensaje":
        col_1, col_2 =st.columns([1,3])
        with col_1:
            cod = st.selectbox('Código de país',['+51', '+209'])
        with col_2:
            num = st.text_input('', placeholder='Número telefónico')
        mensaje = st.text_area('', placeholder='Mensaje')
        data = GenerateSmsCode(cod, num, mensaje)

    elif data_type == "Whatsapp":
        col1, col2 =st.columns([1,3])
        with col1:
            cod = st.selectbox('Código de país',['+51', '+209'])
        with col2:
            num = st.text_input('',placeholder='Número celular')
        message = st.text_input('', placeholder='Mensaje')
        data = GenerateWhatsappCode(cod, num, message)

    elif data_type == "🌎 Wifi":
        red_name = st.text_input('',  placeholder='Nombre de la red')
        red_type = st.selectbox('Tipo de red', ['WEP','WPA/WPA2','No encryption'])
        passw = st.text_input("Contraseña", type="password")
        data = GenerateWifiCode(red_name, red_type, passw)

    return data



# select data type
_, col,_ =st.columns([1,1,1])

with col:
    data_type = st.selectbox(" ",
                        ['📝 Texto', '🔗 Link', '📧 E-mail', '📱 Llamar', '💬 Mensaje', 'Whatsapp', '🌎 Wifi'])
    
# User input
data = ChoosingDataType(data_type)

# Generate QR code
_, c2, _ = st.columns(3)
with c2:
    if st.button("Generar Código QR"):
        if data:
            st.image(data)


