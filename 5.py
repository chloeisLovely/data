import streamlit as st
import pandas as pd
import altair as alt
import re

# --- 페이지 설정 ---
st.set_page_config(
    page_title="5차시: 데이터 쿡방 특집 🍳",
    page_icon="📊",
    layout="wide"
)

# --- 스타일링 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #FFF8F0;
        font-family: 'Gowun+Dodum', sans-serif;
    }

    /* 헤더 스타일 */
    h1, h2, h3 {
        color: #D2691E !important;
        font-weight: bold !important;
    }

    /* 콘텐츠를 중앙에 정렬하고 중간 너비 설정 */
    .main .block-container {
        max-width: 950px !important;
        margin: 0 auto !important; /* 중앙 정렬 */
    }

    /* st.container(border=True)에 대한 커스텀 스타일 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 2px solid #FFDABA;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* 노트 스타일 */
    .note {
        background-color: #FFF5E1;
        border-left: 5px solid #FFC04D;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* 장면 비교 스타일 */
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


# --- 도입: 탐정 D의 메시지 ---
with st.container(border=True):
    st.markdown('<div style="text-align:center;">'
                '<div style="font-size: 4rem; margin-bottom: 1rem;">👨‍🍳</div>'
                '<h2>탐정 D의 다섯 번째 메시지</h2>'
                '<p style="font-size: 1.2rem; text-align: left;">"크리에이터 탐정단! 지난 시간, 여러분이 보여준 재료 손질(데이터 정제) 능력은 실로 놀라웠다. 덕분에 우리 쿡방 스튜디오는 지금, 세상에서 가장 신선하고 깨끗한 최상급 재료들로 가득 차 있다. 하지만... 아무도 생감자와 날고기를 그대로 먹지는 않지. 최고의 셰프는 최고의 재료를 가지고 최고의 \'요리\'를 만든다. 그리고 그 요리의 가치를 결정하는 마지막 단계가 바로 <strong>플레이팅(Plating)</strong>, 즉 접시에 음식을 아름답게 담아내는 기술이다."</p>'
                '</div>', unsafe_allow_html=True)


# --- 활동 1: 시각화의 힘 체험하기 ---
with st.container(border=True):
    st.header("🧐 활동 1: '맛없는 쿡방' vs '맛있는 쿡방'")
    st.write("여러분이 시청자라면 어떤 쿡방 채널을 구독하시겠습니까? 아래 두 쿡방 장면을 보고, 왜 B장면이 훨씬 더 이해하기 쉽고 재미있는지 우리 팀의 생각을 적어봅시다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="scene-box">'
                    '<h4>A장면: 맛없는 쿡방 (재료 목록)</h4>'
                    '<p><strong>[가장 좋아하는 과목]</strong></p>'
                    '</div>', unsafe_allow_html=True)
        raw_data = st.text_area(
            "데이터를 '항목: 값' 형식으로 입력하세요.",
            height=260,
            value="국어: 15\n수학: 10\n사회: 20\n과학: 25\n체육: 30",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="scene-box">'
                    '<h4>B장면: 맛있는 쿡방 (완성된 요리)</h4>'
                    '</div>', unsafe_allow_html=True)
        
        # 데이터 파싱
        data_lines = raw_data.strip().split('\n')
        parsed_data = []
        for line in data_lines:
            # ':' 또는 ','를 구분자로 사용하고, 공백을 제거
            parts = re.split(r'[:\s,]+', line.strip())
            if len(parts) >= 2:
                item = parts[0].strip()
                try:
                    # 마지막 부분을 숫자로 변환
                    value = float(parts[-1].strip())
                    parsed_data.append((item, value))
                except (ValueError, IndexError):
                    pass # 숫자 변환 실패 시 해당 라인 무시
        
        if parsed_data:
            df = pd.DataFrame(parsed_data, columns=['항목', '값'])
            
            chart_type = st.radio(
                "원하는 차트 레시피를 선택하세요",
                ("막대 그래프", "선 그래프", "파이 그래프"),
                horizontal=True
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
                ).properties(
                    title='항목별 비율'
                )
                st.altair_chart(c, use_container_width=True)
        else:
            st.warning("차트를 그리려면 '항목: 값' 형식으로 유효한 데이터를 입력해주세요.")

    st.subheader("B장면(차트)이 더 좋은 이유는?")
    st.text_area("B장면이 더 좋은 이유", placeholder="예: 숫자를 읽지 않아도 어떤 과목이 가장 인기 있는지 막대의 길이만 보고 바로 알 수 있어요!", label_visibility="collapsed")


# --- 활동 2: 최고의 레시피(차트) 선택하기 ---
with st.container(border=True):
    st.header("🛠️ 활동 2: 최고의 레시피(차트) 선택하기")
    st.write("모든 요리에 같은 레시피를 쓸 수는 없습니다. 보여주고 싶은 내용에 맞는 최고의 레시피(차트)를 골라야 하죠. 아래 두 가지 쿡방 미션에 어떤 레시피가 어울릴지 우리 팀의 의견을 정하고, 그 이유를 적어봅시다.")

    # 미션 A
    st.subheader("미션 A: 가장 인기 있는 급식 메뉴 Top 5")
    st.info('"가장 인기 있는 급식 메뉴 Top 5의 순위를 한눈에 비교하고 싶다."')
    
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.radio("어떤 레시피를 선택할까?", ["막대 차트", "원 차트"], key="mission_a_chart", horizontal=True)
    with a_col2:
        st.text_input("그 레시피를 선택한 이유는?", placeholder="예: 여러 메뉴의 인기도를 '키재기'처럼 비교해야 하니까", key="mission_a_reason")

    st.divider()

    # 미션 B
    st.subheader("미션 B: 우리 반 학생들의 남녀 성비")
    st.info('"우리 반 학생들의 남녀 성비를 보여주고 싶다."')
    
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.radio("어떤 레시피를 선택할까?", ["막대 차트", "원 차트"], key="mission_b_chart", horizontal=True)
    with b_col2:
        st.text_input("그 레시피를 선택한 이유는?", placeholder="예: 전체에서 남학생과 여학생이 차지하는 비율을 봐야 하니까", key="mission_b_reason")

# --- 활동 3: 나의 첫 '시그니처 디쉬' 만들기 ---
with st.container(border=True):
    st.header("📝 활동 3: 나의 첫 '시그니처 디쉬' 만들기")
    st.write("이제 레시피를 정했으니, 직접 요리를 시작할 시간입니다! 4차시에 손질한 우리 팀의 데이터에서, 시청자들에게 가장 보여주고 싶은 하이라이트 장면 하나를 정하고, 그에 맞는 레시피(차트)로 요리해 보세요.")
    
    st.markdown('<div class="note">'
                '<h5>🧑‍🍳 모든 위대한 셰프의 첫 요리가 완벽하지는 않았습니다!</h4>'
                '<p>오늘 우리의 첫 시그니처 디쉬가 조금 서툴러도 괜찮습니다. 일단 자신감 있게 데이터라는 재료를 볶고 끓여서, 세상에 없는 우리만의 첫 요리를 만들어 봅시다!</p>'
                '</div>', unsafe_allow_html=True)

    st.subheader("[요리 순서]")
    st.markdown("""
    1.  **4차시 정제된 데이터 시트**를 엽니다.
    2.  차트로 만들고 싶은 **데이터 범위를 마우스로 선택**합니다. (예: 메뉴 이름과 응답 개수)
    3.  상단 메뉴에서 **[삽입] > [차트]**를 클릭합니다.
    4.  차트 편집기에서 우리가 선택한 레시피(**막대** 또는 **원 차트**)가 맞는지 확인하고, 필요하다면 수정합니다.
    """)

# --- 문제 챌린지 ---
with st.container(border=True):
    st.header("🎯 오늘의 챌린지: '셰프 특선 요리' 선보이기")
    st.write("훌륭한 요리가 완성되었습니다! 이제 시청자들에게 이 요리가 어떤 요리인지 설명해야겠죠. 구글 시트에 `5차시_시그니처디쉬`라는 새 탭을 만들고, 여러분의 첫 시그니처 디쉬를 멋지게 플레이팅하여 쿡방 예고편으로 제출해 주십시오.")

    st.subheader("[데이터 쿡방: 오늘의 시그니처 디쉬]")
    
    st.text_input("**요리(차트) 이름:**", placeholder="예: 반박불가! 우리 학교 급식의 제왕")
    
    uploaded_file = st.file_uploader("**플레이팅(차트 이미지):** (방금 만든 차트를 복사/캡쳐하여 업로드)", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 시그니처 디쉬 ✨", use_column_width=True)

    st.text_area("**셰프의 한 마디 (차트 설명):**", placeholder="예: 이 요리는 우리 학교 학생 절반이 다른 어떤 메뉴보다 '돈까스'를 압도적으로 사랑한다는 사실을 담고 있습니다.")

    if st.button("쿡방 예고편 제출하기!", type="primary", use_container_width=True):
        st.success("멋진 시그니처 디쉬가 완성되었군요! 다음 쿡방이 기대됩니다! 👨‍🍳👩‍🍳")
        st.balloons()


# --- 정리 및 다음 차시 예고 ---
with st.container(border=True):
    st.header("📝 정리: 오늘 배운 개념 요약")
    st.markdown("""
    - **데이터 시각화:** 숫자 목록(재료)을 한눈에 이해할 수 있는 차트(요리)로 만드는 과정. 최고의 **플레이팅** 기술!
    - **막대 차트:** 여러 항목의 크기나 순위를 비교할 때 사용하는 **'인기 메뉴 TOP 5'** 레시피.
    - **원 차트:** 전체에서 각 항목이 차지하는 비율을 보여줄 때 사용하는 **'레시피 재료 비율'** 레시피.
    """)

st.markdown('<div style="text-align:center; padding: 2rem;">'
            '<h2>👉 다음 차시 예고</h2>'
            '<p style="font-size: 1.2rem; max-width: 800px; margin: auto; color: #333;">"브라보, 셰프 크리에이터 여러분! 여러분의 주방에서 맛있는 통찰력이 담긴 첫 요리가 탄생했습니다. 하지만 자세히 보니, 몇몇 요리에는 이름표(제목)가 빠져있고, 재료 설명(범례)이 조금 헷갈리기도 합니다. 훌륭한 요리지만, 아직 구독자 100만 채널의 퀄리티는 아닌 것 같군요. 다음 시간에는 우리의 요리를 평범한 맛집 수준에서, 누구도 따라올 수 없는 미슐랭 3스타급 명품 요리로 업그레이드하는 비법을 배우겠습니다. 모두 다음 쿡방을 기대하십시오!"</p>'
            '</div>', unsafe_allow_html=True)
