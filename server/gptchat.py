from flask import Flask, request
import requests
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=False)
Authorization: "Bearer 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"

# 전역 변수 선언
global_data = {}
print(global_data)

@app.route('/consult', methods=['POST'])
@cross_origin(origins="http://localhost:3000")
def consult():
    # API 키
    api_key = ""



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


    data = {
        #"model": "gpt-4",
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f'''너는 소매업자에게 도움을 주는 사업 컨설턴트야 너는 소매업자의 업체 위치에따른 주요 연령,성별 타겟의 상권분석을 해주는 데 상권분석은 위치:{place}, 성별:{sex}, 연령:{age}로 가장 많이 찾아오는 타겟에 대한 데이터만 말해 내가 부여한 데이터 외의 분석은 하지마 내가 보내준 데이터로 답하기 어려운 문제는 이 데이터는 정확하지 않을 수 있습니다 라는 말을 앞에 먼저하고 너 나름대로 답을 해줘 그리고 문장은  최대한 간략하게 항상 답해야 해 '''},
            {"role": "user", "content": "제 가게의 상권을 분석해주세요 "},
            {"role": "assistant", "content": f'''이 상권의 주요타겟은 {age} {sex}입니다.'''},
            {"role": "user", "content": "그럼 그 주요 타겟이 좋아할 만한 품목이 뭐가 있죠?? "},
            {"role": "assistant", "content": f'''{age} {sex}의 좋아할 만한 품목은 주류와 라면류입니다.'''},
            {"role": "user", "content": content  }

        ],
        # 연결 설정
        # OpenAI config
        "temperature": 0.2,          # 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
        "top_p" : 0.0,               # 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
        # "best_of" : 1,               # 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성) => best_of가 없다고 함
        "frequency_penalty" : 0.0,   # 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
        "presence_penalty": 0.0   # 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)




    }
    print("user가 들어간 데이터 : ",data)
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
        print("gpt와 통신도 되는지?", response.json())
    except Exception as e:
        print("Error occurred: ", e)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)