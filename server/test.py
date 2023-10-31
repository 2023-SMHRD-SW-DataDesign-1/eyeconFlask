import requests
import base64
from flask import Flask
app = Flask(__name__)
@app.route("/test")
def test():
# image(rawdata) -> api -> image(attention map)
# api url
    upload_url = "http://geneye.gendata.cloud/upload"

# 이미지 파일 전송
    image_file_path = './image.jpeg'

    files = {'image': open(image_file_path, 'rb')}
    response = requests.post(upload_url, files=files)
# print(response)
    response_data = response.json()

# base64 이미지를 디코딩
    image_base64 = response_data['image_base64']
    image_data = base64.b64decode(image_base64)

    if response.status_code == 200:
        data = response.json()
    # 정상 응답인 경우 -> 이미지 저장

        local_image_path = './received_image.jpg'

        with open('received_image.jpg', 'wb') as img_file:
            img_file.write(image_data)

    else:
        print(f'Error: {response.status_code}')
        if 'error' in response.json():
            print(f'Error Message: {response.json()["error"]}')

    return "test"

if __name__ == '__main__':
    app.run(debug=True)