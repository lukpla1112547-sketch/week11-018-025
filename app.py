# -*- coding: utf-8 -*-
"""Streamlit app — ทีม อดทนจนกว่าจะแลนด์ (018-025) · AI ทำนายความพึงพอใจผู้โดยสารสายการบิน
เวอร์ชันใช้เฉพาะ 7 ช่องกรอกที่ GA คัดเลือก (ผ่านการทดลอง 26 → 8 คอลัมน์ → ยุบเป็น 7 ช่องกรอก)
"""
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Airline Satisfaction AI | GA-7 | ทีม 018-025",
    page_icon="✈️",
    layout="wide",
)
BASE = Path(__file__).resolve().parent


@st.cache_resource
def load_model():
    return joblib.load(BASE / "airline_model.joblib")


@st.cache_data
def load_meta():
    with open(BASE / "team_features.json", encoding="utf-8") as f:
        return json.load(f)


model = load_model()
meta = load_meta()
FEATURES = meta["features"]
TEAM = meta.get("members", [["018", "ณิชกุล ทิพยอาสน์"], ["025", "พรสุดา สว่างศรี"]])
ACC = float(meta.get("test_accuracy", 0.9475))
F1 = float(meta.get("f1", 0.9391))
CV = float(meta.get("cv_accuracy", 0.9462))
N_ROWS = int(meta.get("n_rows", 103902))
RATE = float(meta.get("satisfied_rate", 0.4333))
IMP = meta.get("feature_importance", {})
BASE22 = meta.get("baseline_all_features_acc", 0.9623)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Kanit','Leelawadee UI',Tahoma,sans-serif; }

  /* ── ล็อกพื้นหลังให้เป็นโหมดสว่างเสมอ (ผู้ใช้ที่ตั้งเครื่องเป็น dark mode ก็อ่านได้) ── */
  [data-testid="stAppViewContainer"], .stApp, [data-testid="stMain"], section.main {
      background-color: #F8FAFC !important; color-scheme: light !important; }
  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
  [data-testid="stSidebar"] > div { background-color: #FFFFFF !important; }
  [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background-color: #F8FAFC !important; }

  /* ── ล็อกสีตัวหนังสือทุกประเภทเป็นโทนเข้ม อ่านชัดบนพื้นสว่าง ── */
  [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
  [data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4,
  [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] *,
  [data-testid="stExpander"] summary, [data-testid="stExpander"] p,
  [data-testid="stDataFrame"] *, [data-testid="stAlert"], [data-testid="stAlert"] *,
  [data-baseweb="select"] *, [data-baseweb="input"] input,
  .stApp input, .stApp textarea, .stApp small,
  [role="tab"], [role="tab"] * { color: #0F172A !important; }
  [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #475569 !important; }
  [data-testid="stSliderThumbValue"], [data-testid="stSliderThumbValue"] *,
  [data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] { color: #0F172A !important; }
  [role="tab"][aria-selected="true"], [role="tab"][aria-selected="true"] * { color: #1D4ED8 !important; }
  .stApp code, .stApp pre { color: #0F172A !important; background: #F1F5F9 !important; }

  /* ── กล่อง/การ์ดของทีม (ใส่ .stApp นำหน้าเพื่อให้ความสำคัญสูงกว่ากฎด้านบน) ── */
  .stApp .hero-container {
      background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
      padding: 2.2rem 2rem 1.8rem; border-radius: 20px;
      box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.4); margin-bottom: 22px;
  }
  .stApp .hero-title, .stApp .hero-title * {
      font-size: 2.3rem; font-weight: 700; margin: 0; color: #FFFFFF !important; letter-spacing: -0.5px; }
  .stApp .hero-subtitle, .stApp .hero-subtitle * {
      font-size: 1.05rem; font-weight: 300; color: #DBEAFE !important; margin-top: 8px; }
  .stApp .hero-subtitle b { color: #FFFFFF !important; }
  .chips { margin-top: 14px; }
  .stApp .chip { display:inline-block; background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35);
          padding:6px 14px; border-radius:999px; font-size:.85rem; margin:0 8px 8px 0; color:#FFFFFF !important; }
  .stApp .chip.solid { background:#FFFFFF; color:#1E3A8A !important; font-weight:700; }
  .stApp .team-card { background:#FFFFFF; padding:16px; border-radius:16px; border:1px solid #E2E8F0;
               box-shadow:0 4px 12px rgba(0,0,0,.03); margin-bottom:18px; }
  .stApp .team-header { font-size:.95rem; font-weight:700; color:#1E293B !important;
                 border-bottom:2px solid #3B82F6; padding-bottom:6px; margin-bottom:10px; }
  .stApp .team-member, .stApp .team-member * { font-size:.9rem; color:#334155 !important; padding:4px 0; }
  div.stFormSubmitButton > button, div.stButton > button {
      background: linear-gradient(90deg,#2563EB 0%,#1D4ED8 100%) !important;
      font-size:1.1rem !important; font-weight:600 !important; padding:12px 26px !important;
      border-radius:14px !important; border:none !important;
      box-shadow:0 10px 20px -5px rgba(37,99,235,.4) !important; }
  div.stFormSubmitButton > button p, div.stButton > button p, div.stFormSubmitButton > button * ,
  div.stButton > button * { color: #FFFFFF !important; }
  .stApp .card-title { font-size:1.25rem; font-weight:700; margin-bottom:6px; }
  .stApp .card-desc, .stApp .card-desc * { font-size:.95rem; color:#334155 !important; line-height:1.6; }
  .stApp .card-satisfied { background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 100%);
      border-left:8px solid #10B981; padding:20px; border-radius:16px; }
  .stApp .card-dissatisfied { background:linear-gradient(135deg,#FEF2F2 0%,#FEE2E2 100%);
      border-left:8px solid #EF4444; padding:20px; border-radius:16px; }
  .stApp .metric-card { background:#FFFFFF; border-radius:16px; padding:18px; border:1px solid #E2E8F0;
      text-align:center; box-shadow:0 4px 12px rgba(0,0,0,.03); }
  [data-testid="stMetric"] { background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:12px 16px; }
  [data-testid="stMetricValue"], [data-testid="stMetricValue"] * { color:#1E3A8A !important; }
  [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { color:#475569 !important; }
  div[data-testid="stVerticalBlockBorderWrapper"] { border-radius:16px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-container">
  <div class="hero-title">✈️ AIRLINE SATISFACTION AI</div>
  <div class="hero-subtitle">ระบบพยากรณ์ความพึงพอใจผู้โดยสาร — ใช้เฉพาะ <b>{len(FEATURES)} ช่องกรอก</b>
     ที่ขั้นตอนวิธีเชิงพันธุกรรม (GA) คัดเลือกไว้ (จาก 26 คอลัมน์ → 8 คอลัมน์ → ยุบเป็น {len(FEATURES)} ช่องกรอก)</div>
  <div class="chips">
    <div class="chip solid">ทีม อดทนจนกว่าจะแลนด์ 018-025</div>
    {''.join(f'<div class="chip">{c} {n}</div>' for c, n in TEAM)}
    <div class="chip">ความแม่น {ACC*100:.2f}% · CV {CV*100:.2f}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
    <div class='team-card'>
        <div class='team-header'>👩‍💻 ผู้จัดทำโครงงาน</div>
        {''.join(f"<div class='team-member'>🔹 <b>{c}</b> &nbsp; {n}</div>" for c, n in TEAM)}
    </div>
""", unsafe_allow_html=True)
st.sidebar.title("📌 เกี่ยวกับระบบ")
st.sidebar.info(f"""
ระบบนี้ใช้ **Random Forest (100 ต้น)** บน **{len(FEATURES)} ช่องกรอกที่ GA คัดเลือก** จากข้อมูลผู้โดยสารจริง {N_ROWS:,} ราย
(ความแม่น {ACC*100:.2f}%) — ฟอร์มนี้ตรงกับฟีเจอร์ของโมเดล ไม่ขาด ไม่เกิน
""")
st.sidebar.caption("เปรียบเทียบ: ใช้ทั้ง 22 ฟีเจอร์แม่น "
                   f"{BASE22*100:.2f}% · ใช้ 7 ช่องกรอกของ GA แม่น {ACC*100:.2f}% (ต่างกันเพียง {(BASE22-ACC)*100:.2f} จุด)")

tab_p, tab_m, tab_h = st.tabs(["🎯 ทำนายความพึงพอใจ", "🧠 ข้อมูลโมเดล & ผลการทดลอง", "📘 วิธีใช้ & ข้อจำกัด"])

with tab_p:
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        with st.form("sat_form"):
            st.markdown("**ให้คะแนนบริการที่ผู้โดยสารประเมิน (0–5)**")
            st.caption("ทั้ง 5 ข้อนี้คือปัจจัยที่ GA คัดว่ามีอิทธิพลที่สุดต่อความพึงพอใจ")
            c1, c2 = st.columns(2)
            with c1:
                wifi = st.slider("📶 Inflight wifi service", 0, 5, 3)
                online_boarding = st.slider("🎟️ Online boarding", 0, 5, 3)
                seat = st.slider("💺 Seat comfort", 0, 5, 3)
            with c2:
                entertainment = st.slider("🎬 Inflight entertainment", 0, 5, 3)
                baggage = st.slider("🧳 Baggage handling", 0, 5, 3)
            st.divider()
            st.markdown("**ข้อมูลผู้โดยสาร**")
            c3, c4 = st.columns(2)
            with c3:
                ctype = st.selectbox("ประเภทลูกค้า (Customer Type)", ["Loyal Customer", "disloyal Customer"])
            with c4:
                ttype = st.selectbox("วัตถุประสงค์การเดินทาง (Type of Travel)", ["Business travel", "Personal Travel"])
            go = st.form_submit_button("🚀 ประมวลผลและทำนายความพึงพอใจ", width="stretch")
    with right:
        if go:
            row = {
                "Inflight wifi service": wifi,
                "Online boarding": online_boarding,
                "Seat comfort": seat,
                "Inflight entertainment": entertainment,
                "Baggage handling": baggage,
                "Customer Type_Loyal Customer": 1 if ctype == "Loyal Customer" else 0,
                "Type of Travel_Business travel": 1 if ttype == "Business travel" else 0,
            }
            X = pd.DataFrame([row])[FEATURES]
            pred = int(model.predict(X)[0])
            proba = model.predict_proba(X)[0]
            p_sat = float(proba[list(model.classes_).index(1)])
            st.metric("โอกาสที่ผู้โดยสารจะพึงพอใจ", f"{p_sat:.1%}")
            st.progress(min(max(p_sat, 0.0), 1.0))
            if pred == 1:
                st.markdown("""
                <div class='card-satisfied'>
                  <div class='card-title' style='color:#065F46;'>🎉 แนวโน้มพึงพอใจ (Satisfied)</div>
                  <div class='card-desc'><b>ข้อเสนอเชิงบริหาร:</b> ประสบการณ์โดยรวมดี ควรรักษามาตรฐานบริการ
                  และใช้กลุ่มนี้เป็นกลุ่มอ้างอิง (benchmark) ในการพัฒนาเส้นทางอื่น</div>
                </div>""", unsafe_allow_html=True)
            else:
                weak = [name for name, val in [("Inflight wifi service", wifi), ("Online boarding", online_boarding),
                                               ("Seat comfort", seat), ("Inflight entertainment", entertainment),
                                               ("Baggage handling", baggage)] if val <= 2]
                txt = ("จุดที่ควรปรับปรุงด่วน: " + ", ".join(weak)) if weak else \
                      "คะแนนบริการอยู่ในระดับกลาง ควรเน้นประชาสัมพันธ์จุดเด่นและลดความล่าช้าของเที่ยวบิน"
                st.markdown(f"""
                <div class='card-dissatisfied'>
                  <div class='card-title' style='color:#991B1B;'>⚠️ แนวโน้มไม่พึงพอใจ (Neutral or Dissatisfied)</div>
                  <div class='card-desc'><b>ข้อเสนอเชิงบริหาร:</b> {txt}<br>
                  <i>แนะนำให้ปรับปรุงบริการด้านบนก่อน แล้วติดตามคะแนนรอบถัดไป</i></div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card" style="margin-top:12px">
              <div style="font-size:.85rem;color:#64748B;font-weight:600">จำนวนช่องกรอกที่ใช้</div>
              <div style="font-size:1.9rem;font-weight:700;color:#1E3A8A">{len(FEATURES)} ช่อง</div>
              <div style="font-size:.8rem;color:#10B981">✓ ตรงกับฟีเจอร์ของโมเดลทั้งหมด</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("ดูค่าที่ส่งเข้าโมเดล + ฟีเจอร์ที่โมเดลให้น้ำหนักมากที่สุด"):
                st.dataframe(X.T.rename(columns={0: "ค่าที่ส่งเข้าโมเดล"}), width="stretch")
                for f, v in list(IMP.items())[:7]:
                    st.write(f"- {f} — **{v*100:.1f}%**")
        else:
            st.info("ให้คะแนนบริการด้านซ้าย แล้วกด **ประมวลผลและทำนายความพึงพอใจ** เพื่อดูผล")
            st.caption("ระบบใช้เพียง 7 ช่องกรอก — ไม่ต้องกรอกข้อมูลเที่ยวบิน ดีเลย์ หรือข้อมูลส่วนตัวอื่น")

with tab_m:
    st.markdown("#### สรุปโมเดลสุดท้ายของทีม")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ชนิดโมเดล", "Random Forest")
    m2.metric("จำนวนช่องกรอก", f"{len(FEATURES)}")
    m3.metric("ความแม่น (ชุดทดสอบ)", f"{ACC*100:.2f}%")
    m4.metric("F1 / CV", f"{F1:.3f} / {CV:.4f}")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("**22 ฟีเจอร์ vs 7 ช่องกรอกที่ GA คัด** (ชุดทดสอบ 20% เดียวกัน)")
            rows = meta.get("compare_table", [])
            if rows:
                st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
            st.caption("หมายเหตุ: ตอนนี้ครบทุกโมเดลแล้ว รวม SVM ที่เดิมมีแต่ผลชุด 22 ฟีเจอร์")
    with c2:
        with st.container(border=True):
            st.markdown("**การทดลอง GA: 26 → 8 คอลัมน์ → 7 ช่องกรอก**")
            st.write("- ค้นหาบน **26 คอลัมน์** ที่เข้ารหัสแล้ว (one-hot) → GA เลือก **8 คอลัมน์**")
            st.write("- 2 คอลัมน์ของ Customer Type (Loyal / disloyal) ยุบเป็นดรอปดาวน์เดียว "
                     "→ แอปจึงมี **7 ช่องกรอก**")
            st.write(f"- accuracy: ทุกฟีเจอร์ **{meta.get('ga_baseline_on_26', 0.9371)*100:.2f}%** → "
                     f"ชุดที่ GA คัด **{meta.get('ga_on_26', 0.9367)*100:.2f}%** (ต่างกันเพียง "
                     f"{(meta.get('ga_baseline_on_26', 0.9371)-meta.get('ga_on_26', 0.9367))*100:.2f} จุด)")
        with st.container(border=True):
            st.markdown("**ฟีเจอร์ที่โมเดลให้น้ำหนักมากที่สุด**")
            for f, v in list(IMP.items())[:7]:
                st.write(f"- {f} — **{v*100:.1f}%**")

with tab_h:
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("#### วิธีใช้")
            st.markdown(
                "1. ให้คะแนน **5 บริการที่ GA คัดเลือก** (wifi, online boarding, seat comfort, "
                "inflight entertainment, baggage handling) ตั้งแต่ 0–5\n"
                "2. เลือก **ประเภทลูกค้า** และ **วัตถุประสงค์การเดินทาง**\n"
                "3. กด **ประมวลผลและทำนายความพึงพอใจ** → อ่าน % โอกาสพึงพอใจและข้อเสนอ\n"
                "4. ใช้เป็นข้อมูลประกอบการตัดสินใจของฝ่ายบริการ ไม่ใช่คำตัดสินสุดท้าย")
    with c2:
        with st.container(border=True):
            st.markdown("#### ข้อจำกัดของโมเดล")
            st.markdown(
                "1. ใช้เพียง 7 ช่องกรอก ทำให้ความแม่นลดลงเล็กน้อยจาก 22 ฟีเจอร์ "
                f"({BASE22*100:.2f}% → {ACC*100:.2f}%) แต่ใช้งานจริงง่ายกว่ามาก\n"
                "2. คะแนนบริการเป็น **การรับรู้ของผู้โดยสาร** (self-report) ไม่ใช่คุณภาพบริการที่วัดได้จริง\n"
                "3. ข้อมูลเป็นผู้โดยสารสายการบินในสหรัฐฯ ปี 2018 — บริบทสายการบินอื่นอาจต่างกัน\n"
                "4. โมเดลไม่ใช้ข้อมูลส่วนตัว (อายุ เพศ ระยะทาง) จึงลดความเสี่ยงด้านข้อมูลส่วนบุคคล")

st.markdown(f"""
<div style='text-align:center;color:#94A3B8;font-size:.85rem;padding:18px 0'>
  จัดทำโดย <b>ทีม อดทนจนกว่าจะแลนด์</b> — {' · '.join(f'{c} {n}' for c, n in TEAM)}<br>
  วิชา DT36822N ปัญญาประดิษฐ์เพื่อธุรกิจดิจิทัล · ใบงานสัปดาห์ที่ 11-12 ·
  ข้อมูล: Airline Passenger Satisfaction {N_ROWS:,} ราย · โมเดล 7 ช่องกรอกที่ GA คัดเลือก
</div>
""", unsafe_allow_html=True)
