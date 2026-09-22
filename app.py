#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
富邦證券 客戶投資風險取向分析問卷 — Streamlit Prototype v1
Client Investment Risk Preference Questionnaire (RPQ)

v1 agreed business rules:
- 15 questions; A/B/C/D/E = 1/2/3/4/5 points
- G1: 15-30, G2: 31-45, G3: 46-60, G4: 61-75
- Age >= 65: internal rule reminder for independent third-party witness
- Joint account: internal rule uses the higher risk grade (when another holder's grade is provided)
- Consistency issues: warning only; RPQ result still displays, acknowledgement recorded before final download
- Margin/Credit information: disclosure only; does NOT affect RPQ score or grade

IMPORTANT:
This is a prototype. Final production use should be approved against the firm's latest HK compliance,
credit and securities margin financing policies.
"""

from __future__ import annotations

import streamlit as st


# ───────────────────────────── Page setup ─────────────────────────────
st.set_page_config(
    page_title="客戶投資風險取向分析問卷 | Fubon Securities",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
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
    .credit-box {
        background: #EEF5FB;
        border: 1px solid #9CC2E5;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
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
</style>
""",
    unsafe_allow_html=True,
)


# ───────────────────────────── Business rules ─────────────────────────────
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
        "remark": "內規：若選 A（≥65歲），需辦理獨立第三方見證簽署。",
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
            "A. ≤$200,000",
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
            "A. ≤$200,000",
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
            "B. 10%-<20%",
            "C. 20%-<30%",
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
            "B. 5%-<15%",
            "C. 15%-<25%",
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
            "B. >0%-<5%",
            "C. 5%-<15%",
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
            "B. 1年-<3年",
            "C. 3年-<5年",
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
        "remark": "若有多項經驗，請選最高等級（最複雜產品）。Q12 產品分級沿用 v0 原始內容，待業務/Compliance確認。",
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
            "E. ≥11年",
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
            "E. ≥11年",
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
GRADE_ORDER = {"G1": 1, "G2": 2, "G3": 3, "G4": 4}
GRADE_DESC = {
    "G1": "低風險 / Low Risk / 保守型 (Grade 1)",
    "G2": "中風險 / Medium Risk / 平穩型 (Grade 2)",
    "G3": "高風險 / High Risk / 進取型 (Grade 3)",
    "G4": "極高風險 / Aggressive High Risk / 積極型 (Grade 4)",
}


def get_score(answer: str) -> int:
    return SCORE_MAP.get(answer[0], 0) if answer else 0


def get_grade(total: int) -> tuple[str, str]:
    """Apply agreed v1 grade bands. Call only after all 15 questions are completed."""
    if 15 <= total <= 30:
        code = "G1"
    elif total <= 45:
        code = "G2"
    elif total <= 60:
        code = "G3"
    else:
        code = "G4"
    return code, GRADE_DESC[code]


def letter(answer: str) -> str:
    return answer[0] if answer else ""


def rank(answer: str) -> int:
    return SCORE_MAP.get(letter(answer), 0)


def higher_grade(grade_a: str, grade_b: str | None) -> str:
    if not grade_b or grade_b not in GRADE_ORDER:
        return grade_a
    return grade_b if GRADE_ORDER[grade_b] > GRADE_ORDER[grade_a] else grade_a


# ───────────────────────────── Sidebar ─────────────────────────────
with st.sidebar:
    st.markdown("### 📋 問卷資訊")
    account_no = st.text_input("帳戶號碼 Account No.", placeholder="請輸入帳戶號碼")
    account_name = st.text_input("客戶名稱 Account Name", placeholder="請輸入客戶名稱")
    account_type = st.selectbox("帳戶類型 Account Type", ["個人 Individual", "聯名 Joint"])
    fill_date = st.date_input("填寫日期 Date")

    joint_other_grade = None
    if account_type == "聯名 Joint":
        joint_other_grade_raw = st.selectbox(
            "其他聯名戶最高 RPQ 等級",
            ["未提供", "G1", "G2", "G3", "G4"],
            help="內規暫定：聯名帳戶採較高投資風險取向。其他聯名戶應另行完成其RPQ。",
        )
        if joint_other_grade_raw != "未提供":
            joint_other_grade = joint_other_grade_raw
        st.caption("內規：聯名帳戶採各聯名戶中較高的投資風險等級。")

    st.markdown("---")
    st.markdown("### 📊 即時進度")
    progress_placeholder = st.empty()
    score_placeholder = st.empty()

    st.markdown("---")
    st.markdown("### 📖 計分規則")
    st.caption("A = 1 分　B = 2 分　C = 3 分　D = 4 分　E = 5 分")
    st.caption("總分 = 15 題加總（最低 15，最高 75）")
    st.markdown(
        """
        | 等級 | 分數範圍 |
        |------|---------|
        | G1 低風險 | 15–30 |
        | G2 中風險 | 31–45 |
        | G3 高風險 | 46–60 |
        | G4 極高風險 | 61–75 |
        """
    )
    st.markdown("---")
    st.caption("RPQ Prototype v1 · 2026/09")


