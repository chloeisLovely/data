import streamlit as st
import pandas as pd
import altair as alt
import re
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="5차시: 데이터 쿡방 특집 🍳",
    page_icon="📊",
    layout="wide"
)

# --- Google Sheets 연동 함수 ---
def save_to_google_sheets():
    # Streamlit secrets에 인증 정보가 있는지 먼저 확인
    if "gcp_service_account" not in st.secrets:
        st.error("⚠️ Google Sheets 연동을 위한 **Secrets** 설정이 필요합니다.")
        st.info(
            """
            **관리자 안내:**
            1. Google Cloud Platform에서 서비스 계정 키(JSON)를 다운로드하세요.
            2. Streamlit 앱 폴더에 `.streamlit/secrets.toml` 파일을 생성하세요.
            3. `secrets.toml` 파일에 아래와 같이 키 내용을 붙여넣으세요:
            ```toml
            [gcp_service_account]
            type = "service_account"
            project_id = "..."
            private_key_id = "..."
            private_key = "..."
            client_email = "..."
            client_id = "..."
            auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
            token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
            auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
            client_x509_cert_url = "..."
            ```
            4. 앱을 재실행하면 Google Sheets에 데이터가 저장됩니다.
            """
        )
        return

    try:
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = gspread.authorize(creds)
        spreadsheet = client.open("데이터 쿡방 5차시 제출 결과")
        sheet = spreadsheet.worksheet("제출 기록")
    except Exception as e:
        st.error(f"⚠️ Google Sheets에 연결할 수 없습니다. 관리자에게 문의하세요.")
        st.error(f"오류 상세: {e}")
        return

    header = [
        "제출 시각", "활동1_데이터제목", "활동1_입력데이터", "활동1_선택차트", "활동1_선택이유",
        "활동2A_선택", "활동2A_이유", "활동2B_선택", "활동2B_이유",
        "챌린지_요리이름", "챌린지_이미지파일명", "챌린지_셰프의한마디"
    ]
    
    if not sheet.get_all_values():
        sheet.append_row(header)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_info = st.session_state.get('challenge_image', None)
    image_filename = image_info.name if image_info else "업로드 안됨"

    row_to_add = [
        timestamp,
        st.session_state.get("activity1_title", ""),
        st.session_state.get("activity1_data", ""),
        st.session_state.get("activity1_chart_type", ""),
        st.session_state.get("activity1_reason", ""),
        st.session_state.get("mission_a_chart", ""),
        st.session_state.get("mission_a_reason", ""),
        st.session_state.get("mission_b_chart", ""),
        st.session_state.get("mission_b_reason", ""),
        st.session_state.get("challenge_title", ""),
        image_filename,
        st.session_state.get("challenge_comment", "")
    ]
    
    try:
        sheet.append_row(row_to_add)
        st.success("멋진 시그니처 디쉬가 완성되었군요! Google Sheets에 성공적으로 제출되었습니다! 👨‍🍳👩‍🍳")
        st.balloons()
    except Exception as e:
        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")


