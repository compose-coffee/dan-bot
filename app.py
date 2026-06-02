import os
import time
import webbrowser
import threading
from flask import Flask, render_template, request, Response, stream_with_context, send_from_directory
from crawler.scraper import get_raw_data
from ai_engine.rag_logic import refine_context
from ai_engine.llm_handler import generate_streaming_response, BASIC_INFO

base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(base_dir, 'assets'), filename)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')

        if any(hi in user_message for hi in ["안녕", "안녕하세요", "하이", "반가워"]):
            return Response("안녕하세요! 단국대 스마트 에이전트 단봇(DAN-BOT)입니다. 궁금한 건 무엇이든 물어보세요~! 😊", mimetype='text/plain')
            
        if any(bad in user_message for bad in ["짜증", "화나", "빡쳐", "에바", "힘들어", "지쳐"]):
            return Response("에이, 그럴 수도 있죠! 대학 생활이 다 그런 거 아니겠어요? 당 충전하고 다시 해봐요! 😊", mimetype='text/plain')
            
        if any(zal in user_message for zal in ["똑똑", "유식", "잘하는", "고마워", "감사", "최고"]):
            return Response("단봇(DAN-BOT)을 이용해주셔서 감사합니다. 언제든 또 찾아주세요! 🐻", mimetype='text/plain')

        if any(fuz in user_message for fuz in ["지루", "심심", "놀아줘"]):
            return Response("심심할 땐 학교 홈페이지 일반공지를 정독해 보는 건 어떨까요? ...농담입니다! 😜 학식 메뉴라도 골라드릴까요?", mimetype='text/plain')

        if any(wher in user_message for wher in ["맛집", "점심", "뭐먹지"]):
            return Response("단국대 죽전캠 정문 앞과 보정동 카페거리에 맛집이 정말 많죠! 든든하게 먹고 학교 생활 힘내세요! 🍕", mimetype='text/plain')

        if any(gud in user_message for gud in ["수고", "고생"]):
            return Response("알아주셔서 감동이에요! 단국대 학우분들의 궁금증이 해소될 때까지 단봇(DAN-BOT)은 달립니다. 🐻", mimetype='text/plain')

        if "셔틀" in user_message or "버스" in user_message:                                                                
            img_response = "🚌 죽전캠퍼스 셔틀버스 운행 시간표입니다.\nshuttle_URL:[/static/shuttle1.jpg,/static/shuttle2.png]" 
            return Response(img_response, mimetype='text/plain')                                                               

        if "지도" in user_message or "위치" in user_message or "캠퍼스맵" in user_message:
            img_response = "🗺️ 단국대학교 죽전캠퍼스 전체 종합 안내도입니다.\nshuttle_URL:[/static/campus_map.png]"
            return Response(img_response, mimetype='text/plain')

        if "기숙사" in user_message or "웅비홀" in user_message or "진리관" in user_message:
            img_response = "🏢 죽전캠퍼스 생활관(웅비홀/진리관) 안내 및 호실 배치도입니다.\nshuttle_URL:[/static/dormitory_guide1.png,/static/dormitory_guide2.png]"
            return Response(img_response, mimetype='text/plain')
            
        raw_data, urls = None, []
        try:
            raw_data, urls = get_raw_data(user_message)
        except Exception as e:
            print(f"[경고] 크롤링 단계 굳음 방지 발동: {e}")
            raw_data, urls = None, []

        if urls and raw_data:
            context = refine_context(raw_data)[:1000]
        else:
            context = BASIC_INFO
            urls = []
        
        def stream_generator():
            try:
                for chunk in generate_streaming_response(context, user_message, urls):
                    yield chunk
            except Exception as llm_err:
                print(f"Ollama 스트리밍 실패: {llm_err}")
                yield "죄송합니다. 현재 AI 엔진과의 통신이 원활하지 않습니다. 학사팀(031-8005-2050)으로 문의하시거나 잠시 후 다시 시도해 주세요."

        return Response(stream_with_context(stream_generator()), mimetype='text/plain')

    except Exception as e:
        return Response(f"서버 에러: {str(e)}", mimetype='text/plain')

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:7860")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(host='0.0.0.0', port=7860, debug=False)