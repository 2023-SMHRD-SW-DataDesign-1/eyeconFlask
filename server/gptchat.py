import io

from flask import Flask, request, jsonify, send_file
import requests
import json
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import urllib.request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import requests
import base64
from datetime import datetime, timedelta
from urllib.parse import quote

app = Flask(__name__)
CORS(app, supports_credentials=False)
Authorization: "Bearer "

# 전역 변수 선언
global_data = {}
print(global_data)

@app.route('/consult', methods=['POST'])
@cross_origin(origins="http://localhost:3000")
def consult():
    # API 키
    # api_key = ""




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


    prompt = f'''
                타겟 성별 :
                # {sex}
                # 타겟 연령 :
                # {age}
                # 제한조건 :
                # {place}
                # 
               아래의 1번, 2번의 형식화된 문장으로만 대답해야해. 
               그리고 1번과 2번 답변 사이에 한 단락을 띄워줘.
                1번. 타겟 성별과 타겟 연령을 가지고 => "회원님의 주소를 토대로 상권분석을 했습니다. 회원님 편의점의 주요 고객층은 {age} {sex} 입니다" 반드시 이 형식으로 출력해줘.
                2번. 내가 너한테 준 데이터 외의 데이터를 써야하는 질문에서  => "이 데이터는 오차가 있을 수 있습니다. " 라고 하고 질문의 답을 해주고 답변은 400자를 넘기면 안돼.
                '''


    # data = {
    #     #"model": "gpt-4",
    #     "model": "gpt-3.5-turbo",
    #     "messages": [
    #         {"role": "system", "content": f'''너는 소매업자에게 도움을 주는 사업 컨설턴트야 너는 소매업자의 업체 주소에 따라서 주요 연령,성별 타겟의 상권분석을 해주는 데 상권분석은 위치:{place}, 성별:{sex}, 연령:{age}로 가장 많이 찾아오는 타겟에 대한 데이터만 말해 내가 부여한 데이터 외의 분석은 하지마 내가 보내준 데이터로 답하기 어려운 문제는 "이 데이터는 정확하지 않을 수 있습니다." 라는 말을 앞에 먼저하고 너 나름대로 답을 해줘 그리고 문장은  최대한 간략하게 항상 답해야 해 '''},
    #         {"role": "user", "content": "제 가게의 상권을 분석해주세요 "},
    #         {"role": "assistant", "content": f'''이 상권의 주요타겟은 {age} {sex}입니다.'''},
    #         {"role": "user", "content": "그럼 그 주요 타겟이 좋아할 만한 품목이 뭐가 있죠?? "},
    #         {"role": "assistant", "content": f'''{age} {sex}의 좋아할 만한 품목은 주류와 라면류입니다.'''},
    #         {"role": "user", "content": content  }
    #
    #     ],
    #     # 연결 설정
    #     # OpenAI config
    #     "temperature": 0.2,          # 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
    #     "top_p" : 0.0,               # 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
    #     # "best_of" : 1,               # 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성) => best_of가 없다고 함
    #     "frequency_penalty" : 0.0,   # 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
    #     "presence_penalty": 0.0,   # 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)
    #     # "n" : 2                   # 답변하는 횟수 제한
    #
    #
    #
    # }
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
                문장 끝마다 줄바꿈을 넣어서 답변하세요.
                모든 답변은 1~3개의 문장으로 답변하세요. '''},
            # {"role": "user", "content": "제 가게 주변 상권을 알려주거나 분석해주세요. "},
            # {"role": "assistant", "content": f'''{place}위치의 상권 주요타겟은 {age} {sex}입니다. 주변 상권 동종업계 수는 {storecnt}, 평균 매출은 {income}, 일 평균 유동인구는 {population}, 유동인구 최대 요일은 {maxday} 입니다.'''},
            # {"role": "user", "content": "우리 가게의 타겟을 알려주거나 분석해주세요 "},
            # {"role": "assistant", "content": f'''{place}위치의 상권 주요타겟은 {age} {sex}입니다.'''},
            # {"role": "user", "content": "주요 타겟이 좋아할 만한 품목이 뭐가 있죠?? "},
            # {"role": "assistant", "content": f'''{age} {sex}의 좋아할 만한 품목은 주류와 라면류입니다.'''},
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
@cross_origin(origins="http://localhost:3000")
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

if __name__ == '__main__':
    app.run(debug=True)