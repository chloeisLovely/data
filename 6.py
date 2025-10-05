import streamlit as st
import pandas as pd
import altair as alt

# --- 페이지 설정 ---
st.set_page_config(
    page_title="6차시: 미슐랭 스타의 조건 🌟",
    page_icon="🏆",
    layout="wide"
)

# --- 스타일링 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #F0F2F6; /* 고급스러운 느낌을 위해 배경색 변경 */
        font-family: 'Gowun+Dodum', sans-serif;
    }

    /* 헤더 스타일 */
    h1, h2, h3 {
        color: #1E3A8A !important; /* 미슐랭 테마에 맞는 짙은 파란색 */
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
        border: 2px solid #D1D5DB; /* 차분한 회색 테두리 */
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* 노트 스타일 */
    .note {
        background-color: #E0E7FF; /* 파란 계열 노트 */
        border-left: 5px solid #4F46E5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* 비평 박스 스타일 */
    .critique-box {
        background-color: #FFFBEB;
        border: 1px solid #FBBF24;
        padding: 1rem;
        border-radius: 0.5rem;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)


# --- '나쁜 차트' 생성 함수 ---
def create_bad_charts():
    # 1. 정체불명 스테이크 (제목, 범례 없음)
    df1 = pd.DataFrame({'알 수 없는 값': [45, 30, 25]})
    chart1 = alt.Chart(df1).mark_arc().encode(
        theta=alt.Theta(field="알 수 없는 값", type="quantitative")
    ).properties(
        width=250, height=250
    )

    # 2. 고무줄 자 (Y축 시작점이 0이 아님, 축 제목 없음)
    df2 = pd.DataFrame({'항목': ['A제품', 'B제품'], '만족도': [88, 92]})
    chart2 = alt.Chart(df2).mark_bar(width=50).encode(
        x=alt.X('항목', axis=None),
        y=alt.Y('만족도', scale=alt.Scale(domain=[85, 95]), axis=None)
    ).properties(
        width=250, height=250
    )

    # 3. 무지개 폭탄 (의미 없는 현란한 색상)
    df3 = pd.DataFrame({
        '과일': ['사과', '바나나', '딸기', '포도', '오렌지'],
        '판매량': [30, 45, 70, 25, 50]
    })
    chart3 = alt.Chart(df3).mark_bar().encode(
        x='과일',
        y='판매량',
        color=alt.Color('과일', scale=alt.Scale(scheme='rainbow'), legend=None)
    ).properties(
        width=250, height=250
    )
    
    return chart1, chart2, chart3

# --- 헤더 ---
st.markdown('<h1 style="text-align: center; font-size: 3.5rem;">6차시: 미슐랭 스타의 조건 🌟</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #555; margin-bottom: 2rem;">최고의 차트로 설득하라!</p>', unsafe_allow_html=True)


# --- 도입: 미슐랭 심사위원 D의 메시지 ---
with st.container(border=True):
    st.markdown('<div style="text-align:center;">'
                '<div style="font-size: 4rem; margin-bottom: 1rem;">🤵</div>'
                '<h2>미슐랭 심사위원 D의 불시 점검</h2>'
                '<p style="font-size: 1.2rem; text-align: left;">"셰프 탐정단. 지난주, 여러분의 데이터 쿡방 특집은 성공적이었다. 시청자 반응도 뜨거웠지. 하지만... 나는 보통 셰프가 아니다. 오늘은 세상에서 가장 까다로운 \'미슐랭 심사위원 D\'로서 여러분의 주방을 불시에 점검하겠다. 미슐랭 3스타의 조건은 간단하다. <strong>정직함, 친절함, 그리고 아름다움.</strong> 즉, 데이터를 왜곡하지 않고(정직), 누가 봐도 이해하기 쉽게 설명하며(친절), 핵심 메시지를 세련되게 강조하는(아름다움) 것이다. 나의 별점을 받을 자격이 있는지, 증명해 봐라!"</p>'
                '</div>', unsafe_allow_html=True)


# --- 활동 1: '최악의 레스토랑' 메뉴 비평하기 ---
with st.container(border=True):
    st.header("🧐 활동 1: '최악의 레스토랑' 메뉴 비평하기")
    st.write("여러분이 미슐랭 심사위원이라면, 아래 최악의 레스토랑 메뉴판(나쁜 차트 예시)의 문제점은 무엇이고, 어떻게 개선해야 할지 비평 노트를 작성해 보세요.")
    
    chart1, chart2, chart3 = create_bad_charts()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="critique-box"><h4>정체불명 스테이크</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart1, use_container_width=True)
        st.text_area("비평 노트 1", placeholder="예: 요리 이름(제목)이 없어서 무엇에 대한 비율인지 알 수 없어요.", height=150, label_visibility="collapsed")
        
    with col2:
        st.markdown('<div class="critique-box"><h4>고무줄 자</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart2, use_container_width=True)
        st.text_area("비평 노트 2", placeholder="예: 세로축의 시작이 0이 아니라서 차이가 과장되어 보여요. 정직하지 않아요!", height=150, label_visibility="collapsed")

    with col3:
        st.markdown('<div class="critique-box"><h4>무지개 폭탄</h4></div>', unsafe_allow_html=True)
        st.altair_chart(chart3, use_container_width=True)
        st.text_area("비평 노트 3", placeholder="예: 색깔이 너무 많아서 정신없고, 어떤 과일이 중요한지 알 수 없어요.", height=150, label_visibility="collapsed")


# --- 활동 2: '시그니처 디쉬' 업그레이드하기 ---
with st.container(border=True):
    st.header("🛠️ 활동 2: 우리 팀의 '시그니처 디쉬' 업그레이드하기")
    st.write("이제 우리 주방으로 돌아와, 5차시에 만들었던 시그니처 디쉬를 미슐랭 3스타급으로 업그레이드해 봅시다. 아래 업그레이드 체크리스트를 따라 차근차근 수정해 보세요.")
    
    st.subheader("[미슐랭 스타를 위한 업그레이드 체크리스트]")
    st.checkbox("**[제목]** 차트의 제목을 누가 봐도 내용을 알 수 있도록 구체적이고 흥미롭게 수정했나요? (예: 과일 선호도 → [압도적 1위] 우리 반 학생들이 가장 선호하는 과일)")
    st.checkbox("**[축 레이블]** 막대그래프의 세로축(Y축)에 '학생 수(명)'처럼 데이터의 단위를 명확하게 적었나요?")
    st.checkbox("**[색상 강조]** 가장 중요하게 보여주고 싶은 데이터(예: 1등 막대)만 눈에 띄는 다른 색으로 바꾸어 강조했나요?")
    st.checkbox("**[데이터 레이블]** 각 막대나 파이 조각 위에 실제 숫자 값을 표시하여 정확성을 높였나요?")


# --- 활동 3: '코스 요리'로 이야기 만들기 ---
with st.container(border=True):
    st.header("📝 활동 3: '코스 요리'로 이야기 만들기")
    st.write("미슐랭 3스타 레스토랑은 단품 요리 하나만으로 평가받지 않습니다. 전체적인 흐름을 보여주는 코스 요리로 승부하죠. 우리 팀의 주장을 뒷받침할 에피타이저, 메인 디쉬, 디저트, 즉 3개의 업그레이드된 차트를 하나의 코스로 구성해 봅시다.")
    st.markdown('<div class="note">'
                '<h5>🧑‍🍳 처음부터 완벽한 미슐랭 3스타 요리를 만드는 셰프는 없습니다.</h4>'
                '<p>심사위원 D의 피드백을 하나씩 반영하면서, 우리의 요리가 어떻게 명품으로 변신하는지 그 과정을 즐겨봅시다!</p>'
                '</div>', unsafe_allow_html=True)


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

    st.text_area("**오늘의 코스 설명 (셰프의 노트):**", placeholder="이 코스 요리(차트 3개)가 전체적으로 어떤 이야기를 들려주는지 2~3 문장으로 설명해주세요.", height=150)

    if st.button("미슐랭 코스 메뉴판 제출하기!", type="primary", use_container_width=True):
        st.success("원더풀! 미슐랭 3스타를 받기에 충분한 코스 요리입니다! 🌟🌟🌟")
        st.balloons()


# --- 정리 및 다음 차시 예고 ---
with st.container(border=True):
    st.header("📝 정리: 오늘 배운 개념 요약")
    st.markdown("""
    - **좋은 차트의 3대 조건:** 정직함(데이터 왜곡 금지), 친절함(쉬운 설명), 아름다움(핵심 강조)
    - **차트의 3대 필수 요소:** 제목(요리 이름), 축 레이블(단위), 범례(재료 설명)는 반드시 포함해야 함
    - **데이터 강조:** 색상이나 글꼴 크기를 활용하면, 우리가 가장 중요하게 생각하는 메시지를 효과적으로 전달할 수 있음
    """)

st.markdown('<div style="text-align:center; padding: 2rem;">'
            '<h2>👉 다음 차시 예고</h2>'
            '<p style="font-size: 1.2rem; max-width: 800px; margin: auto; color: #333;">"원더풀! 오늘 여러분이 선보인 코스요리들은 모두 미슐랭 3스타를 받기에 충분했습니다. 하지만 진정한 대가는, 아무도 생각지 못한 재료들을 조합하여 세상에 없던 새로운 맛을 창조합니다. 다음 시간에는 우리가 만든 이 완벽한 요리(차트)들을 한 테이블에 올려놓고, 그 조합 속에서만 발견되는 충격적인 비밀 레시피, 즉 데이터 인사이트(Insight)를 찾는 여정을 떠나겠습니다."</p>'
            '</div>', unsafe_allow_html=True)
