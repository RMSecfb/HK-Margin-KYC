#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
富邦證券 客戶投資風險取向分析問卷 — Streamlit 網頁版
Client Investment Risk Preference Questionnaire (Web)
"""

import streamlit as st

# ───────────────────────────── 頁面設定 ─────────────────────────────
st.set_page_config(
    page_title="客戶投資風險取向分析問卷 | Fubon Securities",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自訂 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1F4E79 0%, #2E75B6 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .section-header {
        background: #2E75B6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 1rem 0 0.5rem 0;
        font-weight: 600;
    }
    .result-box {
        background: #FCE4D6;
        border: 2px solid #1F4E79;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    .check-ok {
        background: #C6EFCE;
        color: #006100;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin: 0.3rem 0;
    }
    .check-warn {
        background: #FFC7CE;
        color: #9C0006;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin: 0.3rem 0;
    }
    .check-pending {
        background: #FFF2CC;
        color: #7F6000;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin: 0.3rem 0;
    }
    .score-badge {
        display: inline-block;
        background: #1F4E79;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #D0D0D0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ───────────────────────────── 題目定義 ─────────────────────────────
QUESTIONS = [
    {
        "id": 1,
        "section": "I. 基本資料 Basic Information",
        "cn": "年齡 Age",
        "options": [
            "A. ≥65歲或以上",
            "B. 52-64歲",
            "C. 39-51歲",
            "D. 26-38歲",
            "E. 18-25歲",
        ],
        "remark": "若選 A（≥65歲），需獨立第三方見證簽署",
    },
    {
        "id": 2,
        "section": "I. 基本資料 Basic Information",
        "cn": "教育程度 Education Level",
        "options": [
            "A. 小學/國小(含以下)",
            "B. 中學/國中",
            "C. 高職/高中",
            "D. 專科/大學",
            "E. 碩士/博士",
        ],
        "remark": "",
    },
    {
        "id": 3,
        "section": "I. 基本資料 Basic Information",
        "cn": "每年收入(港幣) Annual Income (HK$)",
        "options": [
            "A. ≤$200,000",
            "B. $200,001-$500,000",
            "C. $500,001-$1,000,000",
            "D. $1,000,001-$5,000,000",
            "E. >$5,000,000",
        ],
        "remark": "",
    },
    {
        "id": 4,
        "section": "I. 基本資料 Basic Information",
        "cn": "流動資產(港幣，不含自住物業) Liquid Assets (HK$)",
        "options": [
            "A. <$200,000",
            "B. $200,001-$500,000",
            "C. $500,001-$1,000,000",
            "D. $1,000,001-$5,000,000",
            "E. >$5,000,000",
        ],
        "remark": "",
    },
    {
        "id": 5,
        "section": "I. 基本資料 Basic Information",
        "cn": "淨資產總額(港元) Total Net Worth (HK$)",
        "options": [
            "A. <$200,000",
            "B. $200,001-$500,000",
            "C. $500,001-$1,000,000",
            "D. $1,000,001-$5,000,000",
            "E. >$5,000,000",
        ],
        "remark": "",
    },
    {
        "id": 6,
        "section": "I. 基本資料 Basic Information",
        "cn": "預期動用流動資產作投資的百分比 % of Liquid Assets for Investment",
        "options": [
            "A. <10%",
            "B. 10%-20%",
            "C. 20%-30%",
            "D. 30%-40%",
            "E. >40%",
        ],
        "remark": "",
    },
    {
        "id": 7,
        "section": "II. 一般投資目的 General Investment Goal",
        "cn": "投資目的 Investment Goal",
        "options": [
            "A. 要求保本",
            "B. 獲取高於定存的報酬",
            "C. 資產穩健增長",
            "D. 資產快速增長",
            "E. 迅速獲得短期資本利得",
        ],
        "remark": "",
    },
    {
        "id": 8,
        "section": "II. 一般投資目的 General Investment Goal",
        "cn": "期望的投資報酬率 Expected Investment Return",
        "options": [
            "A. <5%",
            "B. 5%-15%",
            "C. 15%-25%",
            "D. 25%-35%",
            "E. >35%",
        ],
        "remark": "",
    },
    {
        "id": 9,
        "section": "II. 一般投資目的 General Investment Goal",
        "cn": "可承受的投資損失 Tolerance of Investment Loss",
        "options": [
            "A. 0%",
            "B. <5%",
            "C. 5%-15%",
            "D. 15%-25%",
            "E. >25%",
        ],
        "remark": "",
    },
    {
        "id": 10,
        "section": "II. 一般投資目的 General Investment Goal",
        "cn": "可接受的投資期限 Investment Horizon",
        "options": [
            "A. <1年",
            "B. 1-3年",
            "C. 3-5年",
            "D. 5-10年",
            "E. >10年",
        ],
        "remark": "",
    },
    {
        "id": 11,
        "section": "III. 投資經驗 Investment Experience",
        "cn": "金融市場專業知識與投資交易經驗 Knowledge of Financial Markets",
        "options": [
            "A. 無認識",
            "B. 低水平(基本認識債券/股票)",
            "C. 中等水平(了解分散投資)",
            "D. 高水平(能閱讀財報)",
            "E. 精通(熟悉大部分金融商品)",
        ],
        "remark": "",
    },
    {
        "id": 12,
        "section": "III. 投資經驗 Investment Experience",
        "cn": "曾持有的投資產品經驗 Experience in Investment Products（選最高等級）",
        "options": [
            "A. 現金/存款/保本產品/港府債券",
            "B. 一般掛牌股票/非複雜債券/債券基金",
            "C. 外幣/非保本貨幣掛鈎結構性產品",
            "D. 股票/開放式基金/商品/實體ETF等",
            "E. 衍生性產品/期權/期貨/窩輪/牛熊證/對沖基金等",
        ],
        "remark": "若有多項經驗，請選最高等級（最複雜產品）",
    },
    {
        "id": 13,
        "section": "III. 投資經驗 Investment Experience",
        "cn": "投資經驗年數 Years of Investment Experience",
        "options": [
            "A. 沒有經驗/<1年",
            "B. 1-2年",
            "C. 3-5年",
            "D. 6-10年",
            "E. >11年",
        ],
        "remark": "",
    },
    {
        "id": 14,
        "section": "III. 投資經驗 Investment Experience",
        "cn": "使用孖展(融資)買賣股票/外匯經驗 Margin Facilities Experience",
        "options": [
            "A. 沒有經驗/<1年",
            "B. 1-2年",
            "C. 3-5年",
            "D. 6-10年",
            "E. >11年",
        ],
        "remark": "",
    },
    {
        "id": 15,
        "section": "III. 投資經驗 Investment Experience",
        "cn": "對未獲證監會認可結構性票據/基金或非上市定息債券的投資意願",
        "options": [
            "A. 不放心(只考慮認可及上市)",
            "B. 只考慮良好背景發行人",
            "C. 考慮有良好表現的產品",
            "D. 可考慮私募/非認可基金/對沖基金等",
            "E. 可考慮所有產品包括非保本結構性票據",
        ],
        "remark": "",
    },
]

SCORE_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}


def get_score(answer: str) -> int:
    if not answer:
        return 0
    return SCORE_MAP.get(answer[0], 0)


def get_grade(total: int) -> tuple[str, str]:
    if total < 15:
        return "G1", "低風險 / Low Risk / 保守型 (Grade 1)"
    if total <= 35:
        return "G2", "中風險 / Medium Risk / 平穩型 (Grade 2)"
    if total <= 55:
        return "G3", "高風險 / High Risk / 進取型 (Grade 3)"
    return "G4", "極高風險 / Aggressive High Risk / 積極型 (Grade 4)"


# ───────────────────────────── 側邊欄 ─────────────────────────────
with st.sidebar:
    st.markdown("### 📋 問卷資訊")
    account_no = st.text_input("帳戶號碼 Account No.", placeholder="請輸入帳戶號碼")
    account_name = st.text_input("客戶名稱 Account Name", placeholder="請輸入客戶名稱")
    fill_date = st.date_input("填寫日期 Date")

    st.markdown("---")
    st.markdown("### 📊 即時進度")
    progress_placeholder = st.empty()
    score_placeholder = st.empty()

    st.markdown("---")
    st.markdown("### 📖 計分規則")
    st.caption("A = 1 分　B = 2 分　C = 3 分　D = 4 分　E = 5 分")
    st.caption("總分 = 15 題加總（最低 15，最高 75）")
    st.markdown("""
    | 等級 | 分數範圍 |
    |------|---------|
    | G1 低風險 | < 15 |
    | G2 中風險 | 16–35 |
    | G3 高風險 | 36–55 |
    | G4 極高風險 | > 56 |
    """)
    st.markdown("---")
    st.caption("RPQ V3 (2024/APR) · 富邦證券")

# ───────────────────────────── 主畫面 ─────────────────────────────
st.markdown("""
<div class="main-header">
    <h2 style="margin:0;">富邦證券 Fubon Securities</h2>
    <h3 style="margin:0.3rem 0 0 0; font-weight:400;">客戶投資風險取向分析問卷 (個人/聯名)</h3>
    <p style="margin:0.4rem 0 0 0; opacity:0.9; font-size:0.9rem;">
        Client Investment Risk Preference Questionnaire (Individual/Joint Account)
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "請依序回答以下 **15** 題。每題必填。分數與風險等級會即時計算。"
    " 全部完成後才會顯示最終結果。黃色提示為防呆檢核。"
)

