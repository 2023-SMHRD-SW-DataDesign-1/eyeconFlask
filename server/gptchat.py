import io

from flask import Flask, request, jsonify, send_file
import requests
import json
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import urllib.request
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import requests
import base64
import torch
import pandas as pd
import numpy as np
# from PIL import Image

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://3.36.133.196:3000", "https://3.36.133.196:3000", "http://eyecon.site", "https://eyecon.site"]}}, supports_credentials=True)
Authorization: "Bearer "

# 전역 변수 선언
global_data = {}
print(global_data)

@app.route('/consult', methods=['POST'])
@cross_origin(origins=["http://3.36.133.196:3000","https://3.36.133.196:3000","http://eyecon.site", "https://eyecon.site"])
def consult():
    # 파일 경로
    file_path = '../secret/gptkey.json'
    print("dd")
    # 파일 열기
    with open(file_path, 'r') as f:
        data = json.load(f)

    # api_key 값 가져오기
    api_key = data['api_key']


    data = request.get_json()
    print(data)
    if 'id' in data:
        # 스프링부트에서 보낸 데이터 저장
        global_data['spring'] = data
    else:
        # 리액트에서 보낸 데이터 저장
        global_data['react'] = data

    # 스프링부트와 리액트에서 보낸 데이터 가져오기
    spring_data = global_data.get('spring', {})
    react_data = global_data.get('react', {})

    # 데이터에서 값 가져오기
    id = spring_data.get('id')
    place = spring_data.get('place')
    age = spring_data.get('age')
    sex = spring_data.get('sex')
    storecnt = spring_data.get('storecnt')
    income = spring_data.get('income')
    population = spring_data.get('population')
    maxday = spring_data.get('maxday')
    category = spring_data.get('category')
    content = react_data.get('content')


    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # 1. 주요타겟 = 성별 + 연령
    # 2. 유동인구 = 유동인구수 + 최다 방문? 요일
    # 3. 주변 동종 업체 개수
    # 4. 주변 동종 업체 월 평균 매출
    # 5.

    data = {
        "model": "gpt-4",
        # "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system",
             "content": f'''당신은 소매업자({category} 점주)에게 도움을 주는 사업 컨설턴트입니다.
                 점주의 가게 위치(주소) : {place},
                 주요 타겟 성별 : {sex},
                 주요 타겟 연령 : {age},
                 주변 동종업계 수 : {storecnt}, 
                 주변 상권 평균 매출 : {income},
                 주변 상권 일 평균 유동인구 : {population},
                 주변 상권 유동인구 최대 요일 : {maxday} 
                위의 정보들을 참고해서 대답하세요. 정보들이 null인 경우에는 해당 정보를 참고하지 마세요.
                "사진"에 관한 질문이 들어올 시 사진은 시선 예측 AI로 시선 예측 정보가 담긴 히트맵 이미지를 뜻합니다. 이 정보를 통하여 답변하고, 결과 페이지에서 상품 가상 배치 기능을 사용해보라고 추가로 답변을 하세요. 사진에 대한 분석 또는 설명을 할 수 없다는 답변은 하지마세요. 
                모든 답변은 1~3개의 문장으로 답변하세요. '''},
            # {"role": "user", "content": "제 가게 주변 상권을 알려주거나 분석해주세요. "},
            # {"role": "assistant", "content": f'''{place}위치의 상권 주요타겟은 {age} {sex}입니다. 주변 상권 동종업계 수는 {storecnt}, 평균 매출은 {income}, 일 평균 유동인구는 {population}, 유동인구 최대 요일은 {maxday} 입니다.'''},
            # {"role": "user", "content": "우리 가게의 타겟을 알려주거나 분석해주세요 "},
            # {"role": "assistant", "content": f'''{place}위치의 상권 주요타겟은 {age} {sex}입니다.'''},
            # {"role": "user", "content": "주요 타겟이 좋아할 만한 품목이 뭐가 있죠?? "},
            # {"role": "assistant", "content": f'''{age} {sex}의 좋아할 만한 품목은 주류와 라면류입니다.'''},
            # {"role": "user", "content": "저 사진에 대해 설명해줘 "},
            # {"role": "assistant", "content": f'''사진은 시선 예측 AI가 분석한 결과를 표현한 히트맵 이미지입니다. 이를 통해 고객들이 가장 많이 주목하는 상품 위치를 파악할 수 있습니다. 결과페이지에서 Planogram 기능을 사용해 보세요.'''},
            {"role": "user", "content": content}

        ],
        # 연결 설정
        # OpenAI config

        "temperature": 0.2,  # 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
        "top_p": 0.0,  # 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
        # "best_of" : 1,               # 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성) => best_of가 없다고 함
        "frequency_penalty": 0.0,  # 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
        "presence_penalty": 0.0  # 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)
        # "n" : 2                   # GPT가 제공하는 답변 경우의 수
        # "stop"                    # GPT가 답변할때 설정한 단어가 나오면 거기서 대답멈추는 거 같음


    }


    print("user가 들어간 데이터 : ",data)
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
        print("gpt와 통신도 되는지?", response.json())
    except Exception as e:
        print("Error occurred: ", e)
    return response.json()


 # 시선예측 api 모델
