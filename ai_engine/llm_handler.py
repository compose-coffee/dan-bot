import requests
import json

BASIC_INFO = """
[단국대학교 학사지원 스마트 챗봇 기본 지식]
- 명칭: 단국대학교 학사지원 스마트 챗봇 '단봇(DAN-BOT)'
- 학사팀 (죽전): 031-8005-2050
- 장학팀: 031-8005-2402
"""

def generate_streaming_response(current_context, user_message, source_urls):
    if not current_context:
        current_context = "단국대학교 관련 학사 정보 내역을 참고하여 답변하십시오."

    payload = {
        "model": "llama3.2:3b",
        "prompt": (
            f"너는 단국대학교 학사 안내 전문 AI 스마트 챗봇 '단봇'이다.\n"
            f"주어진 [참조 데이터]의 내용을 기반으로 사용자의 질문에 친절하고 명확하게 답변하라.\n\n"
            f"[규칙]\n"
            f"1. 반드시 100% 한국어로만 답변하고 외국어 사용하지마. 'College of Information Science and Engineering' 이 말 쓰지마. 요점만 간단히 요약하라.\n"
            f"2. 데이터에 없는 내용을 억지로 상상해서 지어내지 마라.\n\n"
            f"[참조 데이터]:\n{current_context}\n\n"
            f"[사용자 질문]: {user_message}\n\n"
            f"단봇의 답변:"
        ),
        "stream": True,
        "options": {
            "temperature": 0.1,
            "top_p": 0.8,
            "num_predict": 500,
            "num_thread": 4
        }
    }
    try:
        with requests.post("http://localhost:11434/api/generate", json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    json_data = json.loads(decoded_line)
                    chunk = json_data.get("response", "")
                    yield chunk
    except Exception as e:
        yield f"AI 엔진 통신 에러: {str(e)}"