# --- 스타일링 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    .stApp {
        background-color: #FFF8F0;
        font-family: 'Gowun+Dodum', sans-serif;
    }
    h1, h2, h3 {
        color: #D2691E !important;
        font-weight: bold !important;
    }
    .main .block-container {
        max-width: 950px !important;
        margin: 0 auto !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 2px solid #FFDABA;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .note {
        background-color: #FFF5E1;
        border-left: 5px solid #FFC04D;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .scene-box {
        background-color: #fafafa;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 0.5rem;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 헤더 ---
st.markdown('<h1 style="text-align: center; font-size: 3.5rem;">5차시: 데이터 쿡방 특집 🍳</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #555; margin-bottom: 2rem;">최고의 시그니처 디쉬를 선보여라!</p>', unsafe_allow_html=True)

# --- 도입 ---
with st.container(border=True):
    st.markdown('<div style="text-align:center;">'
                '<div style="font-size: 4rem; margin-bottom: 1rem;">👨‍🍳</div>'
                '<h2>탐정 D의 다섯 번째 메시지</h2>'
                '<p style="font-size: 1.2rem; text-align: left;">"크리에이터 탐정단! ... 최고의 셰프는 최고의 재료를 가지고 최고의 \'요리\'를 만든다. 그리고 그 요리의 가치를 결정하는 마지막 단계가 바로 <strong>플레이팅(Plating)</strong>, 즉 접시에 음식을 아름답게 담아내는 기술이다."</p>'
                '</div>', unsafe_allow_html=True)

# --- 활동 1 ---
with st.container(border=True):
    st.header("🧐 활동 1: '맛없는 쿡방' vs '맛있는 쿡방'")
    st.write("여러분이 시청자라면 어떤 쿡방 채널을 구독하시겠습니까? 아래 두 쿡방 장면을 보고, 왜 B장면이 훨씬 더 이해하기 쉽고 재미있는지 우리 팀의 생각을 적어봅시다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="scene-box">'
                    '<h4>A장면: 맛없는 쿡방 (재료 목록)</h4>'
                    '</div>', unsafe_allow_html=True)
        st.text_input("데이터의 제목을 입력하세요.", value="가장 좋아하는 과목", key="activity1_title")
        raw_data = st.text_area(
            "데이터를 '항목: 값' 형식으로 입력하세요.",
            height=225,
            value="국어: 15\n수학: 10\n사회: 20\n과학: 25\n체육: 30",
            key="activity1_data"
        )

    with col2:
        st.markdown('<div class="scene-box">'
                    '<h4>B장면: 맛있는 쿡방 (완성된 요리)</h4>'
                    '</div>', unsafe_allow_html=True)
        
        data_lines = st.session_state.activity1_data.strip().split('\n')
        parsed_data = []
        for line in data_lines:
            parts = re.split(r'[:\s,]+', line.strip())
            if len(parts) >= 2:
                item = parts[0].strip()
                try:
                    value = float(parts[-1].strip())
                    parsed_data.append((item, value))
                except (ValueError, IndexError):
                    pass
        
        if parsed_data:
            df = pd.DataFrame(parsed_data, columns=['항목', '값'])
            chart_type = st.radio(
                "원하는 차트 레시피를 선택하세요",
                ("막대 그래프", "선 그래프", "파이 그래프"),
                horizontal=True,
                key="activity1_chart_type"
            )
            if chart_type == "막대 그래프":
                st.bar_chart(df.set_index('항목'), color="#ff8c00")
            elif chart_type == "선 그래프":
                st.line_chart(df.set_index('항목'), color="#007bff")
            elif chart_type == "파이 그래프":
                c = alt.Chart(df).mark_arc().encode(
                    theta=alt.Theta(field="값", type="quantitative"),
                    color=alt.Color(field="항목", type="nominal", title="항목"),
                    tooltip=['항목', '값']
                ).properties(title=st.session_state.activity1_title)
                st.altair_chart(c, use_container_width=True)
        else:
            st.warning("차트를 그리려면 '항목: 값' 형식으로 유효한 데이터를 입력해주세요.")

    st.subheader("B장면(차트)이 더 좋은 이유는?")
    st.text_area("B장면이 더 좋은 이유", placeholder="예: 숫자를 읽지 않아도 어떤 과목이 가장 인기 있는지 막대의 길이만 보고 바로 알 수 있어요!", key="activity1_reason")

# --- 활동 2 ---
with st.container(border=True):
    st.header("🛠️ 활동 2: 최고의 레시피(차트) 선택하기")
    st.write("모든 요리에 같은 레시피를 쓸 수는 없습니다...")
    st.subheader("미션 A: 가장 인기 있는 급식 메뉴 Top 5")
    st.info('"가장 인기 있는 급식 메뉴 Top 5의 순위를 한눈에 비교하고 싶다."')
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.radio("어떤 레시피를 선택할까?", ["막대 차트", "원 차트"], key="mission_a_chart", horizontal=True)
    with a_col2:
        st.text_input("그 레시피를 선택한 이유는?", placeholder="예: 여러 메뉴의 인기도를 '키재기'처럼 비교해야 하니까", key="mission_a_reason")
    st.divider()
    st.subheader("미션 B: 우리 반 학생들의 남녀 성비")
    st.info('"우리 반 학생들의 남녀 성비를 보여주고 싶다."')
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.radio("어떤 레시피를 선택할까?", ["막대 차트", "원 차트"], key="mission_b_chart", horizontal=True)
    with b_col2:
        st.text_input("그 레시피를 선택한 이유는?", placeholder="예: 전체에서 남학생과 여학생이 차지하는 비율을 봐야 하니까", key="mission_b_reason")

# --- 활동 3 ---
with st.container(border=True):
    st.header("📝 활동 3: 나의 첫 '시그니처 디쉬' 만들기")
    st.write("이제 레시피를 정했으니, 직접 요리를 시작할 시간입니다! ...")
    st.markdown('<div class="note"><h5>🧑‍🍳 모든 위대한 셰프의 첫 요리가 완벽하지는 않았습니다!</h4><p>오늘 우리의 첫 시그니처 디쉬가 조금 서툴러도 괜찮습니다. ...</p></div>', unsafe_allow_html=True)
    st.subheader("[요리 순서]")
    st.markdown("1. **4차시 정제된 데이터 시트**를 엽니다. ...")

# --- 문제 챌린지 ---
with st.container(border=True):
    st.header("🎯 오늘의 챌린지: '셰프 특선 요리' 선보이기")
    st.write("훌륭한 요리가 완성되었습니다! ...")
    st.subheader("[데이터 쿡방: 오늘의 시그니처 디쉬]")
    st.text_input("**요리(차트) 이름:**", placeholder="예: 반박불가! 우리 학교 급식의 제왕", key="challenge_title")
    st.file_uploader("**플레이팅(차트 이미지):**", type=['png', 'jpg', 'jpeg'], key="challenge_image")
    if st.session_state.get('challenge_image', None) is not None:
        st.image(st.session_state.challenge_image, caption="업로드된 시그니처 디쉬 ✨", use_column_width=True)
    st.text_area("**셰프의 한 마디 (차트 설명):**", placeholder="예: 이 요리는 ...", key="challenge_comment")
    if st.button("쿡방 예고편 제출하기!", type="primary", use_container_width=True):
        save_to_google_sheets()

# --- 정리 및 다음 차시 예고 ---
with st.container(border=True):
    st.header("📝 정리: 오늘 배운 개념 요약")
    st.markdown("- **데이터 시각화:** ...\n- **막대 차트:** ...\n- **원 차트:** ...")
st.markdown('<div style="text-align:center; padding: 2rem;">'
            '<h2>👉 다음 차시 예고</h2>'
            '<p style="font-size: 1.2rem; ...">"브라보, 셰프 크리에이터 여러분! ..."</p>'
            '</div>', unsafe_allow_html=True)
