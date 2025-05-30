import streamlit as st
import pandas as pd
import os
import time
# 랜덤 함수 임시용
import random
CSV_FILE = "users.csv"

# CSV 초기화 (처음 실행 시 파일 없으면 생성)
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["name", "win", "draw", "lose"])
        df.to_csv(CSV_FILE, index=False)

init_csv()

# 사용자 저장 함수
def save_user(name):
    filename = "users.csv"
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=["name"])
    
    # 새로운 사용자 추가
    new_row = pd.DataFrame([{"name": name, "win": 0, "draw": 0, "lose": 0}])
    df = pd.concat([df, new_row], ignore_index=True)

    # CSV로 저장
    df.to_csv(filename, index=False)

def is_duplicate_user(name):
    try:
        df = pd.read_csv("users.csv")
        return name in df['name'].values
    except FileNotFoundError:
        return False
    
def update_user_record(name, result):
    # CSV 로드
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["name", "win", "draw", "lose"])

    # 유저 row가 존재하는지 확인
    if name in df["name"].values:
        idx = df[df["name"] == name].index[0]

    # 결과 업데이트
    if result == "🎉 인간 승리!":
        df.at[idx, "win"] += 1
    elif result == "무승부 🤝":
        df.at[idx, "draw"] += 1
    elif result == "🤖 AI 승리!":
        df.at[idx, "lose"] += 1

    # 다시 저장
    df.to_csv(CSV_FILE, index=False)

# 사용자 목록 불러오기
def get_users():
    return pd.read_csv(CSV_FILE)

# 웹사이트 기본설정
st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="🎮",
    layout="wide"
)

# 현재 페이지 저장용
if "page" not in st.session_state:
    st.session_state.page = "home" 

# 페이지 전환 함수
def set_page(name):
    st.session_state.page = name

def judge_win(human, ai):
    if human == ai:
        return "무승부 🤝"
    elif (human == "scissors" and ai == "paper") or \
         (human == "rock" and ai == "scissors") or \
         (human == "paper" and ai == "rock"):
        return "🎉 인간 승리!"
    else:
        return "🤖 AI 승리!"
    
# 시작 페이지
def main():
    # 제목 및 설명
    st.markdown("""
        <div style='text-align: center;'>
            <h1>✊ ✋ ✌ 가위바위보 게임 ✌ ✋ ✊</h1>
            <h4>간단하게 즐기는 가위바위보 게임!</h4>
            <p>이 게임은 머신러닝으로 학습된 AI와 대결하는 가위바위보 게임입니다.<br>
            '게임 시작' 버튼을 눌러 플레이를 시작해보세요!</p>
        </div>
    """, unsafe_allow_html=True)

    # 버튼을 중앙에 정렬 (가운데 column 하나만 사용)
    col1, col2, col3 = st.columns([4, 1, 4])
    with col2:
        st.markdown("### 게임 메뉴", unsafe_allow_html=True)

        if st.button("🎮 게임 시작"):
            set_page("game")
            st.rerun()

        if st.button("👤 사용자 정보"):
            set_page("user")
            st.rerun()

        if st.button("🛑 종료"):
            set_page("exit")
            st.rerun()

# 게임 페이지
def game_clicked_page():
    if st.button("← 홈으로 "):
        set_page("home")
        st.rerun()

    st.markdown("""
                <div style='text-align:center;'> <h2>👤 로그인 </h2><br>
                <p>계정이 없으신가요?<p>
                </div>
                """
                , unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 1, 4])

    with col2:
        if st.button("🆕 신규 사용자"):
            set_page("make_user")
            st.rerun()

        st.markdown("<p style='text-align:center;'>계정이 있으신가요?</p>", unsafe_allow_html=True)

        if st.button("👤기존 사용자"):
            set_page("exist_user")
            st.rerun()

# 사용자 정보 페이지
def user_clicked_page():
    st.markdown("<h2 style='text-align:center;'>👤 사용자 정보 페이지입니다.</h2>", unsafe_allow_html=True)
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()

        # 사용자 리스트 로딩
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
        user_list = df["name"].tolist()
    else:
        user_list = []

    # 세션 상태 초기화
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    if "confirmed_user" not in st.session_state:
        st.session_state.confirmed_user = None

    # 사용자 리스트 렌더링
    for user in user_list:
        # 버튼 렌더링
        if st.button(f"👤 {user}", key=f"user_{user}"):
            st.session_state.selected_user = user
            st.session_state.confirmed_user = None
            # 선택이 바뀌면 확인 초기화
            st.rerun()

        if st.session_state.selected_user == user and not st.session_state.confirmed_user:
            st.markdown(f"<p><strong>{user}</strong> 사용자가 맞습니까?</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ 정보보기", key=f"yes_{user}"):
                    st.session_state.confirmed_user = user
                    set_page("user_info")
                    st.rerun()
            with col2:
                if st.button("❌ 정보 삭제", key=f"no_{user}"):
                    df = pd.read_csv("users.csv")
                    df = df.drop(df[df['name'] == user].index)
                    df.to_csv("users.csv", index=False)
                    st.session_state.selected_user = None
                    st.rerun()