# ───────────────────────────── Main questionnaire ─────────────────────────────
st.markdown(
    """
<div class="main-header">
    <h2 style="margin:0;">富邦證券 Fubon Securities</h2>
    <h3 style="margin:0.3rem 0 0 0; font-weight:400;">客戶投資風險取向分析問卷 (個人/聯名)</h3>
    <p style="margin:0.4rem 0 0 0; opacity:0.9; font-size:0.9rem;">
        Client Investment Risk Preference Questionnaire (Individual/Joint Account)
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.info(
    "請依序回答以下 **15** 題。每題必填。分數與風險等級會即時計算。"
    " 全部完成後才會顯示最終 RPQ 結果；一致性檢核僅作提醒，不會改變 RPQ 分數。"
)

answers: dict[int, str] = {}
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

scores = {qid: get_score(a) for qid, a in answers.items()}
total = sum(scores.values())
filled = sum(1 for a in answers.values() if a)
all_done = filled == 15

progress_placeholder.progress(filled / 15, text=f"已完成 {filled} / 15 題")
if all_done:
    grade_code, grade_desc = get_grade(total)
    score_placeholder.success(f"**總分：{total}** → {grade_code}")
else:
    score_placeholder.warning(f"目前得分：{total}（尚缺 {15 - filled} 題）")


# ───────────────────────────── RPQ result ─────────────────────────────
st.markdown("---")
st.markdown("### 📈 投資風險取向分析結果")

primary_grade_code = None
account_grade_code = None
if not all_done:
    st.warning(f"⚠ 尚有 **{15 - filled}** 題未填，請完成所有題目後再查看最終風險等級。")
else:
    primary_grade_code, grade_desc = get_grade(total)
    account_grade_code = primary_grade_code
    if account_type == "聯名 Joint":
        account_grade_code = higher_grade(primary_grade_code, joint_other_grade)

    color_map = {"G1": "#548235", "G2": "#BF8F00", "G3": "#C65911", "G4": "#C00000"}
    st.markdown(
        f"""
        <div class="result-box">
            <h3 style="margin:0 0 0.5rem 0;">總分 Total Score：
                <span style="color:#1F4E79; font-size:1.5rem;">{total}</span> / 75
            </h3>
            <h2 style="margin:0; color:{color_map[primary_grade_code]};">
                {primary_grade_code}　{grade_desc}
            </h2>
            <p style="margin-top:0.8rem; color:#666; font-size:0.9rem;">
                評分對照：G1 15–30　|　G2 31–45　|　G3 46–60　|　G4 61–75
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if account_type == "聯名 Joint":
        if joint_other_grade:
            st.info(
                f"內規：本份 RPQ 為 **{primary_grade_code}**；其他聯名戶最高等級為 **{joint_other_grade}**；"
                f"帳戶適用風險等級取較高者 → **{account_grade_code}**。"
            )
        else:
            st.warning(
                "此為聯名帳戶，但尚未提供其他聯名戶的 RPQ 等級。"
                "本版不會假設其他聯名戶風險屬性；請另行完成其 RPQ 後再依內規取較高等級。"
            )


# ───────────────────────────── Consistency checks ─────────────────────────────
st.markdown("### 🛡 相互防呆檢核 Consistency Checks")

active_consistency_warnings: list[str] = []
age65 = letter(answers.get(1, "")) == "A"

# Check 1: internal rule for elderly client
if not answers.get(1):
    st.markdown('<div class="check-pending">檢核1：— 請先填寫年齡</div>', unsafe_allow_html=True)
elif age65:
    st.markdown(
        '<div class="check-warn">檢核1：⚠ 內規提醒：客戶年齡 ≥65 歲，需辦理獨立第三方見證簽署並確認問卷內容。</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="check-ok">檢核1：✓ 年齡未達內規第三方見證門檻</div>', unsafe_allow_html=True)

# Check 2: liquid assets vs net worth
a4, a5 = answers.get(4, ""), answers.get(5, "")
if not a4 or not a5:
    st.markdown('<div class="check-pending">檢核2：— 請先填寫流動資產與淨資產</div>', unsafe_allow_html=True)
elif rank(a4) > rank(a5):
    msg = "流動資產等級高於淨資產等級，請確認填寫是否合理。"
    active_consistency_warnings.append(msg)
    st.markdown(f'<div class="check-warn">檢核2：⚠ {msg}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="check-ok">檢核2：✓ 流動資產與淨資產等級大致一致</div>', unsafe_allow_html=True)

# Check 3: investment goal vs knowledge
a7, a11 = answers.get(7, ""), answers.get(11, "")
if not a7 or not a11:
    st.markdown('<div class="check-pending">檢核3：— 請先填寫投資目的與知識水平</div>', unsafe_allow_html=True)
elif rank(a7) >= 4 and rank(a11) <= 2:
    msg = "投資目的較進取但市場知識較低，請向客戶確認。"
    active_consistency_warnings.append(msg)
    st.markdown(f'<div class="check-warn">檢核3：⚠ {msg}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="check-ok">檢核3：✓ 投資目的與知識水平未觸發提醒</div>', unsafe_allow_html=True)

# Check 4: expected return vs loss tolerance
a8, a9 = answers.get(8, ""), answers.get(9, "")
if not a8 or not a9:
    st.markdown('<div class="check-pending">檢核4：— 請先填寫期望報酬與可承受損失</div>', unsafe_allow_html=True)
elif rank(a8) >= 4 and rank(a9) <= 2:
    msg = "期望報酬較高但可承受損失偏低，請向客戶確認。"
    active_consistency_warnings.append(msg)
    st.markdown(f'<div class="check-warn">檢核4：⚠ {msg}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="check-ok">檢核4：✓ 期望報酬與損失承受度未觸發提醒</div>', unsafe_allow_html=True)

# Check 5: product experience vs margin experience
a12, a14 = answers.get(12, ""), answers.get(14, "")
if not a12 or not a14:
    st.markdown('<div class="check-pending">檢核5：— 請先填寫產品經驗與孖展經驗</div>', unsafe_allow_html=True)
elif rank(a14) >= 3 and rank(a12) <= 2:
    msg = "有較長孖展經驗但產品經驗顯示較基礎，請向客戶確認。"
    active_consistency_warnings.append(msg)
    st.markdown(f'<div class="check-warn">檢核5：⚠ {msg}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="check-ok">檢核5：✓ 孖展經驗與產品經驗未觸發提醒</div>', unsafe_allow_html=True)

st.caption("一致性檢核僅作提醒，不會自動調整 RPQ 分數或風險等級。")

consistency_ack = True
if active_consistency_warnings:
    consistency_ack = st.checkbox(
        "已向客戶確認上述一致性提醒，客戶確認原填答內容無誤",
        key="consistency_ack",
    )

witness_ack = True
if age65:
    witness_ack = st.checkbox(
        "已確認本案需依內規辦理獨立第三方見證",
        key="witness_ack",
    )


# ───────────────────────────── Margin / Credit disclosure ─────────────────────────────
st.markdown("---")
st.markdown("### 💳 Margin / Credit Information（獨立揭露）")
st.info(
    "本區為融資/信用資訊揭露，**不參與 RPQ 計分，也不由 RPQ 等級推導**。"
    "正式資料應來自核准的 Credit / Margin 系統或授信政策。"
)

c1, c2 = st.columns(2)
with c1:
    margin_facility = st.number_input(
        "融資額度 Margin Facility Amount (HK$)", min_value=0.0, step=10000.0, format="%.0f"
    )
    used_amount = st.number_input(
        "已動用額度 Used Amount (HK$)", min_value=0.0, step=10000.0, format="%.0f"
    )
with c2:
    credit_limit = st.number_input(
        "Credit Limit (HK$)", min_value=0.0, step=10000.0, format="%.0f"
    )
    credit_data_date = st.date_input("額度資料日期 Credit Data Date", key="credit_data_date")

available_limit = max(credit_limit - used_amount, 0.0)
st.markdown(
    f"""
    <div class="credit-box">
        <b>可用額度 Available Limit：</b> HK$ {available_limit:,.0f}<br>
        <span style="font-size:0.85rem;color:#666;">計算：Credit Limit − Used Amount；僅供畫面揭露。</span>
    </div>
    """,
    unsafe_allow_html=True,
)
credit_source = st.text_input("額度資料來源 / 備註 Credit Source / Note", placeholder="例如：Credit system / approved limit file")

if credit_limit > 0 and used_amount > credit_limit:
    st.warning("⚠ 已動用額度高於 Credit Limit，請確認來源資料。此提醒不影響 RPQ 結果。")
if credit_limit > 0 and margin_facility > credit_limit:
    st.warning("⚠ 融資額度高於 Credit Limit，請確認兩欄定義及來源資料。此提醒不影響 RPQ 結果。")


# ───────────────────────────── Confirmation and export ─────────────────────────────
st.markdown("---")
st.markdown("### ✅ 客戶確認 Client Confirmation")
st.markdown(
    """
1. 本人/吾等確認上述投資風險取向分析的結果正確反映本人的投資風險取向。  
2. 本人/吾等明白上述投資風險取向分析的結果將取代本人/吾等於開戶表之答案。  
3. Margin / Credit Information 為獨立揭露資訊，不屬於 RPQ 計分結果。
"""
)

confirm = st.checkbox("本人確認以上內容正確無誤")

final_ready = all_done and confirm and consistency_ack and witness_ack

if all_done and confirm and not consistency_ack:
    st.warning("RPQ 結果已產生；請完成一致性提醒確認後再下載最終紀錄。")
if all_done and confirm and not witness_ack:
    st.warning("RPQ 結果已產生；請確認 ≥65 歲內規第三方見證事項後再下載最終紀錄。")

if final_ready:
    st.success("問卷已完成並確認。可下載結果摘要。")

    grade_code, grade_desc = get_grade(total)
    final_account_grade = grade_code
    if account_type == "聯名 Joint":
        final_account_grade = higher_grade(grade_code, joint_other_grade)

    lines = [
        "富邦證券 — 客戶投資風險取向分析問卷結果摘要 (Prototype v1)",
        f"帳戶號碼：{account_no or '（未填）'}",
        f"客戶名稱：{account_name or '（未填）'}",
        f"帳戶類型：{account_type}",
        f"填寫日期：{fill_date}",
        "",
        "【RPQ 結果】",
        f"總分：{total} / 75",
        f"本份 RPQ 風險等級：{grade_code} {grade_desc}",
        "評分區間：G1 15-30 / G2 31-45 / G3 46-60 / G4 61-75",
    ]

    if account_type == "聯名 Joint":
        lines.append(f"其他聯名戶最高 RPQ 等級：{joint_other_grade or '未提供'}")
        lines.append(f"帳戶適用風險等級（內規取較高者）：{final_account_grade if joint_other_grade else '待其他聯名戶RPQ完成'}")

    lines.extend(["", "【各題答案】"])
    for q in QUESTIONS:
        a = answers[q["id"]]
        lines.append(f"Q{q['id']}. {q['cn']} → {a}（{get_score(a)}分）")

    lines.extend(["", "【一致性/內規紀錄】"])
    lines.append(f"≥65歲內規第三方見證提醒：{'是' if age65 else '否'}")
    lines.append(f"第三方見證事項已確認：{'是' if witness_ack else '否'}")
    if active_consistency_warnings:
        for idx, warning in enumerate(active_consistency_warnings, 1):
            lines.append(f"一致性提醒{idx}：{warning}")
        lines.append(f"一致性提醒已向客戶確認：{'是' if consistency_ack else '否'}")
    else:
        lines.append("一致性提醒：無")

    lines.extend(
        [
            "",
            "【Margin / Credit Information — 獨立揭露，不參與RPQ計分】",
            f"融資額度 Margin Facility Amount：HK$ {margin_facility:,.0f}",
            f"Credit Limit：HK$ {credit_limit:,.0f}",
            f"已動用額度 Used Amount：HK$ {used_amount:,.0f}",
            f"可用額度 Available Limit：HK$ {available_limit:,.0f}",
            f"額度資料日期：{credit_data_date}",
            f"額度資料來源/備註：{credit_source or '（未填）'}",
            "",
            "注意：RPQ 與 Margin/Credit Limit 為不同控制維度。Margin/Credit 資訊不得由 RPQ 分數直接推導。",
            "Prototype v1：正式上線前仍須依公司最新香港 Compliance / Credit / SMF 政策核准。",
        ]
    )
    summary = "\n".join(lines)

    st.download_button(
        label="📥 下載結果摘要（文字檔）",
        data=summary.encode("utf-8"),
        file_name=f"RPQ_v1_{account_no or '未命名'}_{fill_date}.txt",
        mime="text/plain",
    )
elif not all_done:
    st.caption("完成所有題目後，可產生 RPQ 結果；完成必要確認後可下載最終摘要。")
elif not confirm:
    st.info("RPQ 結果已產生。勾選客戶確認後，可完成最終紀錄。")


# ───────────────────────────── Footer ─────────────────────────────
st.markdown("---")
st.caption(
    "本問卷分析結果僅供風險屬性評估使用；公司保留依內部政策及適用規範進行最終審核之權利。"
    " 聯名帳戶暫依內規採較高投資風險取向。客戶財務狀況或風險取向變更時，應重新評估。"
)
st.caption("RPQ Prototype v1 · Fubon Securities (Hong Kong) Limited")
