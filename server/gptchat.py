from flask import Flask, request
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
Authorization: "Bearer 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"



@app.route('/consult', methods=['POST'])
def consult():
    # API 키
    api_key = ""


    data = request.get_json()
    print("리엑트에서 온 값: ", data)


    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        #"model": "gpt-4",
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "너는 소매업자에게 도움을 주는 사업 컨설턴트야 너는 소매업자의 업체 위치에따른 주요 연령,성별 타겟의 상권분석을 해주는 데 상권분석결과는 {위치:광주광역시 독립로 54번길29, 성별: 여성, 연령:40대}로 가장 많이 찾아오는 타겟에 대한 데이터야"},
            {"role": "user", "content": data.get('content')},
            # {"role": "assistant", "content": "이 상권의 주요타겟은 남성, 60대로 추정됩니다."},
            # {"role": "user", "content": "그럼 그 주요타겟이 좋아할 만한 품목이 뭐가 있죠?? "}
        ],
        # 연결 설정
        # OpenAI config
        "temperature": 0.2,          # 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
        "top_p" : 0.0,               # 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
        # "best_of" : 1,               # 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성) => best_of가 없다고 함
        "frequency_penalty" : 0.0,   # 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
        "presence_penalty": 0.0   # 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)

         # prompt 작성
         # "prompt" :  f'''
         #        문제 :
         #        # {problem_content}
         #        # 제출한 코드 :
         #        # {sub_code}
         #        # 제한조건 :
         #        # {test_condition}
         #        #
         #       아래의 1번, 2번의 형식화된 문장으로만 대답해야해. 그 이외의 답변이나 설명은 절대 하지마.
         #       그리고 1번과 2번 답변 사이에 한 단락을 띄워줘.
         #        1번. 작성된 코드를 판단해서 => "1번. 정답 or 오답 입니다" 반드시 이 형식으로 출력해줘.
         #        2번. 작성된 코드의 조건을 판단해서  => 2번. "조건n번 : 만족 or 불만족, 조건n번: 만족 or 불만족,..." 반드시 이 형식으로 출력해줘.
         #        '''


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