def user_info_page():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()
    df = pd.read_csv("users.csv")

    user = st.session_state.confirmed_user

    st.markdown(f"<h2 style='text-align:center;'> {user}님의 정보입니다. <br> </h2>",unsafe_allow_html=True)
    for idx, row in df.iterrows():
        if row["name"] == user:
            win = row["win"]
            draw = row["draw"]
            lose = row["lose"]

            st.markdown(f"<h3 style='text-align:center;'> 👉 {win}승 {draw}무 {lose}패 👈 </h3>" , unsafe_allow_html=True)
            break

# 종료 페이지
def exit_clicked_page():

    st.markdown("<h2 style='text-align:center;'>👋 앱을 종료합니다. </h2>", unsafe_allow_html=True)
    st.stop()

# 신규 유저 생성 페이지
def make_user_page():
    if st.button("← 뒤로"):
        set_page("game")
        st.rerun()

    # 페이지 제목
    st.markdown("<h2 style='text-align: center;'> 🆕 신규 사용자 등록</h2>", unsafe_allow_html=True)

    with st.form("user_form", clear_on_submit=True):
        user_name = st.text_input("사용자 이름을 입력하세요:")
        submitted = st.form_submit_button("등록")

        if submitted:
            if user_name.strip() == "":
                st.warning("이름을 입력해주세요.")
            elif is_duplicate_user(user_name):
                st.warning(f"'{user_name}' 님은 이미 등록되어 있습니다!")
            else:
                save_user(user_name)
                st.success(f"'{user_name}' 님이 등록되었습니다!")

def exist_user_page():
    if st.button("← 뒤로"):
        set_page("game")
        st.rerun()

    # 사용자 리스트 로딩
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
        user_list = df["name"].tolist()
    else:
        user_list = []

    # 세션 상태 초기화
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    if "confirmed_user" not in st.session_state:
        st.session_state.confirmed_user = None

    st.markdown("<h3 style='text-align:center;'>👥 기존 사용자 선택 <br> </h3>", unsafe_allow_html=True)

    # 사용자 리스트 렌더링
    for user in user_list:
        # 버튼 렌더링
        if st.button(f"👤 {user}", key=f"user_{user}"):
            st.session_state.selected_user = user
            st.session_state.confirmed_user = None  # 선택이 바뀌면 확인 초기화
            st.rerun()

        # 선택된 사용자와 일치할 때만 확인 UI 출력
        if st.session_state.selected_user == user and not st.session_state.confirmed_user:
            st.markdown(f"<p><strong>{user}</strong> 사용자가 맞습니까?</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ 예", key=f"yes_{user}"):
                    st.session_state.confirmed_user = user
                    set_page("ready_game")
                    st.rerun()
            with col2:
                if st.button("❌ 아니오", key=f"no_{user}"):
                    st.session_state.selected_user = None
                    st.rerun()

# 게임 설명 페이지
def ready_game_page():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()

    st.markdown("""<div style='text-align: center;'> <h1> 게임설명 </h1>
                <h4>게임방법</h4>
                <p>1. 플레이어와 AI가 각각 '가위', '바위', '보' 중 하나를 선택합니다.<br>
                2. 10초동안 선택해야하며 10초가 지날시에 자동으로 선택됩니다.<br>
                3. 선택은 캠을 이용한 손 모양 또는 버튼 클릭 으로 이루어집니다.<br>
                4. 선택 결과에 따라 승패가 결정됩니다.<br>
                <h4>게임규칙</h4>
                가위는 보를 이깁니다.<br>
                바위는 가위를 이깁니다.<br>
                보는 바위를 이깁니다.<br>
                같은 선택일 경우 무승부입니다.<br></p>
                </div>""",unsafe_allow_html = True)
    
    left, center, right = st.columns([6, 1, 6])
    with center:
        if st.button("게임 시작"):
            set_page("rcp1")
            st.rerun()
# 본 게임 페이지
def rcp_game_page1():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()

    if "camera" not in st.session_state:
        st.session_state.camera = None 

    if st.session_state.camera is None:
        st.write("<p>웹캠을 사용하시나요?</p>", unsafe_allow_html=True)
        if st.button("사용"):
            st.session_state.camera = True
        if st.button("사용 안함"):
            st.session_state.camera = False
        st.rerun()

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "ai_choice" not in st.session_state:
        st.session_state.ai_choice = None
    if "human_choice" not in st.session_state:
        st.session_state.human_choice = None

    if st.button("게임 시작"):
        st.session_state.start_time = time.time()
        st.session_state.ai_choice = None
        st.session_state.human_choice = None

        if st.session_state.camera is True:
            set_page("rcp4")
        else:
            set_page("rcp2")
        st.rerun()

