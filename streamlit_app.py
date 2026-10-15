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

# Custom CSS ตกแต่งแท็บและกล่องข้อความชื่อกลุ่ม
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
    /* สไตล์กล่องแสดงชื่อกลุ่มบนหน้าหลัก */
    .group-box {
        background-color: #e8f4f8;
        border-left: 5px solid #1f77b4;
        padding: 12px 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #0f4c81;
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
# SIDEBAR (แปะข้อความชื่อผู้จัดทำใน Sidebar)
# ==========================================
st.sidebar.title("👥 ข้อมูลผู้จัดทำ")

# --------------------------------------------------------------------------
# [จุดที่ 1] แก้ไขข้อความรายชื่อกลุ่มตรงนี้ได้เลย ( Sidebar )
# --------------------------------------------------------------------------
st.sidebar.markdown("""
*กลุ่มที่:* 3  
*สมาชิกผู้จัดทำ:*
1. นายกิตติศักดิ์ ชัยชนะ (65012345)
2. นายธนพล สุขใจ (65012346)
""")
st.sidebar.markdown("---")

st.sidebar.title("⚙️ ตั้งค่าพารามิเตอร์ (Inputs)")

# Interactive Controls
a = st.sidebar.number_input("📌 ขอบเขตล่าง (a):", value=0.0, step=0.1)
b = st.sidebar.number_input("📌 ขอบเขตบน (b):", value=2.0, step=0.1)
n = st.sidebar.select_slider("🔢 จำนวนช่วงแบ่ง (n):", options=[8, 16, 32, 64], value=64)
method_choice = st.sidebar.selectbox("📈 เลือกวิธีแสดงผลกราฟ:", ["Trapezoidal Rule", "Simpson's Rule"])

# คำนวณค่าจริง Exact Value โดยใช้ scipy quad
exact_val, _ = quad(f, a, b)
trap_val, x_trap, y_trap, h_trap = trapezoidal_rule(a, b, n)
simp_val, x_simp, y_simp, h_simp = simpsons_rule(a, b, n)

# ==========================================
# MAIN CONTENT
# ==========================================
st.title("Project 3: Comparison of Numerical Integration Approximations")

# --------------------------------------------------------------------------
# [จุดที่ 2] แก้ไขข้อความรายชื่อกลุ่มตรงนี้ได้เลย ( หน้าหลัก )
# --------------------------------------------------------------------------
st.markdown("""
<div class="group-box">
    <b>📌 ผู้จัดทำ (กลุ่มที่ 3):</b><br>
    • นายกิตติศักดิ์ ชัยชนะ (65012345) &nbsp;&nbsp;|&nbsp;&nbsp; • นายธนพล สุขใจ (65012346)
</div>
""", unsafe_allow_html=True)

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
        st.latex(r"h = \frac{b - a}{n}")
        
    with col2:
        st.subheader("2. Simpson's Rule")
        st.write("ประมาณค่าด้วยสมการพาราโบลา (ใช้ $n$ เป็นจำนวนคู่):")
        st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{3} \left[ f(x_0) + 4\sum_{i \text{ odd}} f(x_i) + 2\sum_{i \text{ even}} f(x_i) + f(x_n) \right]")
        st.latex(r"h = \frac{b - a}{n}")

# ------------------------------------------
# TAB 2: Dynamic Visualization
# ------------------------------------------
with tab2:
    st.header("📊 กราฟจำลองพื้นที่และการแสดงผลคำนวณ")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 ค่าจริง (Exact Value A)", f"{exact_val:.6f}")
    m2.metric("📐 Trapezoidal Approx.", f"{trap_val:.6f}", f"Error: {abs(exact_val - trap_val):.2e}", delta_color="inverse")
    m3.metric("🔵 Simpson's Approx.", f"{simp_val:.6f}", f"Error: {abs(exact_val - simp_val):.2e}", delta_color="inverse")
    
    st.markdown("---")
    
    st.subheader(f"พื้นที่ประมาณค่าด้วยวิธี {method_choice} (n = {n})")
    
    x_dense = np.linspace(a - 0.2, b + 0.2, 300)
    y_dense = f(x_dense)
    
    fig = go.Figure()
    
    # เส้นฟังก์ชัน f(x)
    fig.add_trace(go.Scatter(
        x=x_dense, y=y_dense, 
        mode='lines', name='f(x) = √(1 + eⁿ)',
        line=dict(color='crimson', width=2.5)
    ))
    
    # แรเงาพื้นที่ใต้กราฟ
    x_curr = x_trap if method_choice == "Trapezoidal Rule" else x_simp
    y_curr = y_trap if method_choice == "Trapezoidal Rule" else y_simp
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_curr, x_curr[::-1]]),
        y=np.concatenate([y_curr, np.zeros_like(y_curr)]),
        fill='toself',
        fillcolor='rgba(30, 144, 255, 0.6)',
        line=dict(color='blue'),
        name=f'พื้นที่ประมาณค่า ({method_choice})'
    ))
    
    # จุดพิกัดบนกราฟ
    fig.add_trace(go.Scatter(
        x=x_curr, y=y_curr,
        mode='markers', name='Points',
        marker=dict(size=5, color='black')
    ))
    
    fig.update_layout(
        title=f"การจำลองพื้นที่ใต้โค้งบนช่วง [{a}, {b}] (n = {n})",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        template="plotly_white",
        height=480
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# TAB 3: Step-by-Step & Tables
# ------------------------------------------
with tab3:
    st.header("📝 การคำนวณทีละขั้นตอนและสรุปผลตามโจทย์")
    
    with st.expander("🔍 ดูขั้นตอนการคำนวณทีละขั้นตอน (Step-by-Step Calculation)", expanded=True):
        st.markdown(f"""
        1. *กำหนดค่าพารามิเตอร์:* $a = {a}$, $b = {b}$, $n = {n}$
        2. *คำนวณความกว้างช่วงย่อย ($h$):* $h = \\frac{{{b} - {a}}}{{{n}}} = {h_trap:.6f}$
        3. *คำนวณค่า $f(x)$ ที่จุดขอบ:* $f({a}) = {f(a):.6f}$, $f({b}) = {f(b):.6f}$
        4. *ผลลัพธ์การคำนวณ:*
           - *Exact Value ($A$):* {exact_val:.6f}
           - *Trapezoidal Value ($\tilde{{A}}$):* {trap_val:.6f} | *Error:* {abs(exact_val - trap_val):.6e}
           - *Simpson Value ($\tilde{{A}}$):* {simp_val:.6f} | *Error:* {abs(exact_val - simp_val):.6e}
        """)

    st.subheader("1. ตารางแสดงค่า Error ตามจำนวนช่วง n (ข้อ 3 ในโจทย์)")
    n_list = [8, 16, 32, 64]
    trap_errs, simp_errs = [], []
    
    for n_val in n_list:
        t_v, _, _, _ = trapezoidal_rule(a, b, n_val)
        s_v, _, _, _ = simpsons_rule(a, b, n_val)
        trap_errs.append(abs(exact_val - t_v))
        simp_errs.append(abs(exact_val - s_v))
        
    df_n_error = pd.DataFrame({
        "n": n_list,
        "Trapezoidal Error |A - A~|": [f"{e:.6e}" for e in trap_errs],
        "Simpson Error |A - A~|": [f"{e:.6e}" for e in simp_errs]
    })
    st.dataframe(df_n_error, use_container_width=True)

    st.subheader("2. ตารางเปรียบเทียบ Error เมื่อ n = 64 (ข้อ 4 ในโจทย์)")
    t_64, _, _, _ = trapezoidal_rule(a, b, 64)
    s_64, _, _, _ = simpsons_rule(a, b, 64)
    
    df_compare_64 = pd.DataFrame({
        "Method": ["Trapezoidal", "Simpson"],
        "A": [f"{exact_val:.6f}", f"{exact_val:.6f}"],
        "A~": [f"{t_64:.6f}", f"{s_64:.6f}"],
        "Error = |A - A~|": [f"{abs(exact_val - t_64):.6e}", f"{abs(exact_val - s_64):.6e}"]
    })
    st.dataframe(df_compare_64, use_container_width=True)

    st.subheader("3. Output ที่ได้จาก Python ตาม Format ในโจทย์")
    st.code(
f"""Method          A~1          Error A1
----------------------------------------
Trapezoidal     {t_64:<12.6f} {abs(exact_val - t_64):.5E}
Simpson         {s_64:<12.6f} {abs(exact_val - s_64):.5E}""", 
        language="text"
    )