# 收集答案
answers = {}
current_section = None

for q in QUESTIONS:
    if q["section"] != current_section:
        current_section = q["section"]
        st.markdown(f'<div class="section-header">{current_section}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        ans = st.selectbox(
            f"**Q{q['id']}. {q['cn']}**",
            options=[""] + q["options"],
            key=f"q{q['id']}",
            help=q["remark"] if q["remark"] else None,
            format_func=lambda x: "— 請選擇 —" if x == "" else x,
        )
        if q["remark"]:
            st.caption(f"💡 {q['remark']}")
    with col2:
        sc = get_score(ans)
        if ans:
            st.markdown(
                f"<div style='padding-top:1.8rem; text-align:center;'>"
                f"<span class='score-badge'>{sc} 分</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='padding-top:1.8rem; text-align:center; color:#999;'>未填</div>",
                unsafe_allow_html=True,
            )
    answers[q["id"]] = ans

# 計算總分與完成度
scores = {qid: get_score(a) for qid, a in answers.items()}
total = sum(scores.values())
filled = sum(1 for a in answers.values() if a)
all_done = filled == 15

# 更新側邊欄進度
progress_placeholder.progress(filled / 15, text=f"已完成 {filled} / 15 題")
if all_done:
    grade_code, grade_desc = get_grade(total)
    score_placeholder.success(f"**總分：{total}** → {grade_code}")