def rcp_game_page2():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()
        
    remaining = 10
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 10 - elapsed)

    st.markdown(
        f"<p style='text-align: right; font-size: 24px;'>🕒 남은 시간: {remaining}초</p>",
        unsafe_allow_html=True
    )
        
    if st.session_state.start_time is not None:
        top_col1, top_col2 = st.columns([1, 1])

        with top_col1:
            st.markdown("<h3 style='text-align:center;'> Human <br></h3>", unsafe_allow_html=True)
            btn_col1, btn_col2, btn_col3 = st.columns([4, 4, 2])

            if st.session_state.human_choice is None:
                with btn_col1:
                    st.image("images/scissors.jpeg", width=100)
                    if st.button("가위"):
                        st.session_state.human_choice = "scissors"

                with btn_col2:
                    st.image("images/rock.jpeg", width=100)
                    if st.button("바위"):
                        st.session_state.human_choice = "rock"

                with btn_col3:
                    st.image("images/paper.jpeg", width=100)
                    if st.button("보"):
                        st.session_state.human_choice = "paper"
                
                st.empty()
        with top_col2:
            st.markdown("<h3 style='text-align:center;'> AI <br></h3>", unsafe_allow_html=True)

        # 타이머 종료 처리
        if remaining == 0 or st.session_state.human_choice is not None:
            st.session_state.ai_choice = random.choice(["scissors", "rock", "paper"])
            if st.session_state.human_choice is None:
                st.session_state.human_choice = random.choice(["scissors", "rock", "paper"])

            set_page("rcp3")
            st.rerun()


        elif remaining > 0:
            time.sleep(0.5)
            st.rerun()

def choose_image(name):
    if name == "rock":
        return "images/rock.jpeg"
    elif name == "paper":
        return "images/paper.jpeg"
    elif name == "scissors":
        return "images/scissors.jpeg"

def rcp_game_page3():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()
    st.session_state.record_update = False
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align:center;'>Human <br> </h3>", unsafe_allow_html=True)
        left, center, right = st.columns([3, 1, 3])
        with center:
            st.image(choose_image(st.session_state.human_choice), width=100)
        st.markdown(f"<p style='text-align:center;'>🙋‍♂️ {st.session_state.human_choice}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='text-align:center;'>AI <br> </h3>", unsafe_allow_html=True)
        left, center, right = st.columns([3, 1, 3])
        with center:
            st.image(choose_image(st.session_state.ai_choice), width=100)
            st.markdown(f"<p style='text-align:center;'>🤖 {st.session_state.ai_choice}</p>", unsafe_allow_html=True)

    result = judge_win(st.session_state.human_choice, st.session_state.ai_choice)
    st.success(f"🏆 결과: {result}")

    st.session_state.record_update = True
    if st.session_state.record_update == True:
        update_user_record(st.session_state.confirmed_user, result)

    if st.button("계속하기"):
        st.session_state.human_choice = None
        st.session_state.ai_choice = None
        st.session_state.start_time = time.time()  # 타이머 초기화
        st.session_state.record_update = False

        if st.session_state.camera is True:
            set_page("rcp4")
        else:
            set_page("rcp2")
        st.rerun()
        
    if st.button("그만하기"):
        set_page("home")
        st.session_state.record_update = False
        st.rerun()
            
def rcp_game_page4():
    if st.button("← 홈으로"):
        set_page("home")
        st.rerun()

    remaining = 10
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 10 - elapsed)

    st.markdown(
        f"<p style='text-align: right; font-size: 24px;'>🕒 남은 시간: {remaining}초</p>",
        unsafe_allow_html=True
    ) 

    if st.session_state.start_time is not None:
        top_col1, top_col2 = st.columns([1, 1])

    with top_col1:
        st.markdown("<h3 style='text-align:center;'> Human <br></h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'> 웹캠을 켜고 손 모양을 화면에 보여주세요!</p>", unsafe_allow_html=True)

        picture = st.camera_input(" ")

        if picture:
            st.image(picture)

        with top_col2:
            st.markdown("<h3 style='text-align:center;'> AI <br></h3>", unsafe_allow_html=True)

        # 타이머 종료 처리
        if remaining == 0 or st.session_state.human_choice is not None:
            st.session_state.ai_choice = random.choice(["scissors", "rock", "paper"])
            if st.session_state.human_choice is None:
                st.session_state.human_choice = random.choice(["scissors", "rock", "paper"])

            set_page("rcp3")
            st.rerun()


        elif remaining > 0:
            time.sleep(0.5)
            st.rerun()

# 페이지 함수
if st.session_state.page == "home":
    main()
elif st.session_state.page == "game":
    game_clicked_page()
elif st.session_state.page == "user":
    user_clicked_page()
elif st.session_state.page == "exit":
    exit_clicked_page()
elif st.session_state.page == "make_user":
    make_user_page()
elif st.session_state.page == "exist_user":
    exist_user_page()
elif st.session_state.page == "ready_game":
    ready_game_page()
elif st.session_state.page == "rcp1":
    rcp_game_page1()
elif st.session_state.page == "rcp2":
    rcp_game_page2()
elif st.session_state.page == "rcp3":
    rcp_game_page3()
elif st.session_state.page == "rcp4":
    rcp_game_page4()
elif st.session_state.page == "user_info":
    user_info_page()