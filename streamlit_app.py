import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.integrate import quad

# ==========================================
# PAGE CONFIG & CUSTOM CSS (ตกแต่งความสวยงาม)
# ==========================================
st.set_page_config(
    page_title="Numerical Integration Dashboard",
    page_icon="🧮",
    layout="wide"
)

# ตกแต่ง UI ด้วย Custom CSS ให้ดูเป็นแอปพลิเคชันมืออาชีพ
st.markdown("""
<style>
    /* ปรับแต่งการ์ดแสดงผล */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f3f5;
        border-radius: 8px 8px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def f(x):
    """ฟังก์ชัน f(x) = sqrt(1 + e^x)"""
    return np.sqrt(1 + np.exp(x))

def trapezoidal_rule(a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integration, x, y, h

def simpsons_rule(a, b, n):
    if n % 2 != 0:
        n += 1  # ปรับเป็นจำนวนคู่สำหรับ Simpson's rule
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])
    return integration, x, y, h

# ==========================================
# REQUIREMENT 5: Layout Organization (Sidebar)
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/calculator.png", width=70)
st.sidebar.title("⚙️ แผงควบคุม (Controls)")
st.sidebar.markdown("---")

# REQUIREMENT 1: Interactive Controls (ใช้งาน 4 ชนิด)
# Control 1: st.number_input
a = st.sidebar.number_input("📌 ขอบเขตล่าง (a):", value=0.0, step=0.1)

# Control 2: st.number_input
b = st.sidebar.number_input("📌 ขอบเขตบน (b):", value=1.0, step=0.1)

# Control 3: st.select_slider
n = st.sidebar.select_slider("🔢 จำนวนช่วงแบ่ง (n):", options=[8, 16, 32, 64], value=64)

# Control 4: st.selectbox
method_choice = st.sidebar.selectbox("📈 เลือกวิธีกราฟจำลอง:", ["Trapezoidal Rule", "Simpson's Rule"])

# Control 5: st.color_picker (แถมตกแต่งกราฟ)
chart_color = st.sidebar.color_picker("🎨 เลือกลูกเล่นสีแถบแรเงา:", "#3366CC")

# คำนวณค่าจริงและค่าประมาณ
exact_val, _ = quad(f, a, b)
trap_val, x_trap, y_trap, h_trap = trapezoidal_rule(a, b, n)
simp_val, x_simp, y_simp, h_simp = simpsons_rule(a, b, n)

# ==========================================
# MAIN CONTENT & REQUIREMENT 5: st.tabs
# ==========================================
st.title("🧮 Project 3: Comparison of Numerical Integration Approximations")
st.caption("แอปพลิเคชันเปรียบเทียบการประมาณค่าการอินทิเกรตทางตัวเลขแบบโต้ตอบ")

tab1, tab2, tab3 = st.tabs([
    "📚 1. ทฤษฎี (Theory)", 
    "📊 2. ตัวจำลอง (Dynamic Visualization)", 
    "📝 3. สรุปผล & Step-by-Step"
])

# ------------------------------------------
# TAB 1: ทฤษฎี (Mathematical Notation)
# ------------------------------------------
with tab1:
    st.header("📖 ทฤษฎีและสมการคณิตศาสตร์")
    st.markdown("โจทย์กำหนดให้ประมาณค่าพื้นที่ใต้กราฟ $A$ ของฟังก์ชัน:")
    
    # REQUIREMENT 2: Mathematical Notation (st.latex)
    st.latex(r"A = \int_{a}^{b} \sqrt{1 + e^x} \, dx")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("1. Trapezoidal Rule")
        st.write("ประมาณค่าพื้นที่ด้วยรูปสี่เหลี่ยมคางหมูหลายรูปต่อกัน:")
        st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{2} \left[ f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]")
        st.latex(r"h = \frac{b - a}{n}")
        
    with col_t2:
        st.subheader("2. Simpson's Rule")
        st.write("ประมาณค่าพื้นที่ด้วยสมการพาราโบลา (ใช้ $n$ เป็นจำนวนคู่):")
        st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{3} \left[ f(x_0) + 4\sum_{i \text{ odd}} f(x_i) + 2\sum_{i \text{ even}} f(x_i) + f(x_n) \right]")
        st.latex(r"h = \frac{b - a}{n}")

# ------------------------------------------
# TAB 2: Dynamic Visualization (Plotly Chart)
# ------------------------------------------
with tab2:
    st.header("📊 กราฟปฏิสัมพันธ์ (Interactive Visualization)")
    
    # REQUIREMENT 4: Metrics Summary Card
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 ค่าจริง (Exact Value)", f"{exact_val:.6f}")
    m2.metric("📐 Trapezoidal Approx.", f"{trap_val:.6f}", f"Error: {abs(exact_val - trap_val):.2e}", delta_color="inverse")
    m3.metric("🔵 Simpson's Approx.", f"{simp_val:.6f}", f"Error: {abs(exact_val - simp_val):.2e}", delta_color="inverse")
    
    st.markdown("---")
    
    # REQUIREMENT 3: Data & Dynamic Visualization (st.plotly_chart)
    st.subheader(f"แสดงพื้นที่การประมาณค่าด้วยวิธี {method_choice} (n = {n})")
    
    x_dense = np.linspace(a - 0.2, b + 0.2, 300)
    y_dense = f(x_dense)
    
    fig = go.Figure()
    
    # เส้นฟังก์ชันจริง
    fig.add_trace(go.Scatter(
        x=x_dense, y=y_dense, 
        mode='lines', name='f(x) = √(1 + eⁿ)',
        line=dict(color='crimson', width=3)
    ))
    
    # แรเงาพื้นที่ตามวิธีที่เลือก
    x_curr = x_trap if method_choice == "Trapezoidal Rule" else x_simp
    y_curr = y_trap if method_choice == "Trapezoidal Rule" else y_simp
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_curr, x_curr[::-1]]),
        y=np.concatenate([y_curr, np.zeros_like(y_curr)]),
        fill='toself',
        fillcolor=chart_color,
        opacity=0.5,
        line=dict(color='royalblue'),
        name=f'พื้นที่ประมาณค่า ({method_choice})'
    ))
    
    # เพิ่มจุดพิกัด
    fig.add_trace(go.Scatter(
        x=x_curr, y=y_curr,
        mode='markers', name='Points (x_i, y_i)',
        marker=dict(size=6, color='black')
    ))
    
    fig.update_layout(
        title=f"การจำลองการอินทิเกรตช่วง [{a}, {b}] โดยแบ่ง n = {n}",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# TAB 3: Step-by-Step Calculation & Tables
# ------------------------------------------
with tab3:
    st.header("📝 การคำนวณทีละขั้นตอนและตารางสรุปผล")
    
    # REQUIREMENT 4: Step-by-Step Calculation
    with st.expander("🔍 คลิกเพื่อดูขั้นตอนการคำนวณแบบ Step-by-Step (ณ ค่าปัจจุบัน)", expanded=True):
        st.markdown(f"""
        - *ช่วงการอินทิเกรต:* $a = {a}$, $b = {b}$
        - *ขนาดความกว้างของช่วงย่อย ($h$):* $h = \\frac{{{b} - {a}}}{{{n}}} = {h_trap:.6f}$
        - *ผลรวมที่จุดปลาย:* $f(a) = {f(a):.6f}$, $f(b) = {f(b):.6f}$
        """)
        st.write("---")
        st.markdown("*สูตรสรุปผลการคำนวณ:*")
        st.latex(f"A_{{\\text{{Trapezoidal}}}} = {trap_val:.6f} \\quad (\\text{{Error}} = {abs(exact_val - trap_val):.6e})")
        st.latex(f"A_{{\\text{{Simpson}}}} = {simp_val:.6f} \\quad (\\text{{Error}} = {abs(exact_val - simp_val):.6e})")

    st.subheader("1. ตารางแสดงค่า Error ตามจำนวนช่วง n (n = 8, 16, 32, 64)")
    
    # REQUIREMENT 4: st.dataframe
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
        "Simpson's Error |A - A~|": [f"{e:.6e}" for e in simp_errs]
    })
    st.dataframe(df_n_error, use_container_width=True)

    st.subheader("2. ตารางเปรียบเทียบ Error เมื่อ n = 64")
    
    t_64, _, _, _ = trapezoidal_rule(a, b, 64)
    s_64, _, _, _ = simpsons_rule(a, b, 64)
    
    df_compare = pd.DataFrame({
        "Method": ["Trapezoidal", "Simpson"],
        "A (Exact)": [f"{exact_val:.6f}", f"{exact_val:.6f}"],
        "A~ (Approximated)": [f"{t_64:.6f}", f"{s_64:.6f}"],
        "Error = |A - A~|": [f"{abs(exact_val - t_64):.6e}", f"{abs(exact_val - s_64):.6e}"]
    })
    st.dataframe(df_compare, use_container_width=True)

    st.subheader("3. Output ตาม Format ที่โจทย์กำหนด")
    st.code(
f"""Method          A~1          Error A1
----------------------------------------
Trapezoidal     {t_64:<12.6f} {abs(exact_val - t_64):.5E}
Simpson         {s_64:<12.6f} {abs(exact_val - s_64):.5E}""", 
        language="text"
    )
