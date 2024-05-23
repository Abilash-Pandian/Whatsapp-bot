import qrcode


def generate_qr_code():
    whatsapp_link = "https://wa.me/6369625511"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(whatsapp_link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save("whatsapp_qr.png")


if __name__ == "__main__":
    generate_qr_code()
