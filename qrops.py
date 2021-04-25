import cv2
from pyzbar import pyzbar
import qrcode
import argparse

COMMAND_READ_QR = "read_qr"
COMMAND_GENERATE_QR = "generate_qr"

SUPPORTED_COMMANDS = {
    COMMAND_READ_QR: "",
    COMMAND_GENERATE_QR: "",
}


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = None
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        print("CONTENT:\n{}\n".format(barcode_info))
    return frame, barcode_info


def scan_qrcode():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame, qrcontent = read_barcodes(frame)
        if qrcontent is not None:
            break
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()


def generate_qrcode(message):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=SUPPORTED_COMMANDS.keys(),
                        help="command for the client. supported options are: {}".format(
                            ', '.join(SUPPORTED_COMMANDS.keys())))
    args = parser.parse_args()
    if args.command == COMMAND_READ_QR:
        scan_qrcode()
    elif args.command == COMMAND_GENERATE_QR:
        content = input("Please enter QR content:")
        generate_qrcode(content)

