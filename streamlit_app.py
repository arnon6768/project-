from pathlib import Path

app_code = r'''
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Project #3 | Numerical Integration",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN / CSS
# ============================================================
st.markdown(
    """
    <style>
    /* ---------- Base ---------- */
    [data-testid="stAppViewContainer"] {
        background: #f5f7fb;
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,251,0.92);
    }

    .main .block-container {
        max-width: 1450px;
        padding: 1.25rem 2rem 3rem 2rem;
    }

    /* ---------- Sidebar: LIGHT so input text is always visible ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.25rem 1rem;
    }

    section[data-testid="stSidebar"] * {
        color: #172033 !important;
    }

    section[data-testid="stSidebar"] input {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
        background: #ffffff !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #172033 !important;
        border-color: #d7dce5 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #172033 !important;
    }

    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
        color: #2563eb !important;
    }

    .side-brand {
        padding: 18px 16px;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #1d4ed8);
        color: white !important;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(37,99,235,.16);
    }

    .side-brand * {
        color: white !important;
    }

    .side-brand .big {
        font-size: 28px;
        font-weight: 850;
        line-height: 1.1;
    }

    .side-brand .small {
        font-size: 12px;
        opacity: .82;
        margin-top: 6px;
    }

    .side-section {
        font-weight: 800;
        font-size: 15px;
        margin: 15px 0 8px;
    }

    .side-help {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 12px;
        font-size: 12px;
        line-height: 1.65;
        color: #475569 !important;
    }

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 26px;
        padding: 34px 38px;
        color: white;
        background:
            radial-gradient(circle at 90% 10%, rgba(255,255,255,.17), transparent 28%),
            radial-gradient(circle at 78% 90%, rgba(96,165,250,.24), transparent 25%),
            linear-gradient(135deg, #0f172a 0%, #172554 50%, #2563eb 100%);
        box-shadow: 0 18px 45px rgba(15,23,42,.16);
        margin-bottom: 22px;
    }

    .hero-kicker {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.2);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .7px;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 13px 0 6px;
        font-size: 40px;
        line-height: 1.08;
        letter-spacing: -.8px;
        color: white;
    }

    .hero p {
        margin: 0;
        max-width: 850px;
        font-size: 16px;
        line-height: 1.7;
        color: rgba(255,255,255,.84);
    }

    .hero-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 18px;
    }

    .hero-tag {
        padding: 7px 11px;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.16);
        font-size: 12px;
        font-weight: 700;
        color: white;
    }

    /* ---------- Section ---------- */
    .section-head {
        margin: 24px 0 12px;
    }

    .section-head .title {
        font-size: 25px;
        font-weight: 850;
        color: #111827;
    }

    .section-head .desc {
        color: #64748b;
        font-size: 14px;
        margin-top: 4px;
    }

    /* ---------- Metric cards ---------- */
    .metric-card {
        background: white;
        border: 1px solid #e7eaf0;
        border-radius: 18px;
        padding: 18px 19px;
        min-height: 128px;
        box-shadow: 0 8px 24px rgba(15,23,42,.055);
    }

    .metric-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        color: #64748b;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .4px;
    }

    .metric-icon {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: 10px;
        background: #eff6ff;
        color: #2563eb;
        font-size: 17px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 850;
        color: #111827;
        margin-top: 15px;
        white-space: nowrap;
    }

    .metric-sub {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 2px;
    }

    /* ---------- White content cards ---------- */
    .card {
        background: white;
        border: 1px solid #e7eaf0;
        border-radius: 18px;
        padding: 21px;
        box-shadow: 0 8px 24px rgba(15,23,42,.05);
        margin-bottom: 16px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 850;
        color: #111827;
        margin-bottom: 8px;
    }

    .card-desc {
        color: #64748b;
        font-size: 13px;
        line-height: 1.7;
    }

    .formula-label {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 8px;
        background: #eff6ff;
        color: #1d4ed8;
        font-size: 11px;
        font-weight: 850;
        margin-bottom: 8px;
        letter-spacing: .4px;
    }

    /* ---------- Step cards ---------- */
    .step {
        background: white;
        border: 1px solid #e7eaf0;
        border-radius: 18px;
        padding: 20px 22px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(15,23,42,.045);
    }

    .step-no {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 74px;
        padding: 6px 10px;
        border-radius: 999px;
        background: #111827;
        color: white;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: .5px;
    }

    .step-title {
        font-size: 18px;
        font-weight: 850;
        color: #111827;
        margin: 10px 0 3px;
    }

    .step-note {
        font-size: 13px;
        color: #64748b;
    }

    /* ---------- Status / callouts ---------- */
    .callout {
        border-radius: 16px;
        padding: 14px 16px;
        margin: 10px 0 16px;
        border: 1px solid #dbeafe;
        background: #eff6ff;
        color: #1e3a8a;
        font-size: 13px;
        line-height: 1.7;
    }

    .callout-success {
        border-color: #bbf7d0;
        background: #f0fdf4;
        color: #166534;
    }

    .callout-warning {
        border-color: #fde68a;
        background: #fffbeb;
        color: #92400e;
    }

    /* ---------- Table polish ---------- */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ---------- Footer ---------- */
    .footer {
        margin-top: 30px;
        padding: 18px;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
    }

    /* ---------- Hide default Streamlit menu/footer clutter ---------- */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MATH FUNCTIONS
# ============================================================
def f(x):
    return 1 + np.exp(x)


def exact_integral(a, b):
    return (b + np.exp(b)) - (a + np.exp(a))


def trapezoidal_rule(a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h * ((y[0] + y[-1]) / 2 + np.sum(y[1:-1]))


def simpsons_rule(a, b, n):
    if n % 2 != 0:
        raise ValueError("Simpson's Rule requires an even n.")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (h / 3) * (
        y[0]
        + y[-1]
        + 4 * np.sum(y[1:-1:2])
        + 2 * np.sum(y[2:-1:2])
    )


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown(
    """
    <div class="side-brand">
        <div class="big">∫ Project #3</div>
        <div class="small">Comparison of Numerical Integration Approximations</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="side-section">⚙️ Input Parameters</div>', unsafe_allow_html=True)

a = st.sidebar.number_input(
    "a — ขอบเขตล่าง",
    value=0.0,
    step=0.1,
    format="%.2f",
)

b = st.sidebar.number_input(
    "b — ขอบเขตบน",
    value=1.0,
    step=0.1,
    format="%.2f",
)

n = st.sidebar.selectbox(
    "n — จำนวนช่วง",
    options=[8, 16, 32, 64],
    index=0,
)

graph_points = st.sidebar.slider(
    "ความละเอียดกราฟ",
    min_value=200,
    max_value=1200,
    value=600,
    step=100,
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div class="side-help">
        <b>Interactive Controls</b><br>
        • number_input สำหรับ a และ b<br>
        • selectbox สำหรับ n<br>
        • slider สำหรับความละเอียดกราฟ<br><br>
        <b>หมายเหตุ:</b> Simpson's Rule ต้องใช้ n เป็นจำนวนคู่
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# VALIDATION
# ============================================================
if b <= a:
    st.error("ค่า b ต้องมากกว่าค่า a กรุณาแก้ไข Input ทางด้านซ้าย")
    st.stop()

# ============================================================
# CALCULATIONS
# ============================================================
A = exact_integral(a, b)
AT = trapezoidal_rule(a, b, n)
AS = simpsons_rule(a, b, n)

ET = abs(A - AT)
ES = abs(A - AS)

h = (b - a) / n

# ============================================================
# HERO
# ============================================================
st.markdown(
    """
    <div class="hero">
        <span class="hero-kicker">Numerical Methods • Streamlit Application</span>
        <h1>Numerical Integration Lab</h1>
        <p>
            Project #3 — Comparison of Numerical Integration Approximations
            using the Trapezoidal Rule and Simpson's Rule.
        </p>
        <div class="hero-tags">
            <span class="hero-tag">∫ Exact Integral</span>
            <span class="hero-tag">Trapezoidal Rule</span>
            <span class="hero-tag">Simpson's Rule</span>
            <span class="hero-tag">Error Analysis</span>
            <span class="hero-tag">Interactive Graph</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# PROBLEM SUMMARY
# ============================================================
st.markdown(
    """
    <div class="section-head">
        <div class="title">📌 Problem & Current Input</div>
        <div class="desc">ค่าทั้งหมดจะคำนวณและอัปเดตอัตโนมัติเมื่อเปลี่ยน Input</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="card">
        <span class="formula-label">FUNCTION</span>
        <div class="card-title">โจทย์ที่ใช้ในการคำนวณ</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.latex(r"A=\int_a^b(1+e^x)\,dx")

# ============================================================
# METRICS
# ============================================================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top"><span>EXACT VALUE</span><span class="metric-icon">A</span></div>
            <div class="metric-value">{A:.6f}</div>
            <div class="metric-sub">Analytical integral</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top"><span>TRAPEZOIDAL</span><span class="metric-icon">T</span></div>
            <div class="metric-value">{AT:.6f}</div>
            <div class="metric-sub">Ãₜ • Error {ET:.3E}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top"><span>SIMPSON</span><span class="metric-icon">S</span></div>
            <div class="metric-value">{AS:.6f}</div>
            <div class="metric-sub">Ãₛ • Error {ES:.3E}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top"><span>STEP SIZE</span><span class="metric-icon">h</span></div>
            <div class="metric-value">{h:.6f}</div>
            <div class="metric-sub">h = (b − a) / n</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TABS
# ============================================================
tab_theory, tab_steps, tab_graph, tab_error, tab64 = st.tabs(
    [
        "📚 Theory",
        "🧮 Step-by-Step",
        "📈 Visualization",
        "📉 Error Analysis",
        "🏆 n = 64",
    ]
)

# ============================================================
# TAB 1: THEORY
# ============================================================
with tab_theory:
    st.markdown(
        """
        <div class="section-head">
            <div class="title">📚 Mathematical Theory</div>
            <div class="desc">สูตรและหลักการที่ใช้ใน Project #3</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="card">
                <span class="formula-label">FUNCTION</span>
                <div class="card-title">ฟังก์ชัน</div>
                <div class="card-desc">ฟังก์ชันที่กำหนดในโจทย์</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"f(x)=1+e^x")

    with c2:
        st.markdown(
            """
            <div class="card">
                <span class="formula-label">EXACT VALUE</span>
                <div class="card-title">ค่าจริงของอินทิกรัล</div>
                <div class="card-desc">ใช้เป็นค่ามาตรฐานในการคำนวณ Error</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"A=\int_a^b(1+e^x)\,dx")
        st.latex(r"A=(b+e^b)-(a+e^a)")

    st.markdown(
        """
        <div class="card">
            <span class="formula-label">TRAPEZOIDAL RULE</span>
            <div class="card-title">Trapezoidal Rule</div>
            <div class="card-desc">แบ่งพื้นที่ใต้กราฟเป็นรูปสี่เหลี่ยมคางหมูจำนวน n ช่วง</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(r"h=\frac{b-a}{n}")
    st.latex(
        r"\tilde A_T=h\left[\frac{f(a)+f(b)}{2}+\sum_{i=1}^{n-1}f(a+ih)\right]"
    )

    st.markdown(
        """
        <div class="card">
            <span class="formula-label">SIMPSON'S RULE</span>
            <div class="card-title">Simpson's Rule</div>
            <div class="card-desc">ใช้พาราโบลาประมาณช่วงของฟังก์ชัน และต้องใช้ n เป็นจำนวนคู่</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(
        r"\tilde A_S=\frac{h}{3}\left[f(a)+f(b)+4\sum_{\mathrm{odd}}f(x_i)+2\sum_{\mathrm{even}}f(x_i)\right]"
    )

    st.markdown(
        """
        <div class="card">
            <span class="formula-label">ERROR</span>
            <div class="card-title">Absolute Error</div>
            <div class="card-desc">วัดความแตกต่างระหว่างค่าจริงกับค่าประมาณ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(r"Error=\left|A-\tilde A\right|")

# ============================================================
# TAB 2: STEP BY STEP
# ============================================================
with tab_steps:
    st.markdown(
        """
        <div class="section-head">
            <div class="title">🧮 Step-by-Step Calculation</div>
            <div class="desc">แสดงวิธีทำจาก Input ปัจจุบันแบบเป็นขั้นตอน</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="callout">
            <b>Current Input:</b>
            a = {a:.2f} &nbsp; | &nbsp; b = {b:.2f} &nbsp; | &nbsp; n = {n}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Step 1
    st.markdown(
        """
        <div class="step">
            <span class="step-no">STEP 01</span>
            <div class="step-title">หา Step Size (h)</div>
            <div class="step-note">แบ่งช่วง [a,b] ออกเป็น n ส่วนเท่า ๆ กัน</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(r"h=\frac{b-a}{n}")
    st.latex(rf"h=\frac{{{b:.2f}-{a:.2f}}}{{{n}}}={h:.10f}")

    # Step 2
    st.markdown(
        """
        <div class="step">
            <span class="step-no">STEP 02</span>
            <div class="step-title">หา Exact Integral</div>
            <div class="step-note">คำนวณค่าจริงเพื่อใช้เป็นค่ามาตรฐาน</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(r"A=(b+e^b)-(a+e^a)")
    st.latex(
        rf"A=({b:.2f}+e^{{{b:.2f}}})-({a:.2f}+e^{{{a:.2f}}})"
    )
    st.latex(rf"\boxed{{A={A:.10f}}}")

    # Step 3
    x = np.linspace(a, b, n + 1)
    y = f(x)
    interior_sum = np.sum(y[1:-1])

    st.markdown(
        """
        <div class="step">
            <span class="step-no">STEP 03</span>
            <div class="step-title">Trapezoidal Rule</div>
            <div class="step-note">ใช้ค่าที่จุดปลายและจุดภายในทุกจุด</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(
        r"\tilde A_T=h\left[\frac{f(a)+f(b)}{2}+\sum_{i=1}^{n-1}f(x_i)\right]"
    )
    st.write(f"ผลรวมค่าภายใน = {interior_sum:.10f}")
    st.latex(
        rf"\tilde A_T={h:.10f}\left[\frac{{{y[0]:.10f}+{y[-1]:.10f}}}{{2}}+{interior_sum:.10f}\right]"
    )
    st.latex(rf"\boxed{{\tilde A_T={AT:.10f}}}")
    st.latex(rf"Error_T=|A-\tilde A_T|={ET:.5E}")

    # Step 4
    odd_sum = np.sum(y[1:-1:2])
    even_sum = np.sum(y[2:-1:2])

    st.markdown(
        """
        <div class="step">
            <span class="step-no">STEP 04</span>
            <div class="step-title">Simpson's Rule</div>
            <div class="step-note">แยกผลรวมจุดคี่และจุดคู่ แล้วแทนในสูตร Simpson</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(
        r"\tilde A_S=\frac{h}{3}\left[f(a)+f(b)+4\sum_{\mathrm{odd}}f(x_i)+2\sum_{\mathrm{even}}f(x_i)\right]"
    )
    st.write(f"ผลรวมจุดคี่ = {odd_sum:.10f}")
    st.write(f"ผลรวมจุดคู่ = {even_sum:.10f}")
    st.latex(
        rf"\tilde A_S=\frac{{{h:.10f}}}{{3}}\left[{y[0]:.10f}+{y[-1]:.10f}+4({odd_sum:.10f})+2({even_sum:.10f})\right]"
    )
    st.latex(rf"\boxed{{\tilde A_S={AS:.10f}}}")
    st.latex(rf"Error_S=|A-\tilde A_S|={ES:.5E}")

# ============================================================
# TAB 3: VISUALIZATION
# ============================================================
with tab_graph:
    st.markdown(
        """
        <div class="section-head">
            <div class="title">📈 Interactive Visualization</div>
            <div class="desc">กราฟเปลี่ยนตาม a, b และความละเอียดที่เลือกจาก Sidebar</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    x_plot = np.linspace(a, b, graph_points)
    y_plot = f(x_plot)

    fig = go.Figure()

    # Area
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([x_plot, x_plot[::-1]]),
            y=np.concatenate([y_plot, np.zeros_like(y_plot)]),
            fill="toself",
            fillcolor="rgba(37,99,235,0.13)",
            line=dict(color="rgba(0,0,0,0)"),
            hoverinfo="skip",
            name="Area under curve",
        )
    )

    # Function
    fig.add_trace(
        go.Scatter(
            x=x_plot,
            y=y_plot,
            mode="lines",
            line=dict(color="#2563eb", width=4),
            name="f(x) = 1 + eˣ",
        )
    )

    # Numerical points
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                size=7,
                color="#111827",
                line=dict(color="white", width=1),
            ),
            name=f"n = {n} points",
        )
    )

    fig.add_vline(
        x=a,
        line_dash="dash",
        line_color="#16a34a",
        annotation_text=f"a = {a:.2f}",
        annotation_position="top left",
    )

    fig.add_vline(
        x=b,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text=f"b = {b:.2f}",
        annotation_position="top right",
    )

    fig.update_layout(
        title=dict(
            text="Area Under the Curve: f(x) = 1 + eˣ",
            font=dict(size=22, color="#111827"),
        ),
        xaxis=dict(
            title="x",
            gridcolor="#e5e7eb",
            zerolinecolor="#cbd5e1",
        ),
        yaxis=dict(
            title="f(x)",
            gridcolor="#e5e7eb",
            zerolinecolor="#cbd5e1",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=600,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        margin=dict(l=50, r=30, t=90, b=50),
    )

    st.plotly_chart(fig, use_container_width=True)

    g1, g2, g3 = st.columns(3)

    with g1:
        st.metric("Lower Bound (a)", f"{a:.2f}")

    with g2:
        st.metric("Upper Bound (b)", f"{b:.2f}")

    with g3:
        st.metric("Area A", f"{A:.6f}")

    st.markdown(
        """
        <div class="callout callout-success">
            <b>Graph elements:</b>
            เส้นฟังก์ชัน • พื้นที่ใต้กราฟ • จุดแบ่ง n ช่วง • ขอบเขต a และ b
            และข้อมูลแบบ Interactive เมื่อเลื่อนเมาส์บนกราฟ
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TAB 4: ERROR ANALYSIS
# ============================================================
with tab_error:
    st.markdown(
        """
        <div class="section-head">
            <div class="title">📉 Error Analysis</div>
            <div class="desc">เปรียบเทียบ Error สำหรับ n = 8, 16, 32 และ 64</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    n_values = [8, 16, 32, 64]
    rows = []

    for ni in n_values:
        ti = trapezoidal_rule(a, b, ni)
        si = simpsons_rule(a, b, ni)
        rows.append(
            {
                "n": ni,
                "A": A,
                "Trapezoidal": ti,
                "Error (Trapezoidal)": abs(A - ti),
                "Simpson": si,
                "Error (Simpson)": abs(A - si),
            }
        )

    result_df = pd.DataFrame(rows)

    st.markdown(
        """
        <div class="card">
            <div class="card-title">📋 Numerical Results</div>
            <div class="card-desc">ตารางผลลัพธ์และ Error ของทั้งสองวิธี</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        result_df.style.format(
            {
                "A": "{:.6f}",
                "Trapezoidal": "{:.6f}",
                "Error (Trapezoidal)": "{:.5E}",
                "Simpson": "{:.6f}",
                "Error (Simpson)": "{:.5E}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    # Error chart
    error_fig = go.Figure()

    error_fig.add_trace(
        go.Scatter(
            x=n_values,
            y=result_df["Error (Trapezoidal)"],
            mode="lines+markers",
            name="Trapezoidal Error",
            line=dict(color="#2563eb", width=3),
            marker=dict(size=9),
        )
    )

    error_fig.add_trace(
        go.Scatter(
            x=n_values,
            y=result_df["Error (Simpson)"],
            mode="lines+markers",
            name="Simpson Error",
            line=dict(color="#dc2626", width=3),
            marker=dict(size=9),
        )
    )

    error_fig.update_layout(
        title=dict(
            text="Comparison of Absolute Error",
            font=dict(size=21, color="#111827"),
        ),
        xaxis=dict(
            title="Number of intervals (n)",
            type="category",
            gridcolor="#e5e7eb",
        ),
        yaxis=dict(
            title="Absolute Error",
            type="log",
            gridcolor="#e5e7eb",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=540,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        margin=dict(l=50, r=30, t=90, b=50),
    )

    st.plotly_chart(error_fig, use_container_width=True)

    st.markdown(
        """
        <div class="callout">
            <b>Why log scale?</b><br>
            ใช้ logarithmic scale ที่แกน Error เพื่อให้มองเห็นความแตกต่างของ
            Error ที่มีขนาดต่างกันมากได้ชัดเจน
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TAB 5: N = 64
# ============================================================
with tab64:
    st.markdown(
        """
        <div class="section-head">
            <div class="title">🏆 Final Comparison — n = 64</div>
            <div class="desc">ตารางสรุปในรูปแบบเดียวกับ Output ที่ระบุในโจทย์</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    trap64 = trapezoidal_rule(a, b, 64)
    simp64 = simpsons_rule(a, b, 64)
    trap64_error = abs(A - trap64)
    simp64_error = abs(A - simp64)

    final_df = pd.DataFrame(
        {
            "Method": ["Trapezoidal", "Simpson"],
            "A": [A, A],
            "Ã": [trap64, simp64],
            "Error = |A − Ã|": [trap64_error, simp64_error],
        }
    )

    st.dataframe(
        final_df.style.format(
            {
                "A": "{:.6f}",
                "Ã": "{:.6f}",
                "Error = |A − Ã|": "{:.5E}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### 💻 Output Format")

    st.code(
        f"""Method          A_tilde       Error A
-----------------------------------------
Trapezoidal     {trap64:.6f}    {trap64_error:.5E}
Simpson         {simp64:.6f}    {simp64_error:.5E}""",
        language="text",
    )

    st.markdown(
        """
        <div class="callout callout-success">
            <b>Project output completed:</b>
            Exact value, approximation values and absolute errors
            are displayed for n = 64.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        <b>Project #3 — Comparison of Numerical Integration Approximations</b><br>
        Streamlit • Numerical Methods • Trapezoidal Rule • Simpson's Rule
    </div>
    """,
    unsafe_allow_html=True,
)
'''

requirements = """streamlit
numpy
pandas
plotly
"""

base = Path("/mnt/data")
app_path = base / "app.py"
req_path = base / "requirements.txt"

app_path.write_text(app_code, encoding="utf-8")
req_path.write_text(requirements, encoding="utf-8")

print(f"สร้างไฟล์เรียบร้อย:\n- {app_path}\n- {req_path}")
