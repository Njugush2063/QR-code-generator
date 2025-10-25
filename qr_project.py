import PySimpleGUI4 as psg
import qrcode
from PIL import Image
import io
import os
import re


def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=2,
        box_size=8,
        border=8,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black",back_color="white")

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

layout = [
    [psg.Image(key="image",size=(300,300),background_color="gray")],
    [psg.Input(size=(25,1),key="link")],
    [psg.Button("Generate QR Code"), psg.Button("open Folder"), psg.Button("Exit")]
]

window = psg.Window("QR Image Viewer", layout)



    
    
       


while True:
    event, values = window.read()

    if event == psg.WIN_CLOSED or event == "Exit":
        break

    if event == "Generate QR Code":
        user_input = values["-INPUT-"].strip()
        
        if not user_input:
            psg.popup("⚠️ Please enter a URL or text first!")
            continue
        
        try:
            print(f"Generating QR code for: {user_input}")
            img_bytes, filepath = generate_qr_code(user_input)
            
            # Update the image display
            window["-IMAGE-"].update(data=img_bytes)
            
            last_filepath = filepath
            psg.popup(f"✓ QR Code generated!\nSaved to:\n{filepath}", title="Success")
            
        except Exception as e:
            psg.popup_error(f"❌ Error: {str(e)}")
            print(f"Error details: {e}")
    
    if event == "Open Folder":
        if last_filepath and os.path.exists(last_filepath):
            # Open the folder containing the file
            folder = os.path.dirname(last_filepath)
            os.startfile(folder)  # Windows
            # For Mac: os.system(f'open "{folder}"')
            # For Linux: os.system(f'xdg-open "{folder}"')
        else:
            psg.popup("⚠️ Generate a QR code first!")


window.close()