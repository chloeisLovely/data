import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import datetime
import re
import math

# --- 페이지 설정 ---
st.set_page_config(
    page_title="6차시: 미슐랭 스타의 조건 🌟",
    page_icon="🏆",
    layout="wide"
)

# --- 헬퍼 함수 ---

def parse_data(raw_data):
    """텍스트 데이터를 파싱하여 리스트로 반환합니다."""
    parsed_data = []
    if not raw_data:
        return parsed_data
    data_lines = raw_data.strip().split('\n')
    for line in data_lines:
        parts = re.split(r'[:\s,]+', line.strip())
        if len(parts) >= 2:
            item = parts[0].strip()
            try:
                value = float(parts[-1].strip())
                parsed_data.append({'항목': item, '값': value})
            except (ValueError, IndexError):
                pass
    return parsed_data

def wrap_text(text, font, max_width):
    """주어진 너비에 맞게 텍스트를 여러 줄로 나눕니다."""
    lines = []
    if not text:
        return lines
    for line in text.split('\n'):
        words = line.split(' ')
        while len(words) > 0:
            current_line = ''
            while len(words) > 0 and font.getbbox(current_line + words[0])[2] <= max_width:
                current_line += (words.pop(0) + ' ')
            lines.append(current_line.strip())
    return lines

def draw_chart_on_image(draw, data, chart_type, title, x_pos, y_pos, width, height, font_m, font_s):
    """Pillow을 사용하여 이미지 위에 간단한 차트를 그립니다."""
    draw.rectangle([x_pos, y_pos, x_pos + width, y_pos + height], fill="#FFFFFF", outline="#DDDDDD", width=1)
    
    # 차트 제목
    title_bbox = font_m.getbbox(title)
    draw.text((x_pos + (width - title_bbox[2]) / 2, y_pos + 15), title, font=font_m, fill="#333333")

    chart_area_y = y_pos + 50
    chart_area_height = height - 60
    
    if not data:
        draw.text((x_pos + 20, chart_area_y + 20), "데이터 없음", font=font_s, fill="#AAAAAA")
        return

    total_value = sum(item['값'] for item in data)
    
    if chart_type == "원 차트 (비율)":
        if total_value == 0: return
        center_x, center_y = x_pos + width / 2, chart_area_y + chart_area_height / 2
        radius = min(width, chart_area_height) * 0.35
        bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
        
        start_angle = -90
        colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#bab0ac", "#d37295"]
        for i, item in enumerate(data):
            angle = (item['값'] / total_value) * 360
            draw.pieslice(bbox, start=start_angle, end=start_angle + angle, fill=colors[i % len(colors)])
            start_angle += angle
            
    elif chart_type == "막대 차트 (비교)":
        num_bars = len(data)
        if num_bars == 0: return
        bar_width = (width - 40) / (num_bars * 1.5)
        max_val = max(item['값'] for item in data)
        if max_val == 0: return
        
        for i, item in enumerate(data):
            bar_height = (item['값'] / max_val) * (chart_area_height - 20)
            bar_x = x_pos + 30 + i * (bar_width * 1.5)
            bar_y = chart_area_y + chart_area_height - bar_height
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, chart_area_y + chart_area_height], fill="#4e79a7")
            label = item['항목']
            label_bbox = font_s.getbbox(label)
            draw.text((bar_x + bar_width/2 - label_bbox[2]/2, chart_area_y + chart_area_height + 5), label, font=font_s, fill="#333")

