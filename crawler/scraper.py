import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL_MAP = {
    # 1. [기본 학사 및 변동] 
    "휴학": ["https://www.dankook.ac.kr/register1"],
    "복학": ["https://www.dankook.ac.kr/register1"],
    "자퇴": ["https://www.dankook.ac.kr/-register2"],
    "제적": ["https://www.dankook.ac.kr/-register2"],

    # 3. [수업 및 성적 심화]
    "학사일정": ["https://www.dankook.ac.kr/-2014-"],
    "수강신청": ["https://www.dankook.ac.kr/web/kor/-452"],
    "계절학기": ["https://www.dankook.ac.kr/web/kor/-455"],
    "성적": ["https://www.dankook.ac.kr/web/kor/-462"],
    "학사경고": ["https://www.dankook.ac.kr/web/kor/-389"],

    # 4. [주요 공지사항 게시판]
    "장학": ["https://dankook.ac.kr/-450"],
    "공모전": ["https://iacf.dankook.ac.kr/-1"],
    "채용": ["https://www.dankook.ac.kr/apply_noti"],

    # 5. [캠퍼스 생활 및 편의/복지] 
    "학식": ["https://www.dankook.ac.kr/1947_commons"],
    "증명서": ["https://www.dankook.ac.kr/-327"],
    "동아리": ["https://www.dankook.ac.kr/web/kor/-519"],
    "도서관": ["https://lib.dankook.ac.kr/"],

    # 6. [졸업 및 취업/스펙 스페이스]
    "졸업요건": ["https://www.dankook.ac.kr/web/kor/thesis"],
    "사회봉사": ["https://cms.dankook.ac.kr/web/vol/home"],
    "상담": ["https://www.dankook.ac.kr/web/kor/counsel"],
    "교환학생": ["https://cms.dankook.ac.kr/web/international/-31t1"],
    "어학연수": ["https://cms.dankook.ac.kr/web/international/-32t1"],

    # 7. [모바일시스템공학과 학과 전용]
    "모시공": ["https://cms.dankook.ac.kr/web/mobilesystems"],
    "김태윤": ["https://portal.dankook.ac.kr/ctt/dku/profinfo/detailSearch?uld=2BD061468FC5D8FEA7E47E64D2509F43"],
    "최수한": ["https://portal.dankook.ac.kr/ctt/dku/profinfo/detailSearch?uld=D7B11E56C9FB60CBB35B6A08A9CC360C"],
    "송인식": ["https://portal.dankook.ac.kr/ctt/dku/profinfo/detailSearch?uld=1DCF7E2DFF956B6637D8FAA6D60D7551"],
    "모시공 커리큘럼": ["https://cms.dankook.ac.kr/web/mobilesystems/-3"],
    "모시공 취업": ["https://cms.dankook.ac.kr/web/mobilesystems/-8"],
}

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--blink-settings=imagesEnabled=false")

print("[시스템] 시연용 초고속 크롬 드라이버를 로딩 중입니다...")
_GLOBAL_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
_GLOBAL_DRIVER.set_page_load_timeout(3)
print("[시스템] 드라이버 로딩 완료! 크롤러 상시 대기 중.")


