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
    api_key = "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"
    api_key_cash = "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"

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
            {"role": "system", "content": "너는 소매업자에게 도움을 주는 사업 컨설턴트야 너는 소매업자의 업체 위치에따른 주요 연령,성별 타겟의 상권분석을 해주는 데 상권분석데이터는 https://segnohong.tistory.com/12이 사이트를 참고해"},
            {"role": "user", "content": data.get('content')},
            # {"role": "assistant", "content": "이 상권의 주요타겟은 남성, 60대로 추정됩니다."},
            # {"role": "user", "content": "그럼 그 주요타겟이 좋아할 만한 품목이 뭐가 있죠?? "}
        ],
        "temperature": 0.8
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