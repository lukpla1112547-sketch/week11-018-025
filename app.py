import streamlit as st
import pandas as pd
import joblib

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Airline Satisfaction AI | Executive Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling แบบจัดเต็มด้วย Custom CSS (Luxury Executive Theme)
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
    }

    /* Background & Container */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Hero Banner Header */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.4);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        color: #93C5FD;
        margin-top: 8px;
    }

    /* Sidebar Custom Profile */
    .team-card {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .team-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1E293B;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }
    .team-member {
        font-size: 0.9rem;
        color: #334155;
        padding: 4px 0;
        display: flex;
        align-items: center;
    }

    /* Styled Prediction Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 14px 28px;
        border-radius: 14px;
        border: none;
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%);
        transform: translateY(-2px);
        box-shadow: 0 15px 25px -5px rgba(37, 99, 235, 0.5);
        color: #FFFFFF;
    }

    /* Custom Result Cards */
    .card-satisfied {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 8px solid #10B981;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    .card-dissatisfied {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 8px solid #EF4444;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.1);
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-desc {
        font-size: 0.95rem;
        color: #475569;
    }

    /* Metric Box */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Hero Banner (ส่วนหัวของแอป)
st.markdown("""
    <div class='hero-container'>
        <div class='hero-title'>✈️ AIRLINE SATISFACTION AI</div>
        <div class='hero-subtitle'>ระบบพยากรณ์และวิเคราะห์ความพึงพอใจผู้โดยสารระดับผู้บริหาร (Executive Intelligence)</div>
    </div>
""", unsafe_allow_html=True)

# 4. Sidebar แสดงโปรไฟล์ทีมพัฒนา
st.sidebar.markdown("""
    <div class='team-card'>
        <div class='team-header'>👨‍💻 ผู้จัดทำโครงงาน</div>
        <div class='team-member'>🔹 <b>018</b> &nbsp; ณิชกุล ทิพยอาสน์</div>
        <div class='team-member'>🔹 <b>025</b> &nbsp; พรสุดา สว่างศรี</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("📌 เกี่ยวกับระบบ")
st.sidebar.info("""
ระบบนี้ใช้ **Machine Learning (Random Forest)** ในการประมวลผลปัจจัย 22 ด้าน เพื่อทำนายแนวโน้มความพึงพอใจของผู้โดยสารสายการบินล่วงหน้า
""")

# 5. โหลดโมเดล
@st.cache_resource
def load_model():
    return joblib.load('airline_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"❌ ไม่สามารถโหลดโมเดลได้: {e}")
    st.stop()

# 6. ฟอร์มรับข้อมูล (Tabs Layout)
st.subheader("📋 ระบุข้อมูลเพื่อประมวลผล")

tab1, tab2, tab3 = st.tabs([
    "👤 ข้อมูลผู้โดยสาร & เที่ยวบิน", 
    "⭐ คะแนนประเมินการบริการ (0-5)", 
    "⏱️ ข้อมูลเวลาและการดีเลย์"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("เพศ (Gender)", ["Male", "Female"])
        customer_type = st.selectbox("ประเภทลูกค้า (Customer Type)", ["Loyal Customer", "disloyal Customer"])
        age = st.number_input("อายุ (Age)", min_value=1, max_value=100, value=30)
    with col2:
        travel_type = st.selectbox("วัตถุประสงค์การเดินทาง (Type of Travel)", ["Personal Travel", "Business travel"])
        travel_class = st.selectbox("ชั้นผู้โดยสาร (Class)", ["Business", "Eco", "Eco Plus"])
        flight_distance = st.number_input("ระยะทางบิน (Flight Distance - Miles)", min_value=0, value=1000)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        inflight_wifi = st.slider("📶 Inflight Wifi Service", 0, 5, 3)
        dep_arr_time = st.slider("⏰ Departure/Arrival Time Convenient", 0, 5, 3)
        ease_online_booking = st.slider("📱 Ease of Online Booking", 0, 5, 3)
        gate_location = st.slider("🚪 Gate Location", 0, 5, 3)
        food_and_drink = st.slider("🍽️ Food and Drink", 0, 5, 3)
        online_boarding = st.slider("🎟️ Online Boarding", 0, 5, 3)
        seat_comfort = st.slider("💺 Seat Comfort", 0, 5, 3)
    with col2:
        inflight_entertainment = st.slider("🎬 Inflight Entertainment", 0, 5, 3)
        onboard_service = st.slider("🧑‍✈️ On-board Service", 0, 5, 3)
        leg_room = st.slider("🦵 Leg Room Service", 0, 5, 3)
        baggage_handling = st.slider("🧳 Baggage Handling", 0, 5, 3)
        checkin_service = st.slider("📋 Check-in Service", 0, 5, 3)
        inflight_service = st.slider("✈️ Inflight Service", 0, 5, 3)
        cleanliness = st.slider("✨ Cleanliness", 0, 5, 3)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        departure_delay = st.number_input("Departure Delay (นาที)", min_value=0, value=0)
    with col2:
        arrival_delay = st.number_input("Arrival Delay (นาที)", min_value=0, value=0)

st.markdown("<br>", unsafe_allow_html=True)

# 7. ปุ่มประมวลผล
if st.button("🚀 ประมวลผลและทำนายความพึงพอใจ", use_container_width=True):
    # Encoding ข้อมูล
    gender_val = 1 if gender == "Male" else 0
    cust_val = 0 if customer_type == "Loyal Customer" else 1
    travel_val = 0 if travel_type == "Business travel" else 1
    class_dict = {"Business": 0, "Eco": 1, "Eco Plus": 2}
    class_val = class_dict[travel_class]

    # รวมข้อมูลเข้า Dictionary 22 คอลัมน์
    data_dict = {
        'Gender': gender_val, 'Customer Type': cust_val, 'Age': age,
        'Type of Travel': travel_val, 'Class': class_val, 'Flight Distance': flight_distance,
        'Inflight wifi service': inflight_wifi, 'Departure/Arrival time convenient': dep_arr_time,
        'Ease of Online booking': ease_online_booking, 'Gate location': gate_location,
        'Food and drink': food_and_drink, 'Online boarding': online_boarding,
        'Seat comfort': seat_comfort, 'Inflight entertainment': inflight_entertainment,
        'On-board service': onboard_service, 'Leg room service': leg_room,
        'Baggage handling': baggage_handling, 'Checkin service': checkin_service,
        'Inflight service': inflight_service, 'Cleanliness': cleanliness,
        'Departure Delay in Minutes': departure_delay, 'Arrival Delay in Minutes': arrival_delay
    }

    input_df = pd.DataFrame([data_dict])[model.feature_names_in_]

    # ทำนายผล
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    prob_percent = max(probabilities) * 100

    st.markdown("---")
    st.subheader("📊 ผลการวิเคราะห์ และ คำแนะนำเชิงบริหาร")

    col_res1, col_res2 = st.columns([2.5, 1])

    with col_res1:
        if prediction == 1:
            st.markdown(f"""
                <div class='card-satisfied'>
                    <div class='card-title' style='color: #065F46;'>🎉 ผู้โดยสารมีความพึงพอใจ (Satisfied)</div>
                    <div class='card-desc'>
                        <b>กลยุทธ์รักษาลูกค้า:</b> บริการโดยรวมสร้างความประทับใจได้ดี ควรรักษามาตรฐานระดับสูง โดยเฉพาะจุดเด่นบริการด้านความสะดวกสบายและการดูแลบนเที่ยวบิน
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # วิเคราะห์หาจุดอ่อน
            low_scores = []
            service_scores = {
                "Inflight Wifi": inflight_wifi, "Online Boarding": online_boarding,
                "Seat Comfort": seat_comfort, "Inflight Entertainment": inflight_entertainment,
                "Cleanliness": cleanliness, "Food & Drink": food_and_drink
            }
            for k, v in service_scores.items():
                if v <= 2:
                    low_scores.append(k)
            
            weakness_text = f"<b>จุดบกพร่องที่ต้องปรับปรุงด่วน:</b> {', '.join(low_scores)}" if low_scores else "<b>จุดบกพร่องที่ต้องปรับปรุงด่วน:</b> บริการการต่อสาย/ดีเลย์ และการต้อนรับของพนักงาน"

            st.markdown(f"""
                <div class='card-dissatisfied'>
                    <div class='card-title' style='color: #991B1B;'>⚠️ ผู้โดยสารไม่พึงพอใจ / ปานกลาง (Neutral or Dissatisfied)</div>
                    <div class='card-desc'>
                        {weakness_text}<br>
                        <i>ข้อเสนอแนะ: สายการบินควรรีบเข้าทำการแก้ไขในจุดที่ได้คะแนนประเมินต่ำกว่าเกณฑ์มาตรฐาน เพื่อป้องกันการสูญเสียลูกค้าในระยะยาว</i>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_res2:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem; color: #64748B; font-weight: 600;'>AI CONFIDENCE RATE</div>
                <div style='font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin: 8px 0;'>{prob_percent:.1f}%</div>
                <div style='font-size: 0.8rem; color: #10B981;'>✓ พยากรณ์ด้วยความแม่นยำสูง</div>
            </div>
        """, unsafe_allow_html=True)

# 8. Footer ท้ายหน้า
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #94A3B8; font-size: 0.85rem; padding-bottom: 20px;'>
        © 2026 Airline Satisfaction Intelligence Unit | พัฒนาโดย <b>ณิชกุล ทิพยอาสน์ (018)</b> & <b>พรสุดา สว่างศรี (025)</b>
    </div>
""", unsafe_allow_html=True)