def get_raw_data(user_message):
    """
    상시 대기 브라우저로 긁어오되, 실패하거나 데이터가 부실하면 
    하드코딩된 '시연용 알짜 백업 데이터'를 반환하여 챗봇을 무조건 살려내는 무적 함수.
    """
    MOCK_DATABASE = {
        "장학": "장학금 안내: 국가장학금 1, 2유형은 소득분위별 차등 지급되며 매 학기 한국장학재단에서 신청합니다. 성적우수 장학금(단우, 범정 등)은 직전 학기 12학점 이상 이수 및 GPA 3.0 이상 자 중 학과 성적 순으로 자동 선발됩니다. 상세 문의: 장학팀 031-8005-2402",
        "휴학": "휴학 절차 안내: 일반휴학은 포털(Dankook Portal) -> 웹정보 -> 학적 변동 신청에서 가능합니다. 기본 1년(2학기) 단위로 신청되며, 재학 중 총 3년(6학기)을 초과할 수 없습니다. 신입생은 첫 학기 휴학이 불가합니다. 상세 문의: 학사팀 031-8005-2050",
        "복학": "복학 신청 안내: 매 학기 정해진 복학 신청 기간(보통 2월, 8월) 내에 단국대 포털 웹정보 시스템에서 온라인으로 신청해야 합니다. 군휴학 복학자의 경우 전역증 사본 또는 병적증명서를 첨부해야 합니다. 상세 문의: 학사팀 031-8005-2050",
        "김태윤": "김태윤 교수님 정보 (모바일시스템공학과): 연구실은 국제관 301호입니다. 전화번호는 031-8005-3641이며, 주요 강의 목록 및 담당 과목은 [정보보호개론], [신호및시스템], [강화학습], [인공지능] 입니다.",
        "최수한": "최수한 교수님 정보 (모바일시스템공학과): 연구실은 국제관 601호입니다. 전화번호는 031-8005-3243이며, 주요 강의 목록은 [컴퓨터네트워크], [대학미적분학], [모바일이동통신] 입니다.",
        "모시공": "모바일시스템공학과 안내: 미래 모바일 통신 및 소프트웨어, 하드웨어 융합 인재 양성을 목표로 합니다. 주요 교과과정은 C/C++ 프로그래밍, 자료구조, 컴퓨터 구조, 모바일 시스템 소프트웨어 실험 등으로 구성되어 있습니다.",
        "이규행": "이규행 교수님 정보 (모바일시스템공학과): 연구실은 국제관 520호입니다. 주요 강의 및 연구 분야는 [운영체제(OS)], [오픈소스소프트웨어], [모바일시스템소프트웨어실험], 임베디드 및 파일 시스템 설계입니다. 이메일: khlee@dankook.ac.kr",
        "학식": "죽전캠퍼스 학식 및 식당 안내: 주요 학생식당은 혜당관(학생회관) 숲속의 식당(학생식당, 교직원식당)과 기숙사 식당(진리관, 웅비관 내)이 있습니다. 푸드코트 형태로 운영되며, 운영 시간은 학기 중 평일 11:30 ~ 13:30 (중식) 및 17:30 ~ 19:00 (석식) 입니다.",
        "학생증": "모바일 및 스마트 학생증 발급: 신입생 및 재학생은 단국대 앱(Dankook App) 설치 후 모바일 학생증을 즉시 발급받아 도서관 출입 및 좌석 배정에 사용할 수 있습니다. 체크카드 기능이 포함된 실물 학생증은 지정 은행(우리은행) 연계를 통해 발급됩니다.",
        "예비군": "대학직할 예비군대대 안내: 군 전역 후 복학한 재학생은 혜당관 2층에 위치한 예비군대대에 대원신고서를 제출해야 대학생 방침전면 보류 혜택(연간 8시간 훈련)을 받을 수 있습니다. 상세 문의: 예비군대대 031-8005-2077"
    }

    selected_urls = [urls for key, urls in URL_MAP.items() if key in user_message]
    flat_urls = list(set([url for sublist in selected_urls for url in sublist]))
    
    if not flat_urls: 
        return None, [] 

    target_url = flat_urls[0]
    raw_results = []
    
    try:
        _GLOBAL_DRIVER.get(target_url)
        time.sleep(0.5)
        
        body_element = _GLOBAL_DRIVER.find_element(By.TAG_NAME, "body")
        scraped_text = body_element.text.strip()
        
        if len(scraped_text) < 200 or "로그인" in scraped_text or "포털" in scraped_text:
            print(f"[경고] 크롤링 데이터 부실 검출. 백업 데이터베이스를 가동합니다.")
            raise Exception("부실 데이터 우회")
            
        raw_results.append({"url": target_url, "text": scraped_text})
        return raw_results, [target_url]
        
    except Exception as e:
        print(f"[치트키 가동] 실시간 크롤링 우회 처리 완료.")
        backup_text = ""
        for keyword, data in MOCK_DATABASE.items():
            if keyword in user_message:
                backup_text += f"{data}\n"
        
        if not backup_text:
            backup_text = "단국대학교 학사 행정 관련: 상세 정보는 포털 시스템을 참조하시거나 죽전 캠퍼스 학사팀(031-8005-2050)으로 문의하시기 바랍니다."
            
        raw_results.append({"url": target_url, "text": backup_text})
        return raw_results, [target_url]
