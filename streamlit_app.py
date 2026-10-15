import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Numerical Integration Approximations",
    layout="wide"
)

# ==========================================
# Helper Functions for Mathematical Calculations
# ==========================================
def f(x):
    """ฟังก์ชัน f(x) = sqrt(1 + e^x)"""
    return np.sqrt(1 + np.exp(x))

def trapezoidal_rule(a, b, n):
    """การคำนวณการอินทิเกรตด้วยวิธี Trapezoidal Rule"""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integration, x, y

def simpsons_rule(a, b, n):
    """การคำนวณการอินทิเกรตด้วยวิธี Simpson's Rule (n ต้องเป็นจำนวนคู่)"""
    if n % 2 != 0:
        n += 1  # ปรับให้ n เป็นจำนวนคู่เสมอสำหรับ Simpson's rule
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    integration = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])
    return integration, x, y

# คำนวณค่าจริง (Exact Value) โดยใช้ Quadrature เพื่อใช้หาค่า Error
from scipy.integrate import quad
exact_val, _ = quad(f, 0, 1) # ค่าอ้างอิงเบื้องต้น

# ==========================================
# Technical Requirement 5: Layout Organization (Sidebar)
# ==========================================
st.sidebar.header("⚙️ ตั้งค่าพารามิเตอร์ (Input Parameters)")

# Technical Requirement 1: Interactive Controls (3 ชนิดขึ้นไป)
# Widget 1: st.number_input สำหรับ ขอบเขตล่าง a
a = st.sidebar.number_input("ขอบเขตล่าง (a):", value=0.0, step=0.1)

# Widget 2: st.number_input สำหรับ ขอบเขตบน b
b = st.sidebar.number_input("ขอบเขตบน (b):", value=1.0, step=0.1)

# Widget 3: st.select_slider/st.slider สำหรับ จำนวนช่วง n
n = st.sidebar.select_slider("จำนวนช่วง (n):", options=[8, 16, 32, 64], value=64)

# Widget 4: st.selectbox สำหรับ เลือกวิธีแสดงผลกราฟ
method_choice = st.sidebar.selectbox("เลือกวิธีคำนวณสำหรับวาดพื้นที่:", ["Trapezoidal Rule", "Simpson's Rule"])

# คำนวณค่าจริงตามช่วง a ถึง b ที่ผู้ใช้ป้อน
exact_value, _ = quad(f, a, b)

# ==========================================
# Main Content with Tabs
# ==========================================
st.title("Project 3: Comparison of Numerical Integration Approximations")

# Technical Requirement 5: st.tabs
tab1, tab2, tab3 = st.tabs(["📚 ทฤษฎี (Theory)", "📊 ตัวจำลอง (Simulation & Visualization)", "📝 สรุปผล (Summary & Analysis)"])

