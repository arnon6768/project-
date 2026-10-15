import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.integrate import quad

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Project 3: Numerical Integration",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS ตกแต่งแท็บ
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #f1f3f5;
        border-radius: 8px 8px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS (f(x) = sqrt(1 + e^x))
# ==========================================
def f(x):
    """ฟังก์ชัน f(x) = sqrt(1 + e^x) ตามโจทย์ Project 3"""
    return np.sqrt(1 + np.exp(x))

def trapezoidal_rule(a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integration, x, y, h

def simpsons_rule(a, b, n):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])
    return integration, x, y, h

# ==========================================
# SIDEBAR (ตั้งค่าพารามิเตอร์ขึ้นก่อน แล้วตามด้วยข้อมูลผู้จัดทำด้านล่าง)
# ==========================================
st.sidebar.title("⚙️ ตั้งค่าพารามิเตอร์ (Inputs)")

# Interactive Controls
a = st.sidebar.number_input("📌 ขอบเขตล่าง (a):", value=0.0, step=0.1)
b = st.sidebar.number_input("📌 ขอบเขตบน (b):", value=2.0, step=0.1)
n = st.sidebar.select_slider("🔢 จำนวนช่วงแบ่ง (n):", options=[8, 16, 32, 64], value=64)
method_choice = st.sidebar.selectbox("📈 เลือกวิธีแสดงผลกราฟ:", ["Trapezoidal Rule", "Simpson's Rule"])

st.sidebar.markdown("---")

# --------------------------------------------------------------------------
# ย้ายข้อมูลผู้จัดทำมาไว้ด้านล่างสุดของ Sidebar
# --------------------------------------------------------------------------
st.sidebar.title("👥 ข้อมูลผู้จัดทำ")
st.sidebar.markdown("""
*กลุ่มที่:* 3  
*สมาชิกผู้จัดทำ:*
1. นายกิตติศักดิ์ ชัยชนะ (65012345)
2. นายธนพล สุขใจ (65012346)
""")

# คำนวณค่าจริง Exact Value โดยใช้ scipy quad
exact_val, _ = quad(f, a, b)
trap_val, x_trap, y_trap, h_trap = trapezoidal_rule(a, b, n)
simp_val, x_simp, y_simp, h_simp = simpsons_rule(a, b, n)

# ==========================================
# MAIN CONTENT
# ==========================================
st.title("Project 3: Comparison of Numerical Integration Approximations")
st.caption(f"ประมาณค่าอินทิเกรตของ f(x) = √(1 + eⁿ) จาก a = {a} ถึง b = {b}")

tab1, tab2, tab3 = st.tabs([
    "📚 1. ทฤษฎี (Theory)", 
    "📊 2. ตัวจำลอง (Simulation & Graph)", 
    "📝 3. สรุปผล (Results & Output)"
])

# ------------------------------------------
# TAB 1: Theory
# ------------------------------------------
with tab1:
    st.header("📖 ทฤษฎีการประมาณค่าการอินทิเกรตทางตัวเลข")
    st.write("โจทย์กำหนดให้ประมาณค่าการอินทิเกรต:")
    
    st.latex(r"A = \int_{a}^{b} \sqrt{1 + e^x} \, dx")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Trapezoidal Rule")
        st.write("ประมาณค่าด้วยรูปสี่เหลี่ยมคางหมู:")
        st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{2} \left[ f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]")
        st.latex(r"h = \frac{b - a}{n
