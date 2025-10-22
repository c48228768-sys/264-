# -*- coding: utf-8 -*-
#실행 streamlit run 226644.py

import streamlit as st
import json
import os
from openai import OpenAI

# -----------------------------
# 🔧 환경설정
# -----------------------------
st.set_page_config(
    page_title="이육사, 다시 응답하다",
    page_icon="🖋️",
    layout="wide"
)

# -----------------------------
# 🔐 API 키 불러오기
# -----------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        st.error("⚠️ OpenAI API 키를 찾을 수 없습니다. 환경변수 또는 secrets.toml을 확인해주세요.")
        st.stop()

client = OpenAI(api_key=api_key)

# -----------------------------
# 💾 대화 기록 불러오기 / 저장 함수
# -----------------------------
def load_messages():
    """이전 대화 불러오기"""
    if os.path.exists("messages.json"):
        with open("messages.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 처음 실행 시 초기 메시지 설정
        return [{"role": "system", "content": "너는 이육사 시인에 대해 잘 아는 친절한 선생님이야."}]

def save_messages(messages):
    """대화 내용을 파일로 저장"""
    with open("messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# -----------------------------
# 💬 초기화
# -----------------------------
messages = load_messages()

# -----------------------------
# 🧭 사이드바
# -----------------------------
st.sidebar.title("📖 이육사, 다시 응답하다")
st.sidebar.markdown("""
이 웹사이트는 안동 출신 시인이자 독립운동가 **이육사**의 삶과 작품을  
AI를 통해 이해하고, 지역 문화를 친숙하게 즐길 수 있도록 만든  
**문화 체험형 챗봇 프로젝트**입니다.
""")

if st.sidebar.button("🗑️ 대화 초기화"):
    messages = [{"role": "system", "content": "너는 이육사 시인에 대해 잘 아는 친절한 선생님이야."}]
    save_messages(messages)
    st.sidebar.success("대화 기록이 초기화되었습니다.")

# -----------------------------
# 🏠 메인 영역
# -----------------------------
st.title("🖋️ 이육사, 다시 응답하다")
st.markdown("""
안동의 자랑, **이육사 시인**의 정신과 문학 세계를 인공지능을 통해 되살리는 프로젝트입니다.  
시인의 철학과 생애, 작품에 대해 묻고 대화하며 문화를 즐겨보세요.
""")

# 사용자 입력
question = st.text_input("💬 이육사 시인에게 물어보세요:", placeholder="예: 이육사의 '광야'는 어떤 의미인가요?")

# -----------------------------
# 🤖 AI 응답 처리
# -----------------------------
if question:
    messages.append({"role": "user", "content": question})
    try:
        with st.spinner("이육사 시인의 정신을 불러오는 중..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            save_messages(messages)
        st.markdown(f"### 👤 나: {question}")
        st.markdown(f"**🤖 이육사 챗봇:** {reply}")
    except Exception as e:
        st.error(f"⚠️ 오류 발생: {e}")

# -----------------------------
# 💬 이전 대화 보기
# -----------------------------
if st.checkbox("📜 이전 대화 보기"):
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**👤 나:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 이육사 챗봇:** {msg['content']}")

# -----------------------------
# 📚 참고 자료 섹션
# -----------------------------
st.markdown("---")
st.header("📚 이육사 관련 자료")
st.markdown("""
- **이육사문학관 공식 홈페이지:** [http://www.yiuksa.or.kr](http://www.yiuksa.or.kr)  
- **국립중앙도서관:** [이육사 관련 문헌 검색](https://www.nl.go.kr)  
- **한국학중앙연구원:** [인물정보 / 자료 검색](https://www.aks.ac.kr)  
- **문화재청 국가문화유산포털:** [이육사 생가 / 기념관 정보](https://www.heritage.go.kr)
""")

st.markdown("---")
st.caption("© 2025 국립경국대학교 디지털ICT공학과 | 안동지역 전통문화 이해 프로젝트")