def create_summary_image_6():
    """세션 상태의 모든 입력을 기반으로 하나의 요약 이미지를 생성합니다."""
    font_path = "GowunDodum-Regular.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/gowundodum/GowunDodum-Regular.ttf"
            r = requests.get(url)
            with open(font_path, "wb") as f: f.write(r.content)
        except Exception as e:
            st.error(f"폰트를 다운로드하는 데 실패했습니다: {e}"); return None
    
    try:
        title_font = ImageFont.truetype(font_path, 40)
        header_font = ImageFont.truetype(font_path, 28)
        body_font = ImageFont.truetype(font_path, 20)
        small_font = ImageFont.truetype(font_path, 16)
    except IOError:
        st.error("폰트 파일을 로드할 수 없습니다."); return None

    content = [
        ("데이터 쿡방 6차시 제출 결과", title_font),
        (f"제출 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", body_font), ("", body_font),
        ("🧐 활동 1: '최악의 레스토랑' 비평 노트", header_font),
        (f"정체불명 스테이크: {st.session_state.get('critique_1', 'N/A')}", body_font),
        (f"고무줄 자: {st.session_state.get('critique_2', 'N/A')}", body_font),
        (f"무지개 폭탄: {st.session_state.get('critique_3', 'N/A')}", body_font), ("", body_font),
        ("🛠️ 활동 2: 업그레이드 체크리스트", header_font),
        (f"[제목]: {'완료' if st.session_state.get('check_title', False) else '미완료'}", body_font),
        (f"[축 레이블]: {'완료' if st.session_state.get('check_axis', False) else '미완료'}", body_font),
        (f"[색상 강조]: {'완료' if st.session_state.get('check_color', False) else '미완료'}", body_font),
        (f"[데이터 레이블]: {'완료' if st.session_state.get('check_datalabel', False) else '미완료'}", body_font), ("", body_font),
        ("🎯 챌린지: 미슐랭 3스타 코스 요리", header_font),
    ]

    width, padding, line_spacing = 900, 40, 15
    content_width = width - 2 * padding
    
    total_height, wrapped_content = padding, []
    for text, font in content:
        for line in wrap_text(text, font, content_width):
            wrapped_content.append((line, font))
            bbox = font.getbbox(line)
            total_height += (bbox[3] - bbox[1]) + line_spacing

    total_height += 350 # 차트 공간
    
    img = Image.new('RGB', (width, total_height), '#F0F2F6')
    draw = ImageDraw.Draw(img)
    
    y = padding
    for text, font in wrapped_content:
        draw.text((padding, y), text, font=font, fill='#1E3A8A')
        bbox = font.getbbox(text)
        y += (bbox[3] - bbox[1]) + line_spacing
    
    y += padding
    chart_width = (content_width - 30) // 3
    chart_height = 250
    courses = ['appetizer', 'main_dish', 'dessert']
    for i, course in enumerate(courses):
        data = parse_data(st.session_state.get(f'{course}_data', ''))
        chart_type = st.session_state.get(f'{course}_type', '막대 차트 (비교)')
        title = st.session_state.get(f'{course}_title', course.capitalize())
        draw_chart_on_image(draw, data, chart_type, title, padding + i * (chart_width + 15), y, chart_width, chart_height, body_font, small_font)
    
    y += chart_height + padding
    note_lines = wrap_text(f"셰프의 노트: {st.session_state.get('course_note', 'N/A')}", body_font, content_width)
    for line in note_lines:
        draw.text((padding, y), line, font=body_font, fill='#1E3A8A')
        bbox = body_font.getbbox(line)
        y += (bbox[3] - bbox[1]) + line_spacing

    buf = BytesIO()
    img.save(buf, format='PNG'); return buf.getvalue()

# --- 스타일링 ---
st.markdown("""<style>@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');.stApp{background-color:#F0F2F6;font-family:'Gowun+Dodum',sans-serif}h1,h2,h3{color:#1E3A8A !important;font-weight:bold !important}.main .block-container{max-width:950px !important;margin:0 auto !important}[data-testid="stVerticalBlockBorderWrapper"]{background-color:#fff;border:2px solid #D1D5DB;border-radius:1.5rem;margin-bottom:2rem;box-shadow:0 10px 15px -3px rgba(0,0,0,.05),0 4px 6px -2px rgba(0,0,0,.05)}.note{background-color:#E0E7FF;border-left:5px solid #4F46E5;padding:1.5rem;border-radius:.5rem;margin-bottom:1rem}.critique-box{background-color:#FFFBEB;border:1px solid #FBBF24;padding:1rem;border-radius:.5rem;height:100%}</style>""", unsafe_allow_html=True)

def create_bad_charts():
    df1 = pd.DataFrame({'값': [45, 30, 25]}); chart1 = alt.Chart(df1).mark_arc().encode(theta=alt.Theta(field="값", type="quantitative")).properties(width=250, height=250)
    df2 = pd.DataFrame({'항목': ['A제품', 'B제품'], '만족도': [88, 92]}); chart2 = alt.Chart(df2).mark_bar(width=50).encode(x=alt.X('항목', axis=None), y=alt.Y('만족도', scale=alt.Scale(domain=[85, 95]), axis=None)).properties(width=250, height=250)
    df3 = pd.DataFrame({'과일': ['사과', '바나나', '딸기', '포도', '오렌지'], '판매량': [30, 45, 70, 25, 50]}); chart3 = alt.Chart(df3).mark_bar().encode(x='과일', y='판매량', color=alt.Color('과일', scale=alt.Scale(scheme='rainbow'), legend=None)).properties(width=250, height=250)
    return chart1, chart2, chart3

