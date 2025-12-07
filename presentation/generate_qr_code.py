import qrcode


def generate_qr_code(url):
    filename = f"qrcode_{url.split('//')[1].replace('/', '_')}.png"
    img = qrcode.make(url)
    img.save(f"presentation/qr_codes/{filename}")


if __name__ == "__main__":
    url1 = "https://github.com/Rae99/bin-packing-experiment"
    generate_qr_code(url1)

    url2 = "https://developers.google.com/optimization/pack/bin_packing"
    generate_qr_code(url2)
