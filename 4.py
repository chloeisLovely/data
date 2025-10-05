import streamlit as st
import re

# --- 페이지 설정 ---
# 레이아웃을 'wide'로 설정하여 가로 폭을 넓게 사용합니다.
st.set_page_config(
    page_title="데이터 쿡방 스튜디오 🍳",
    page_icon="🍳",
    layout="wide"
)

# --- 스타일링 ---
# 원본 HTML의 CSS를 Streamlit에 맞게 일부 수정하여 적용합니다.
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

    /* 콘텐츠를 중앙에 정렬하고 최대 너비 설정 */
    .main .block-container {
        max-width: 800px !important; /* 너비를 중간값으로 조정 */
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: 0 auto; /* 중앙 정렬을 위해 추가 */
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
    
    /* 코드 블록 스타일 */
     code {
        background-color: #FDF2E2;
        color: #B45309;
        padding: 0.2em 0.4em;
        margin: 0;
        font-size: 85%;
        border-radius: 6px;
    }

    /* 헤더 애니메이션 */
    @keyframes bounce {
        0%, 100% {
            transform: translateY(-5%);
            animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
        }
        50% {
            transform: translateY(0);
            animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
        }
    }
    .bouncing-header {
        animation: bounce 1s infinite;
    }

</style>
""", unsafe_allow_html=True)


# --- 세션 상태 초기화 ---
# Streamlit은 스크립트를 재실행하므로, 상태를 유지하기 위해 session_state를 사용합니다.
if 'example_type' not in st.session_state:
    st.session_state.example_type = None
if 'cleaning_rules' not in st.session_state:
    st.session_state.cleaning_rules = [{"find": "떠뽀끼", "replace": "떡볶이"}]

# --- 헤더 ---
st.markdown('<h1 class="bouncing-header" style="text-align: center; font-size: 3.5rem;">데이터 쿡방 스튜디오 🍳</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #555; margin-bottom: 2rem;">최고의 재료(데이터)를 손질하여 명품 요리(분석)를 만들어봐요!</p>', unsafe_allow_html=True)


# --- 소개 ---
with st.container(border=True):
    st.markdown('<div style="text-align:center;">'
                '<div style="font-size: 4rem; margin-bottom: 1rem;">📢</div>'
                '<h2>탐정 D의 긴급 속보!</h2>'
                '<p style="font-size: 1.2rem;">"크리에이터 탐정단! 여러분의 설문지가 대성공을 거뒀다! 이제 시청자들이 보내준 뜨거운 반응(데이터)을 가지고, \'데이터 쿡방\'을 시작할 시간이다! 최고의 요리는 최고의 재료 손질에서 시작되지. 자, 다 함께 재료를 손질해볼까?"</p>'
                '</div>', unsafe_allow_html=True)


# --- 활동 1: 재료 창고 탐색 ---
with st.container(border=True):
    st.header("🧐 활동 1: 재료 창고(구글 시트) 탐색하기")
    st.write("우리 쿡방 스튜디오의 재료 창고를 열어봅시다. 어떤 '손질이 필요한 재료'들이 도착했는지 탐색하고, 아래 [탐색 노트]에 발견한 것들을 적어보세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🥔 흙 묻은 감자 (오타)", use_container_width=True):
            st.session_state.example_type = 'potato'
    with col2:
        if st.button("🥕 제멋대로 당근 (다른 표현)", use_container_width=True):
            st.session_state.example_type = 'carrot'
    with col3:
        if st.button("💎 섞여 들어온 돌멩이 (무의미 데이터)", use_container_width=True):
            st.session_state.example_type = 'stone'
    
    examples = {
        'potato': "앗! '김치찌게' 발견! '김치찌개'로 고쳐야겠어요.",
        'carrot': "오잉? '돈까스'도 있고 '돈까쓰'도 있네요. 하나로 통일해야겠어요!",
        'stone': "이런! 'ㅋㅋㅋ'라고만 적은 답변이 있어요. 요리엔 쓸 수 없겠네요."
    }
    
    if st.session_state.example_type:
        st.info(f"**발견!** {examples[st.session_state.example_type]}")

    st.subheader("[탐색 노트]")
    st.text_area("여기에 발견한 '손질이 필요한 재료'들을 자유롭게 적어보세요!", key="exploration_notes", height=150, label_visibility="collapsed")

# --- 활동 2: 재료 손질하기 ---
with st.container(border=True):
    st.header("🛠️ 활동 2: 최첨단 도구로 재료 손질하기")
    
    st.markdown('<div class="note">'
                '<h3>🚨 셰프의 제1규칙: 원본 보존!</h3>'
                '<p>요리 전, 반드시 원본 재료는 냉장고에 따로 보관해야 해요! 실제 구글 시트에서는 <strong>\'사본 생성\'</strong>을 눌러 복사본에서만 작업하는 것, 잊지 마세요!</p>'
                '</div>', unsafe_allow_html=True)

    st.subheader("✨ 자동 세척기 (찾기 및 바꾸기) 체험")
    st.write("다른 표현들을 하나의 대표 단어로 통일해 봅시다. 아래에 직접 입력해보세요!")

    # 동적으로 규칙을 추가/삭제하는 UI
    for i, rule in enumerate(st.session_state.cleaning_rules):
        col1, col2, col3 = st.columns([4, 1, 4])
        find_val = col1.text_input("손질할 재료", value=rule["find"], key=f"find_{i}", label_visibility="collapsed")
        col2.markdown('<p style="text-align: center; font-size: 2rem; font-weight: bold; color: #FFA500;">→</p>', unsafe_allow_html=True)
        replace_val = col3.text_input("대표 재료명", value=rule["replace"], key=f"replace_{i}", label_visibility="collapsed")
        st.session_state.cleaning_rules[i] = {"find": find_val, "replace": replace_val}

    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("규칙 추가하기 +", use_container_width=True):
        st.session_state.cleaning_rules.append({"find": "", "replace": ""})
        st.rerun()

    if col_btn2.button("모두 세척하기!", type="primary", use_container_width=True):
        valid_rules = [r for r in st.session_state.cleaning_rules if r['find'] and r['replace']]
        if not valid_rules:
            st.warning("하나 이상의 유효한 세척 규칙을 입력해주세요!")
        else:
            results_html = "<ul>"
            for rule in valid_rules:
                results_html += f"<li>'{rule['find']}' → '{rule['replace']}' (으)로 변경!</li>"
            results_html += "</ul>"
            st.success(f"총 {len(valid_rules)}개의 규칙으로 데이터를 성공적으로 손질했습니다!")
            st.markdown(results_html, unsafe_allow_html=True)


# --- 활동 3: 재료 개수 세기 ---
with st.container(border=True):
    st.header("🔢 활동 3: 자동 계량기(COUNTIF)로 재료 개수 세기")
    st.write("손질이 끝난 재료가 각각 몇 개씩 있는지 정확히 세어봅시다. 아래에 `COUNTIF(범위, \"재료명\")` 함수를 직접 완성해 보세요!")

    st.markdown('<div class="note">'
                '<h3>데이터 범위 (여기에 재료 목록 붙여넣기)</h3>'
                '<p>계산할 데이터 목록을 한 줄에 하나씩 입력하거나 붙여넣어 주세요.</p>'
                '</div>', unsafe_allow_html=True)
    data_source = st.text_area("계산할 데이터", height=200, placeholder="예:\n돈까스\n스파게티\n돈까스", label_visibility="collapsed")

    st.subheader("COUNTIF 함수 완성하기 ✍️")
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 2, 0.3, 3, 0.5])
    col1.markdown('<p style="font-size: 1.5rem; font-family: monospace; font-weight: bold; text-align: right;">=COUNTIF(</p>', unsafe_allow_html=True)
    col2.markdown('<span style="font-size: 1.1rem; font-family: monospace; font-weight: bold; color: #007bff; background-color: #e6f2ff; padding: 10px; border-radius: 5px;">데이터 범위</span>', unsafe_allow_html=True)
    col3.markdown('<p style="font-size: 1.5rem; font-family: monospace; font-weight: bold;">,</p>', unsafe_allow_html=True)
    criteria = col4.text_input("조건", placeholder='"재료명"', label_visibility="collapsed")
    col5.markdown('<p style="font-size: 1.5rem; font-family: monospace; font-weight: bold;">)</p>', unsafe_allow_html=True)

    if st.button("개수 확인하기!", type="primary", use_container_width=True):
        if not data_source or not criteria:
            st.error("'데이터 범위'에 재료 목록을, 함수 속 '재료명'을 모두 입력해주세요!")
        else:
            # 사용자가 따옴표를 넣어도 처리할 수 있도록 정제
            clean_criteria = re.sub(r'^"|"$|^\'|\'$', '', criteria)
            data_list = [line.strip() for line in data_source.strip().split('\n') if line.strip()]
            count = data_list.count(clean_criteria)
            
            result_text = f"""
            <code>=COUNTIF(데이터 범위, {criteria})</code>
            <br>
            결과: '<strong>{clean_criteria}</strong>' 재료는 총 <strong>{count}</strong>개 있습니다!
            """
            st.info(result_text)


# --- 챌린지 ---
with st.container(border=True):
    st.header("🎯 오늘의 챌린지: '재료 손질 규칙' 수립하기")
    st.write("최고의 셰프는 자신만의 재료 손질 원칙이 있어요. 우리 팀만의 규칙을 정하고 아래에 기록하여 제출해봅시다!")
    
    rule1 = st.text_area("**제1원칙 (신선도 보존):**", placeholder="예: 어떤 작업을 하든, 원본 데이터는 반드시 사본을 만들어 보존한다.")
    rule2 = st.text_area("**제2원칙 (이름 통일):**", placeholder="예: 오타나 다른 표현은 가장 표준적인 단어로 통일한다. (예: 돈까쓰 -> 돈까스)")
    rule3 = st.text_area("**제3원칙 (불량 재료 처리):**", placeholder="예: 'ㅋㅋㅋ', '없음' 등 분석에 의미 없는 데이터는 삭제하거나 따로 표시해둔다.")
    
    if st.button("규칙 제출하고 셰프 인증받기!", type="primary", use_container_width=True):
        if rule1 and rule2 and rule3:
            st.success("축하합니다! 훌륭한 데이터 셰프 규칙이에요! 👨‍🍳👩‍🍳")
            st.balloons()
        else:
            st.error("앗! 모든 규칙을 작성해야 셰프 인증을 받을 수 있어요!")


# --- 다음 차시 예고 ---
st.markdown('<div style="text-align:center; padding: 2rem;">'
            '<h2>👉 다음 차시 예고</h2>'
            '<p style="font-size: 1.2rem; max-width: 800px; margin: auto; color: #333;">"최고의 재료 손질이 끝났습니다. 다음 시간에는 드디어 불을 켜고 프라이팬을 잡습니다! 이 완벽한 재료들로 사람들의 눈과 마음을 사로잡을 화려한 플레이팅, <strong>데이터 시각화</strong>를 시작해 봅시다!"</p>'
            '</div>', unsafe_allow_html=True)
