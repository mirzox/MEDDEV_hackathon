import qrcode


def gen_qr_code(text: str, path_to_save: str):
    img = qrcode.make(text)  # generate QRcode
    img.save(path_to_save)