else:
    score_placeholder.warning(f"目前得分：{total}（尚缺 {15 - filled} 題）")

# ───────────────────────────── 結果區 ─────────────────────────────
st.markdown("---")
st.markdown("### 📈 投資風險取向分析結果")

if not all_done:
    st.warning(f"⚠ 尚有 **{15 - filled}** 題未填，請完成所有題目後再查看最終風險等級。")
else:
    grade_code, grade_desc = get_grade(total)
    color_map = {
        "G1": "#548235",
        "G2": "#BF8F00",
        "G3": "#C65911",
        "G4": "#C00000",
    }
    st.markdown(f"""
    <div class="result-box">
        <h3 style="margin:0 0 0.5rem 0;">總分 Total Score：<span style="color:#1F4E79; font-size:1.5rem;">{total}</span> / 75</h3>
        <h2 style="margin:0; color:{color_map.get(grade_code, '#1F4E79')};">{grade_code}　{grade_desc}</h2>
        <p style="margin-top:0.8rem; color:#666; font-size:0.9rem;">
            評分對照：G1 低風險 &lt;15　|　G2 中風險 16–35　|　G3 高風險 36–55　|　G4 極高風險 &gt;56
        </p>
    </div>
    """, unsafe_allow_html=True)

# ───────────────────────────── 防呆檢核 ─────────────────────────────
st.markdown("### 🛡 相互防呆檢核 Consistency Checks")

def letter(ans: str) -> str:
    return ans[0] if ans else ""

def rank(ans: str) -> int:
    return SCORE_MAP.get(letter(ans), 0)

# 檢核 1：年齡 ≥65
a1 = answers.get(1, "")
if not a1:
    st.markdown('<div class="check-pending">檢核1：— 請先填寫年齡</div>', unsafe_allow_html=True)
elif letter(a1) == "A":
    st.markdown(
        '<div class="check-warn">檢核1：⚠ 客戶年齡 ≥65 歲：需獨立第三方'
        '（證監會註冊負責人員/主管或 65 歲以下親屬）見證簽署並確認問卷內容</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核1：✓ 年齡非 65 歲以上，無需特別見證</div>', unsafe_allow_html=True)

# 檢核 2：流動資產 vs 淨資產
a4, a5 = answers.get(4, ""), answers.get(5, "")
if not a4 or not a5:
    st.markdown('<div class="check-pending">檢核2：— 請先填寫流動資產與淨資產</div>', unsafe_allow_html=True)