st.markdown('<h1 style="text-align: center; font-size: 3.5rem;">6차시: 미슐랭 스타의 조건 🌟</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #555; margin-bottom: 2rem;">최고의 차트로 설득하라!</p>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div style="text-align:center;"><div style="font-size: 4rem; margin-bottom: 1rem;">🤵</div><h2>미슐랭 심사위원 D의 불시 점검</h2><p style="font-size: 1.2rem; text-align: left;">"셰프 탐정단. 지난주, 여러분의 데이터 쿡방 특집은 성공적이었다. 시청자 반응도 뜨거웠지. 하지만... 나는 보통 셰프가 아니다. 오늘은 크리에이터가 아닌, 세상에서 가장 까다로운 \'미슐랭 심사위원 D\'로서 여러분의 주방을 불시에 점검하겠다."<br><br>"내가 어제 비밀리에 방문했던 한 최악의 레스토랑 이야기를 해주지. 그곳의 요리들은 겉보기엔 그럴듯했지만, 모두 심사에서 탈락했다. 왜였을까?"<br><br>첫 번째 요리 (제목 없는 차트): "정체불명의 스테이크가 나왔다. 이름이 뭐냐고 물으니, 셰프는 그냥 고기요리라고 하더군. 이게 소고기인지, 돼지고기인지, 손님은 알 길이 없다! 최악이다!"<br>두 번째 요리 (축 설명 없는 차트): "수프가 나왔는데, 양이 얼마나 되는지 메뉴판에 전혀 적혀있지 않았다. 이게 1인분인지 2인분인지 알 수 없다! 끔찍하다!"<br>세 번째 요리 (설명 없는 샐러드): "알록달록한 샐러드가 나왔는데, 소스가 뭔지 설명(범례)이 없었다. 초록색 소스가 바질 페스토인지, 와사비인지 어떻게 아나! 당장 주방 문 닫아!"<br><br>"미슐랭 3스타의 조건은 간단하다. <strong>정직함, 친절함, 그리고 아름다움.</strong> 즉, 데이터를 왜곡하지 않고(정직), 누가 봐도 이해하기 쉽게 설명하며(친절), 핵심 메시지를 세련되게 강조하는(아름다움) 것이다. 자, 이제 여러분의 주방으로 돌아가라. 5차시에 만들었던 여러분의 시그니처 디쉬를, 이 미슐랭 3스타의 기준에 맞춰 명품 요리로 업그레이드할 시간이다. 나의 별점을 받을 자격이 있는지, 증명해 봐라!"</p></div>', unsafe_allow_html=True)

with st.container(border=True):
    st.header("🧐 활동 1: '최악의 레스토랑' 메뉴 비평하기")
    st.write("여러분이 미슐랭 심사위원이라면, 아래 최악의 레스토랑 메뉴판(나쁜 차트 예시)의 문제점은 무엇이고, 어떻게 개선해야 할지 비평 노트를 작성해 보세요.")
    chart1, chart2, chart3 = create_bad_charts()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="critique-box"><h4>정체불명 스테이크</h4></div>', unsafe_allow_html=True); st.altair_chart(chart1, use_container_width=True)
        st.text_area("비평 노트 1", placeholder="예: 요리 이름(제목)이 없어서 무엇에 대한 비율인지 알 수 없어요. 각 조각(범례)이 무엇인지도 설명이 필요해요.", height=150, label_visibility="collapsed", key="critique_1")
    with col2:
        st.markdown('<div class="critique-box"><h4>고무줄 자</h4></div>', unsafe_allow_html=True); st.altair_chart(chart2, use_container_width=True)
        st.text_area("비평 노트 2", placeholder="예: 세로축의 시작이 0이 아니라서 차이가 과장되어 보여요. 정직하지 않아요!", height=150, label_visibility="collapsed", key="critique_2")
    with col3:
        st.markdown('<div class="critique-box"><h4>무지개 폭탄</h4></div>', unsafe_allow_html=True); st.altair_chart(chart3, use_container_width=True)
        st.text_area("비평 노트 3", placeholder="예: 색깔이 너무 많아서 정신없고, 어떤 과일이 중요한지 알 수 없어요.", height=150, label_visibility="collapsed", key="critique_3")

with st.container(border=True):
    st.header("🛠️ 활동 2: 우리 팀의 '시그니처 디쉬' 업그레이드하기")
    st.write("이제 우리 주방으로 돌아와, 5차시에 만들었던 시그니처 디쉬를 미슐랭 3스타급으로 업그레이드해 봅시다. 아래 업그레이드 체크리스트를 따라 차근차근 수정해 보세요.")
    st.subheader("[미슐랭 스타를 위한 업그레이드 체크리스트]")
    st.checkbox("**[제목]** 차트의 제목을 누가 봐도 내용을 알 수 있도록 구체적이고 흥미롭게 수정했나요? (예: 과일 선호도 → \"[압도적 1위] 우리 반 학생들이 가장 선호하는 과일\")", key="check_title")
    st.checkbox("**[축 레이블]** 막대그래프의 세로축(Y축)에 학생 수(명)처럼 데이터의 단위를 명확하게 적었나요?", key="check_axis")
    st.checkbox("**[색상 강조]** 가장 중요하게 보여주고 싶은 데이터(예: 1등 막대)만 눈에 띄는 다른 색으로 바꾸어 강조했나요?", key="check_color")
    st.checkbox("**[데이터 레이블]** 각 막대나 파이 조각 위에 실제 숫자 값을 표시하여 정확성을 높였나요?", key="check_datalabel")