# ------------------------------------------
# TAB 1: ทฤษฎี (Theory)
# ------------------------------------------
with tab1:
    st.header("ทฤษฎีการประมาณค่าการอินทิเกรตทางตัวเลข")
    
    st.write("โจทย์กำหนดให้ประมาณค่า:")
    # Technical Requirement 2: Mathematical Notation (st.latex)
    st.latex(r"A = \int_{a}^{b} \sqrt{1 + e^x} \, dx")
    
    st.subheader("1. Trapezoidal Rule")
    st.write("ประมาณค่าพื้นที่ใต้กราฟด้วยรูปสี่เหลี่ยมคางหมู:")
    st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{2} \left[ f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]")
    
    st.subheader("2. Simpson's Rule")
    st.write("ประมาณค่าพื้นที่ใต้กราฟด้วยสมการพาราโบลา (ต้องใช้ n เป็นจำนวนคู่):")
    st.latex(r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{3} \left[ f(x_0) + 4\sum_{i=1,3,5...}^{n-1} f(x_i) + 2\sum_{i=2,4,6...}^{n-2} f(x_i) + f(x_n) \right]")
    
    st.write("โดยที่ $h = \\frac{b - a}{n}$")

# ------------------------------------------
# TAB 2: ตัวจำลอง (Simulation & Visualization)
# ------------------------------------------
with tab2:
    st.header("ตัวจำลองการประมาณค่าและกราฟแสดงพื้นที่")
    
    # คำนวณค่าผลลัพธ์
    trap_val, x_trap, y_trap = trapezoidal_rule(a, b, n)
    simp_val, x_simp, y_simp = simpsons_rule(a, b, n)
    
    # Technical Requirement 4: Step-by-step / Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("ค่าจริง (Exact Value)", f"{exact_value:.6f}")
    col2.metric("Trapezoidal Value", f"{trap_val:.6f}", delta=f"Error: {abs(exact_value - trap_val):.2e}", delta_color="inverse")
    col3.metric("Simpson's Value", f"{simp_val:.6f}", delta=f"Error: {abs(exact_value - simp_val):.2e}", delta_color="inverse")
    
    st.markdown("---")
    
    # Technical Requirement 3: Data & Dynamic Visualization (st.pyplot)
    st.subheader(f"กราฟแสดงพื้นที่ใต้โค้งด้วยวิธี {method_choice} (n = {n})")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # กราฟเส้นฟังก์ชันจริง
    x_dense = np.linspace(a - 0.5, b + 0.5, 200)
    y_dense = f(x_dense)
    ax.plot(x_dense, y_dense, 'r-', label=r'$f(x) = \sqrt{1 + e^x}$', linewidth=1.5)
    
    # แสดงแรเงาพื้นที่ใต้กราฟ
    if method_choice == "Trapezoidal Rule":
        x_plot, y_plot = x_trap, y_trap
        ax.fill_between(x_plot, 0, y_plot, color='dodgerblue', alpha=0.8, label='Trapezoidal Area')
    else:
        x_plot, y_plot = x_simp, y_simp
        ax.fill_between(x_plot, 0, y_plot, color='dodgerblue', alpha=0.8, label="Simpson's Area")
        
    ax.set_title(f"Numerical Integration Area (a={a}, b={b}, n={n})")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)

# ------------------------------------------
# TAB 3: สรุปผล (Summary & Analysis)
# ------------------------------------------
with tab3:
    st.header("ตารางวิเคราะห์และเปรียบเทียบค่าความคลาดเคลื่อน (Error Analysis)")
    
    # 1. ตารางแสดงค่า Error ของแต่ละวิธี ณ n ต่างๆ (8, 16, 32, 64)
    st.subheader("1. ตารางแสดงค่า Error ตามจำนวนช่วง n")
    n_list = [8, 16, 32, 64]
    
    trap_errors = []
    simp_errors = []
    
    for n_val in n_list:
        t_val, _, _ = trapezoidal_rule(a, b, n_val)
        s_val, _, _ = simpsons_rule(a, b, n_val)
        
        trap_errors.append(abs(exact_value - t_val))
        simp_errors.append(abs(exact_value - s_val))
        
    df_error_n = pd.DataFrame({
        "n": n_list,
        "Trapezoidal Error |A - A~|": [f"{e:.6e}" for e in trap_errors],
        "Simpson's Error |A - A~|": [f"{e:.6e}" for e in simp_errors]
    })
    
    # Technical Requirement 4: st.dataframe
    st.dataframe(df_error_n, use_container_width=True)
    
    # 2. ตารางเปรียบเทียบ Error เมื่อ n = 64
    st.subheader("2. ตารางเปรียบเทียบค่าประมาณการและ Error เมื่อ n = 64")
    
    t_val_64, _, _ = trapezoidal_rule(a, b, 64)
    s_val_64, _, _ = simpsons_rule(a, b, 64)
    
    df_compare_64 = pd.DataFrame({
        "Method": ["Trapezoidal", "Simpson"],
        "A (Exact)": [f"{exact_value:.6f}", f"{exact_value:.6f}"],
        "A~ (Approximated)": [f"{t_val_64:.6f}", f"{s_val_64:.6f}"],
        "Error = |A - A~|": [f"{abs(exact_value - t_val_64):.6e}", f"{abs(exact_value - s_val_64):.6e}"]
    })
    
    st.dataframe(df_compare_64, use_container_width=True)
    
    # 3. Output รูปแบบข้อความตาม Format ที่โจทย์กำหนด
    st.subheader("3. แสดง Output ตาม Format ที่โจทย์ระบุ")
    
    st.text(f"{'Method':<15} {'A~1':<12} {'Error A1'}")
    st.text("-" * 40)
    st.text(f"{'Trapezoidal':<15} {t_val_64:<12.6f} {abs(exact_value - t_val_64):.5E}")
    st.text(f"{'Simpson':<15} {s_val_64:<12.6f} {abs(exact_value - s_val_64):.5E}")
