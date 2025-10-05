import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="6차시: 미슐랭 스타의 조건 🌟",
    page_icon="🏆",
    layout="wide"
)

# --- 이미지 생성 함수 ---

def wrap_text(text, font, max_width):
    """주어진 너비에 맞게 텍스트를 여러 줄로 나눕니다."""
    lines = []
    if not text:
        return lines
    # 사용자가 입력한 개행을 존중
    for line in text.split('\n'):
        words = line.split(' ')
        while len(words) > 0:
            current_line = ''
            while len(words) > 0 and font.getbbox(current_line + words[0])[2] <= max_width:
                current_line += (words.pop(0) + ' ')
            lines.append(current_line.strip())
    return lines

def create_summary_image_6():
    """세션 상태의 모든 입력을 기반으로 하나의 요약 이미지를 생성합니다."""
    # 폰트 다운로드 및 로드
    font_path = "GowunDodum-Regular.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/gowundodum/GowunDodum-Regular.ttf"
            r = requests.get(url)
            with open(font_path, "wb") as f:
                f.write(r.content)
        except Exception as e:
            st.error(f"폰트를 다운로드하는 데 실패했습니다: {e}")
            return None
    
    try:
        title_font = ImageFont.truetype(font_path, 40)
        header_font = ImageFont.truetype(font_path, 28)
        body_font = ImageFont.truetype(font_path, 20)
        small_font = ImageFont.truetype(font_path, 16)
    except IOError:
        st.error("폰트 파일을 로드할 수 없습니다.")
        return None

    # 렌더링할 콘텐츠 목록 생성
    content = [
        ("데이터 쿡방 6차시 제출 결과", title_font),
        (f"제출 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", body_font),
        ("", body_font),
        ("🧐 활동 1: '최악의 레스토랑' 비평 노트", header_font),
        (f"정체불명 스테이크: {st.session_state.get('critique_1', 'N/A')}", body_font),
        (f"고무줄 자: {st.session_state.get('critique_2', 'N/A')}", body_font),
        (f"무지개 폭탄: {st.session_state.get('critique_3', 'N/A')}", body_font),
        ("", body_font),
        ("🛠️ 활동 2: 업그레이드 체크리스트", header_font),
        (f"[제목]: {'완료' if st.session_state.get('check_title', False) else '미완료'}", body_font),
        (f"[축 레이블]: {'완료' if st.session_state.get('check_axis', False) else '미완료'}", body_font),
        (f"[색상 강조]: {'완료' if st.session_state.get('check_color', False) else '미완료'}", body_font),
        (f"[데이터 레이블]: {'완료' if st.session_state.get('check_datalabel', False) else '미완료'}", body_font),
        ("", body_font),
        ("🎯 챌린지: 미슐랭 3스타 코스 요리", header_font),
        ("오늘의 코스 설명 (셰프의 노트):", body_font),
        (f"{st.session_state.get('course_note', 'N/A')}", small_font),
    ]

    # 이미지 크기 계산
    width = 900
    padding = 40
    line_spacing = 15
    content_width = width - 2 * padding
    
    total_height = padding
    wrapped_content = []
    for text, font in content:
        lines = wrap_text(text, font, content_width)
        for line in lines:
            wrapped_content.append((line, font))
            bbox = font.getbbox(line)
            total_height += (bbox[3] - bbox[1]) + line_spacing

    # 업로드된 3개 이미지 공간 추가
    course_images = {
        '에피타이저': st.session_state.get('appetizer'),
        '메인 디쉬': st.session_state.get('main_dish'),
        '디저트': st.session_state.get('dessert'),
    }
    
    img_section_height = 0
    img_placeholder_height = 100 # 이미지가 없을 경우의 높이
    
    for title, img_file in course_images.items():
        if img_file:
            try:
                user_img = Image.open(img_file)
                # 이미지 크기를 3:2 비율 정도로 고정
                img_width = content_width // 3 - 10
                img_height = int(img_width * 0.66)
                img_section_height = max(img_section_height, img_height + 40) # 제목 공간 포함
            except Exception:
                pass # 손상된 파일
    
    if img_section_height == 0:
        img_section_height = img_placeholder_height
        
    total_height += img_section_height + padding
        
    total_height += padding

    # 이미지 생성 및 텍스트 그리기
    img = Image.new('RGB', (width, total_height), '#F0F2F6')
    draw = ImageDraw.Draw(img)
    
    y = padding
    for text, font in wrapped_content:
        draw.text((padding, y), text, font=font, fill='#1E3A8A')
        bbox = font.getbbox(text)
        y += (bbox[3] - bbox[1]) + line_spacing
    
    # 업로드된 코스 이미지 그리기
    y += padding
    current_x = padding
    
    for title, img_file in course_images.items():
        img_width = content_width // 3 - 10
        img_height = int(img_width * 0.66)
        
        # 제목 그리기
        draw.text((current_x, y), title, font=body_font, fill='#1E3A8A')
        
        if img_file:
            try:
                user_img = Image.open(img_file)
                user_img_resized = user_img.resize((img_width, img_height))
                img.paste(user_img_resized, (current_x, y + 40))
            except Exception as e:
                draw.rectangle([current_x, y + 40, current_x + img_width, y + 40 + img_height], outline="red", width=2)
                draw.text((current_x + 10, y + 50), "이미지 오류", font=small_font, fill="red")
        else:
             draw.rectangle([current_x, y + 40, current_x + img_width, y + 40 + img_height], outline="#ccc", width=1)
             draw.text((current_x + 10, y + 50), "이미지 없음", font=small_font, fill="#999")
        
        current_x += img_width + 15
        
    # 이미지를 바이트로 변환
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# --- 스타일링 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    .stApp { background-color: #F0F2F6; font-family: 'Gowun+Dodum', sans-serif; }
    h1, h2, h3 { color: #1E3A8A !important; font-weight: bold !important; }
    .main .block-container { max-width: 950px !important; margin: 0 auto !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border: 2px solid #D1D5DB; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
    .note { background-color: #E0E7FF; border-left: 5px solid #4F46E5; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    .critique-box { background-color: #FFFBEB; border: 1px solid #FBBF24; padding: 1rem; border-radius: 0.5rem; height: 100%; }
</style>
""", unsafe_allow_html=True)

# --- '나쁜 차트' 생성 함수 ---
def create_bad_charts():
    df1 = pd.DataFrame({'값': [45, 30, 25]})
    chart1 = alt.Chart(df1).mark_arc().encode(theta=alt.Theta(field="값", type="quantitative")).properties(width=250, height=250)
    df2 = pd.DataFrame({'항목': ['A제품', 'B제품'], '만족도': [88, 92]})
    chart2 = alt.Chart(df2).mark_bar(width=50).encode(x=alt.X('항목', axis=None), y=alt.Y('만족도', scale=alt.Scale(domain=[85, 95]), axis=None)).properties(width=250, height=250)
    df3 = pd.DataFrame({'과일': ['사과', '바나나', '딸기', '포도', '오렌지'], '판매량': [30, 45, 70, 25, 50]})
    chart3 = alt.Chart(df3).mark_bar().encode(x='과일', y='판매량', color=alt.Color('과일', scale=alt.Scale(scheme='rainbow'), legend=None)).properties(width=250, height=250)
    return chart1, chart2, chart3

# --- 헤더 ---
st.markdown('<h1 style="text-align: center; font-size: 3.5rem;">6차시: 미슐랭 스타의 조건 🌟</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #555; margin-bottom: 2rem;">최고의 차트로 설득하라!</p>', unsafe_allow_html=True)

# --- 도입 ---
with st.container(border=True):
    st.markdown('<div style="text-align:center;"><div style="font-size: 4rem; margin-bottom: 1rem;">🤵</div><h2>미슐랭 심사위원 D의 불시 점검</h2><p style="font-size: 1.2rem; text-align: left;">"셰프 탐정단. ... <strong>정직함, 친절함, 그리고 아름다움.</strong> ... 나의 별점을 받을 자격이 있는지, 증명해 봐라!"</p></div>', unsafe_allow_html=True)

# --- 활동 1 ---
with st.container(border=True):
    st.header("🧐 활동 1: '최악의 레스토랑' 메뉴 비평하기")
    st.write("여러분이 미슐랭 심사위원이라면, 아래 최악의 레스토랑 메뉴판(나쁜 차트 예시)의 문제점은 무엇이고, 어떻게 개선해야 할지 비평 노트를 작성해 보세요.")
    chart1, chart2, chart3 = create_bad_charts()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="critique-box"><h4>정체불명 스테이크</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart1, use_container_width=True)
        st.text_area("비평 노트 1", placeholder="예: 요리 이름(제목)이 없어서...", height=150, label_visibility="collapsed", key="critique_1")
    with col2:
        st.markdown('<div class="critique-box"><h4>고무줄 자</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart2, use_container_width=True)
        st.text_area("비평 노트 2", placeholder="예: 세로축의 시작이 0이 아니라서...", height=150, label_visibility="collapsed", key="critique_2")
    with col3:
        st.markdown('<div class="critique-box"><h4>무지개 폭탄</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart3, use_container_width=True)
        st.text_area("비평 노트 3", placeholder="예: 색깔이 너무 많아서 정신없고...", height=150, label_visibility="collapsed", key="critique_3")

# --- 활동 2 ---
with st.container(border=True):
    st.header("🛠️ 활동 2: 우리 팀의 '시그니처 디쉬' 업그레이드하기")
    st.write("이제 우리 주방으로 돌아와, 5차시에 만들었던 시그니처 디쉬를 미슐랭 3스타급으로 업그레이드해 봅시다. 아래 업그레이드 체크리스트를 따라 차근차근 수정해 보세요.")
    st.subheader("[미슐랭 스타를 위한 업그레이드 체크리스트]")
    st.checkbox("**[제목]**", key="check_title")
    st.checkbox("**[축 레이블]**", key="check_axis")
    st.checkbox("**[색상 강조]**", key="check_color")
    st.checkbox("**[데이터 레이블]**", key="check_datalabel")

# --- 활동 3 ---
with st.container(border=True):
    st.header("📝 활동 3: '코스 요리'로 이야기 만들기")
    st.write("미슐랭 3스타 레스토랑은 단품 요리 하나만으로 평가받지 않습니다. 전체적인 흐름을 보여주는 코스 요리로 승부하죠. 우리 팀의 주장을 뒷받침할 에피타이저, 메인 디쉬, 디저트, 즉 3개의 업그레이드된 차트를 하나의 코스로 구성해 봅시다.")
    st.markdown('<div class="note"><h5>🧑‍🍳 처음부터 완벽한 미슐랭 3스타 요리를 만드는 셰프는 없습니다.</h4><p>심사위원 D의 피드백을 하나씩 반영하면서, 우리의 요리가 어떻게 명품으로 변신하는지 그 과정을 즐겨봅시다!</p></div>', unsafe_allow_html=True)

# --- 문제 챌린지 ---
with st.container(border=True):
    st.header("🎯 오늘의 챌린지: '미슐랭 3스타 코스 요리' 선보이기")
    st.write("여러분의 핵심 주장을 뒷받침하는 에피타이저, 메인 디쉬, 디저트, 즉 3개의 업그레이드된 차트를 코스로 구성하여 미슐랭 코스 메뉴판을 제출해 주십시오.")
    st.subheader("[데이터 쿡방: 미슐랭 3스타 코스]")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.file_uploader("**에피타이저 (차트 1):**", type=['png', 'jpg', 'jpeg'], key="appetizer")
    with c2:
        st.file_uploader("**메인 디쉬 (차트 2):**", type=['png', 'jpg', 'jpeg'], key="main_dish")
    with c3:
        st.file_uploader("**디저트 (차트 3):**", type=['png', 'jpg', 'jpeg'], key="dessert")
    st.text_area("**오늘의 코스 설명 (셰프의 노트):**", placeholder="이 코스 요리(차트 3개)가 전체적으로 어떤 이야기를 들려주는지...", height=150, key="course_note")
    
    if st.button("제출 내용으로 이미지 생성하기", type="primary", use_container_width=True):
        with st.spinner("결과 이미지를 생성 중입니다... 🎨"):
            image_bytes = create_summary_image_6()
            if image_bytes:
                st.session_state.generated_image_6 = image_bytes
            else:
                st.error("이미지 생성에 실패했습니다.")

    if 'generated_image_6' in st.session_state and st.session_state.generated_image_6:
        st.success("이미지 생성이 완료되었습니다! 아래 버튼으로 다운로드하세요.")
        st.download_button(
            label="결과 이미지 다운로드하기 🖼️",
            data=st.session_state.generated_image_6,
            file_name="데이터쿡방_6차시_결과.png",
            mime="image/png",
            use_container_width=True
        )

# --- 정리 및 다음 차시 예고 ---
with st.container(border=True):
    st.header("📝 정리: 오늘 배운 개념 요약")
    st.markdown("""
    - **좋은 차트의 3대 조건:** 정직함(데이터 왜곡 금지), 친절함(쉬운 설명), 아름다움(핵심 강조)
    - **차트의 3대 필수 요소:** 제목(요리 이름), 축 레이블(단위), 범례(재료 설명)는 반드시 포함해야 함
    - **데이터 강조:** 색상이나 글꼴 크기를 활용하면, 우리가 가장 중요하게 생각하는 메시지를 효과적으로 전달할 수 있음
    """)

st.markdown('<div style="text-align:center; padding: 2rem;"><h2>👉 다음 차시 예고</h2><p style="font-size: 1.2rem; max-width: 800px; margin: auto; color: #333;">"원더풀! ... 다음 시간에는 우리가 만든 이 완벽한 요리(차트)들을 한 테이블에 올려놓고, 그 조합 속에서만 발견되는 충격적인 비밀 레시피, 즉 데이터 인사이트(Insight)를 찾는 여정을 떠나겠습니다."</p></div>', unsafe_allow_html=True)