with st.container(border=True):
    st.header("📝 활동 3: '코스 요리'로 이야기 만들기")
    st.write("미슐랭 3스타 레스토랑은 단품 요리 하나만으로 평가받지 않습니다. 전체적인 흐름을 보여주는 코스 요리로 승부하죠. 우리 팀의 주장을 뒷받침할 에피타이저, 메인 디쉬, 디저트, 즉 3개의 업그레이드된 차트를 하나의 코스로 구성해 봅시다.")
    st.markdown('<div class="note"><h5>🧑‍🍳 처음부터 완벽한 미슐랭 3스타 요리를 만드는 셰프는 없습니다.</h4><p>심사위원 D의 피드백을 하나씩 반영하면서, 우리의 요리가 어떻게 명품으로 변신하는지 그 과정을 즐겨봅시다!</p></div>', unsafe_allow_html=True)

with st.container(border=True):
    st.header("🎯 오늘의 챌린지: '미슐랭 3스타 코스 요리' 선보이기")
    st.write("여러분의 핵심 주장을 뒷받침하는 에피타이저, 메인 디쉬, 디저트, 즉 3개의 업그레이드된 차트를 코스로 구성하여 미슐랭 코스 메뉴판을 제출해 주십시오.")
    st.subheader("[데이터 쿡방: 미슐랭 3스타 코스]")

    courses = {
        'appetizer': '에피타이저 (차트 1)',
        'main_dish': '메인 디쉬 (차트 2)',
        'dessert': '디저트 (차트 3)'
    }
    
    cols = st.columns(3)
    for i, (key, title) in enumerate(courses.items()):
        with cols[i]:
            with st.expander(f"**{title}**", expanded=True):
                st.text_input("차트 제목", key=f"{key}_title", placeholder="예: 과일 선호도 비율")
                st.text_area("데이터 ('항목:값')", key=f"{key}_data", height=150, placeholder="사과: 10\n바나나: 15\n딸기: 8")
                st.radio("차트 종류", ["원 차트 (비율)", "막대 차트 (비교)"], key=f"{key}_type", horizontal=True)
                
                data = parse_data(st.session_state.get(f"{key}_data", ""))
                if data:
                    df = pd.DataFrame(data)
                    chart_type = st.session_state.get(f"{key}_type")
                    chart_title = st.session_state.get(f"{key}_title", "")

                    if chart_type == "원 차트 (비율)":
                        c = alt.Chart(df).mark_arc(innerRadius=20).encode(
                            theta=alt.Theta(field="값", type="quantitative"),
                            color=alt.Color(field="항목", type="nominal", title="항목"),
                            tooltip=['항목', '값']
                        ).properties(title=alt.TitleParams(text=chart_title, anchor='middle'))
                        st.altair_chart(c, use_container_width=True)
                    else: # 막대 차트
                        c = alt.Chart(df).mark_bar().encode(
                            x=alt.X('항목', sort=None),
                            y=alt.Y('값'),
                            color=alt.Color('항목', legend=None),
                            tooltip=['항목', '값']
                        ).properties(title=alt.TitleParams(text=chart_title, anchor='middle'))
                        st.altair_chart(c, use_container_width=True)

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
        st.download_button(label="결과 이미지 다운로드하기 🖼️", data=st.session_state.generated_image_6, file_name="데이터쿡방_6차시_결과.png", mime="image/png", use_container_width=True)

with st.container(border=True):
    st.header("📝 정리: 오늘 배운 개념 요약")
    st.markdown("""- **좋은 차트의 3대 조건:** 정직함(데이터 왜곡 금지), 친절함(쉬운 설명), 아름다움(핵심 강조)\n- **차트의 3대 필수 요소:** 제목(요리 이름), 축 레이블(단위), 범례(재료 설명)는 반드시 포함해야 함\n- **데이터 강조:** 색상이나 글꼴 크기를 활용하면, 우리가 가장 중요하게 생각하는 메시지를 효과적으로 전달할 수 있음""")

st.markdown('<div style="text-align:center; padding: 2rem;"><h2>👉 다음 차시 예고</h2><p style="font-size: 1.2rem; max-width: 800px; margin: auto; color: #333;">"원더풀! ... 다음 시간에는 우리가 만든 이 완벽한 요리(차트)들을 한 테이블에 올려놓고, 그 조합 속에서만 발견되는 충격적인 비밀 레시피, 즉 데이터 인사이트(Insight)를 찾는 여정을 떠나겠습니다."</p></div>', unsafe_allow_html=True)