elif rank(a4) > rank(a5):
    st.markdown(
        '<div class="check-warn">檢核2：⚠ 流動資產等級高於淨資產等級，請確認是否合理'
        '（流動資產通常 ≤ 淨資產）</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核2：✓ 流動資產與淨資產等級合理</div>', unsafe_allow_html=True)

# 檢核 3：投資目的 vs 知識
a7, a11 = answers.get(7, ""), answers.get(11, "")
if not a7 or not a11:
    st.markdown('<div class="check-pending">檢核3：— 請先填寫投資目的與知識水平</div>', unsafe_allow_html=True)
elif rank(a7) >= 4 and rank(a11) <= 2:
    st.markdown(
        '<div class="check-warn">檢核3：⚠ 投資目的較進取但市場知識較低，建議加強了解或調整目標</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核3：✓ 投資目的與知識水平大致相符</div>', unsafe_allow_html=True)

# 檢核 4：期望報酬 vs 損失承受
a8, a9 = answers.get(8, ""), answers.get(9, "")
if not a8 or not a9:
    st.markdown('<div class="check-pending">檢核4：— 請先填寫期望報酬與可承受損失</div>', unsafe_allow_html=True)
elif rank(a8) >= 4 and rank(a9) <= 2:
    st.markdown(
        '<div class="check-warn">檢核4：⚠ 期望高報酬但可承受損失偏低，風險與報酬可能不匹配</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核4：✓ 期望報酬與損失承受度大致匹配</div>', unsafe_allow_html=True)

# 檢核 5：孖展 vs 產品經驗
a12, a14 = answers.get(12, ""), answers.get(14, "")
if not a12 or not a14:
    st.markdown('<div class="check-pending">檢核5：— 請先填寫產品經驗與孖展經驗</div>', unsafe_allow_html=True)
elif rank(a14) >= 3 and rank(a12) <= 2:
    st.markdown(
        '<div class="check-warn">檢核5：⚠ 有較長孖展經驗但產品經驗顯示較基礎，請確認填寫是否正確</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核5：✓ 孖展經驗與產品經驗大致一致</div>', unsafe_allow_html=True)

# ───────────────────────────── 確認與匯出 ─────────────────────────────
st.markdown("---")
st.markdown("### ✅ 客戶確認 Client Confirmation")
st.markdown("""
1. 本人/吾等確認上述投資風險取向分析的結果正確反映本人的投資風險取向。  
2. 本人/吾等明白上述投資風險取向分析的結果將取代本人/吾等於開戶表之答案。
""")

confirm = st.checkbox("本人確認以上內容正確無誤")

if all_done and confirm:
    st.success("問卷已完成並確認。可下載結果摘要。")

    # 產生摘要文字
    grade_code, grade_desc = get_grade(total)
    lines = [
        "富邦證券 — 客戶投資風險取向分析問卷結果摘要",
        f"帳戶號碼：{account_no or '（未填）'}",
        f"客戶名稱：{account_name or '（未填）'}",
        f"填寫日期：{fill_date}",
        "",
        f"總分：{total} / 75",
        f"風險等級：{grade_code} {grade_desc}",
        "",
        "各題答案：",
    ]
    for q in QUESTIONS:
        a = answers[q["id"]]
        lines.append(f"  Q{q['id']}. {q['cn'][:20]}… → {a}（{get_score(a)}分）")
    lines.append("")
    lines.append("注意：本結果僅供參考，公司保留最終決定客戶風險等級的權利。")
    summary = "\n".join(lines)

    st.download_button(
        label="📥 下載結果摘要（文字檔）",
        data=summary.encode("utf-8"),
        file_name=f"RPQ結果_{account_no or '未命名'}_{fill_date}.txt",
        mime="text/plain",
    )
elif all_done and not confirm:
    st.info("請勾選上方確認框後即可下載結果。")
else:
    st.caption("完成所有題目並勾選確認後，可下載結果摘要。")

# 頁尾
st.markdown("---")
st.caption(
    "本問卷分析結果僅供參考，本公司保留最終決定客戶風險等級的權利。"
    " 聯名帳戶以較高投資風險取向為主。"
    " 客戶財務狀況或風險取向變更時，請重新填寫並通知公司。"
)
st.caption("RPQ V3 (2024/APR) · Fubon Securities (Hong Kong) Limited")
