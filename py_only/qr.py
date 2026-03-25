import qrcode

# QR 코드에 담을 데이터
data = "data.PNG"

# QR 코드 생성
qr = qrcode.QRCode(
    version=1,  # QR 코드의 버전 (1~40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # 오류 수정 수준
    box_size=10,  # QR 코드의 각 박스 크기
    border=4,  # 테두리 크기
)
qr.add_data(data)
qr.make(fit=True)

# QR 코드 이미지 생성
img = qr.make_image(fill_color="black", back_color="white")

# 이미지 파일로 저장
img.save("maps.png")