@app.route('/eye', methods=['POST'])
@cross_origin(origins=["http://3.36.133.196:3000","https://3.36.133.196:3000","http://eyecon.site", "https://eyecon.site"])
def eye():
    data = request.get_json()
    print("data['beforeimg'] : ", data['beforeimg'])

    # 파이어베이스 앱 초기화
    if not firebase_admin._apps:
        cred = credentials.Certificate("../secret/eyecon-9b097-firebase-adminsdk-38k19-ceea89468c.json")
        firebase_admin.initialize_app(cred, {
        "storageBucket": "eyecon-9b097.appspot.com"
        })

    #스토리지 버킷 가져오기
    bucket = storage.bucket()

    img_path = data['beforeimg']
    print(img_path)

    resp = urllib.request.urlopen(img_path)

    image_data = resp.read()

    # 바이트 스트림을 파일 객체로 변환
    image_file = io.BytesIO(image_data)
    print(resp)
    # 전송 결과 확인
    # if response.status_code == 200:
    #     print("이미지 전송 성공")
    # else:
    #     print("이미지 전송 실패")
    upload_url = "http://geneye.gendata.cloud/upload"
    response = requests.post(upload_url, files={'image': image_file})
    print(response)

    response_data = response.json()
    # print(response_data)
    # base64
    response_image_base64 = response_data['image_base64']
    # response_image_data = base64.b64decode(response_image_base64)

    return response_image_base64

@app.route('/slice', methods=['POST'])
@cross_origin(origins=["http://3.36.133.196:3000","https://3.36.133.196:3000","http://eyecon.site", "https://eyecon.site"])
def slice():
    # yolov5 불러오기
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

    # model에 넣을 beforeImgUrl
    data = request.get_json()
    before_img = data['beforeImgUrl']

    # 이미지에서 객체를 검출합니다.
    with urllib.request.urlopen(before_img) as url_response:
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)

    # yolov5 예측
    results = model(img)


    slice_list = []
    # 검출된 각 객체에 대해 반복합니다.
    for i, (x, y, w, h, conf, _) in enumerate(results.xywh[0]):

        if(conf.item() > 0.8) :
            print("conf : ", conf.item())
            # bounding box 좌표를 정수로 변환합니다.
            x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
            print(x1, y1, x2, y2)
            # bounding box를 기반으로 이미지를 잘라냅니다
            crop_img = img[y1:y2, x1:x2]
            _, encoded_image = cv2.imencode('.jpg', crop_img)
            image_bytes = encoded_image.tobytes()

            # bytes를 base64 인코딩된 문자열로 변환합니다.
            image_string = base64.b64encode(image_bytes).decode('utf-8')

            slice_list.append(image_string)

    # JSON 배열로 변환하여 반환합니다
    # print(slice_list)
    return jsonify(slice_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)