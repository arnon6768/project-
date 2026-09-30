import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Numerical Integration Lab",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #f8fbff 0%,
                #f4f7fb 50%,
                #eef4ff 100%
            );
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ================================
       SIDEBAR
    ================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 50%,
                #1e3a8a 100%
            );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stSlider label {
        font-weight: 600;
    }


    /* ================================
       HERO HEADER
    ================================= */

    .hero {
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #1e3a8a 55%,
                #2563eb 100%
            );

        padding: 38px 42px;
        border-radius: 24px;
        color: white;
        box-shadow:
            0 15px 35px rgba(15, 23, 42, 0.18);

        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -80px;
        top: -100px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
        right: 130px;
        bottom: -100px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 19px;
        opacity: 0.9;
        margin-bottom: 20px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 30px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.25);
        font-size: 14px;
        font-weight: 600;
    }


    /* ================================
       SECTION TITLES
    ================================= */

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 20px;
    }


    /* ================================
       CARDS
    ================================= */

    .info-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.06);
        height: 100%;
    }

    .info-card h3 {
        color: #0f172a;
        margin-bottom: 8px;
    }

    .info-card p {
        color: #64748b;
        line-height: 1.7;
    }


    /* ================================
       RESULT CARDS
    ================================= */

    .result-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.07);
        min-height: 145px;
    }

    .result-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
    }

    .result-method {
        font-size: 13px;
        margin-top: 6px;
        color: #2563eb;
        font-weight: 600;
    }


    /* ================================
       STEP CARDS
    ================================= */

    .step-card {
        background: white;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        padding: 25px;
        margin-bottom: 18px;
        box-shadow:
            0 7px 22px rgba(15, 23, 42, 0.05);
    }

    .step-number {
        display: inline-block;
        background: #2563eb;
        color: white;
        font-weight: 800;
        padding: 7px 13px;
        border-radius: 10px;
        margin-bottom: 10px;
    }


    /* ================================
       BADGES
    ================================= */

    .badge-blue {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
    }

    .badge-green {
        display: inline-block;
        background: #dcfce7;
        color: #15803d;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
    }


    /* ================================
       FOOTER
    ================================= */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding-top: 30px;
        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================

def f(x):
    return 1 + np.exp(x)


def exact_integral(a, b):
    return (b + np.exp(b)) - (a + np.exp(a))


def trapezoidal_rule(a, b, n):

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = f(x)

    return h * (
        (y[0] + y[-1]) / 2
        + np.sum(y[1:-1])
    )


def simpsons_rule(a, b, n):

    if n % 2 != 0:
        raise ValueError(
            "Simpson's Rule requires an even n."
        )

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = f(x)

    odd_sum = np.sum(y[1:-1:2])

    even_sum = np.sum(y[2:-1:2])

    return (
        h / 3
        * (
            y[0]
            + y[-1]
            + 4 * odd_sum
            + 2 * even_sum
        )
    )


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        📐 Numerical Integration Lab
    </div>

    <div class="hero-subtitle">
        Project #3 — Comparison of Numerical Integration Approximations
    </div>

    <span class="hero-badge">
        Trapezoidal Rule
    </span>

    <span class="hero-badge">
        Simpson's Rule
    </span>

    <span class="hero-badge">
        Numerical Methods
    </span>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 0 20px 0;
    ">
        <div style="font-size:42px;">📐</div>
        <div style="
            font-size:22px;
            font-weight:800;
        ">
            Project #3
        </div>
        <div style="
            opacity:0.75;
            font-size:13px;
        ">
            Numerical Integration
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### ⚙️ Input Parameters")

st.sidebar.markdown(
    "กำหนดค่าที่ใช้ในการประมาณอินทิกรัล"
)

# Widget 1
a = st.sidebar.number_input(
    "ค่า a — ขอบเขตล่าง",
    value=0.0,
    step=0.1,
    format="%.2f"
)

# Widget 2
b = st.sidebar.number_input(
    "ค่า b — ขอบเขตบน",
    value=1.0,
    step=0.1,
    format="%.2f"
)

# Widget 3
n = st.sidebar.selectbox(
    "จำนวนช่วง n",
    [8, 16, 32, 64],
    index=0
)

# Widget 4
graph_points = st.sidebar.slider(
    "ความละเอียดของกราฟ",
    100,
    1000,
    500,
    100
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="
        padding:15px;
        border-radius:14px;
        background:rgba(255,255,255,0.10);
    ">
        <b>Widgets ที่ใช้</b><br><br>
        ✓ number_input<br>
        ✓ selectbox<br>
        ✓ slider
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VALIDATION
# ============================================================

if b <= a:

    st.error(
        "❌ ค่า b ต้องมากกว่าค่า a"
    )

    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================

true_value = exact_integral(a, b)

trap_value = trapezoidal_rule(a, b, n)

simp_value = simpsons_rule(a, b, n)

trap_error = abs(
    true_value - trap_value
)

simp_error = abs(
    true_value - simp_value
)

h = (b - a) / n


# ============================================================
# QUICK SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📊 Calculation Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="section-description">
        ผลลัพธ์จากค่าที่กำหนด
        <b>a = {a:.2f}</b>,
        <b>b = {b:.2f}</b>,
        <b>n = {n}</b>
    </div>
    """,
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                EXACT VALUE
            </div>
            <div class="result-value">
                {true_value:.6f}
            </div>
            <div class="result-method">
                A
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                TRAPEZOIDAL
            </div>
            <div class="result-value">
                {trap_value:.6f}
            </div>
            <div class="result-method">
                Ãₜ
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                SIMPSON
            </div>
            <div class="result-value">
                {simp_value:.6f}
            </div>
            <div class="result-method">
                Ãₛ
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                STEP SIZE
            </div>
            <div class="result-value">
                {h:.5f}
            </div>
            <div class="result-method">
                h = (b-a)/n
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📚 Theory",
        "🧮 Step-by-Step",
        "📈 Visualization",
        "📉 Error Analysis",
        "🏆 n = 64"
    ]
)


# ============================================================
# TAB 1 — THEORY
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">📚 Mathematical Theory</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'หลักการและสูตรที่ใช้ในการประมาณค่า Numerical Integration'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="info-card">

        <span class="badge-blue">
        FUNCTION
        </span>

        <h3>ฟังก์ชันที่กำหนด</h3>

        </div>
        """, unsafe_allow_html=True)

        st.latex(
            r"""
            f(x)=1+e^x
            """
        )

    with col2:

        st.markdown("""
        <div class="info-card">

        <span class="badge-green">
        EXACT INTEGRAL
        </span>

        <h3>ค่าจริงของอินทิกรัล</h3>

        </div>
        """, unsafe_allow_html=True)

        st.latex(
            r"""
            A=\int_a^b(1+e^x)\,dx
            """
        )

        st.latex(
            r"""
            A=(b+e^b)-(a+e^a)
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">

    <span class="badge-blue">
    TRAPEZOIDAL RULE
    </span>

    <h3>Trapezoidal Rule</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        h=\frac{b-a}{n}
        """
    )

    st.latex(
        r"""
        \tilde A_T
        =
        h
        \left[
        \frac{f(a)+f(b)}{2}
        +
        \sum_{i=1}^{n-1}f(a+ih)
        \right]
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">

    <span class="badge-green">
    SIMPSON'S RULE
    </span>

    <h3>Simpson's Rule</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        \tilde A_S
        =
        \frac{h}{3}
        \left[
        f(a)+f(b)
        +
        4\sum_{\text{odd}}f(x_i)
        +
        2\sum_{\text{even}}f(x_i)
        \right]
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">

    <span class="badge-blue">
    ERROR
    </span>

    <h3>การหาค่าความคลาดเคลื่อน</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        Error=|A-\tilde A|
        """
    )


# ============================================================
# TAB 2 — STEP BY STEP
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">🧮 Step-by-Step Calculation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'แสดงขั้นตอนการคำนวณตั้งแต่การหาค่า h จนถึง Error'
        '</div>',
        unsafe_allow_html=True
    )

    # STEP 1
    st.markdown("""
    <div class="step-card">

    <span class="step-number">
    STEP 01
    </span>

    <h3>กำหนดค่า Step Size</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        rf"""
        h=\frac{{b-a}}{{n}}
        =
        \frac{{{b:.2f}-{a:.2f}}}{{{n}}}
        =
        {h:.10f}
        """
    )

    # STEP 2
    st.markdown("""
    <div class="step-card">

    <span class="step-number">
    STEP 02
    </span>

    <h3>หาค่า Exact Integral</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        A=(b+e^b)-(a+e^a)
        """
    )

    st.latex(
        rf"""
        A=({b:.2f}+e^{{{b:.2f}}})
        -
        ({a:.2f}+e^{{{a:.2f}}})
        """
    )

    st.latex(
        rf"""
        \boxed{{A={true_value:.10f}}}
        """
    )

    # STEP 3
    x_values = np.linspace(a, b, n + 1)
    y_values = f(x_values)

    interior_sum = np.sum(
        y_values[1:-1]
    )

    st.markdown("""
    <div class="step-card">

    <span class="step-number">
    STEP 03
    </span>

    <h3>Trapezoidal Rule</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        \tilde A_T
        =
        h
        \left[
        \frac{f(a)+f(b)}{2}
        +
        \sum_{i=1}^{n-1}f(x_i)
        \right]
        """
    )

    st.write(
        f"ผลรวมจุดภายใน = {interior_sum:.10f}"
    )

    st.latex(
        rf"""
        \tilde A_T
        =
        {h:.10f}
        \left[
        \frac{{{y_values[0]:.10f}+{y_values[-1]:.10f}}}{{2}}
        +
        {interior_sum:.10f}
        \right]
        """
    )

    st.latex(
        rf"""
        \boxed{{\tilde A_T={trap_value:.10f}}}
        """
    )

    st.latex(
        rf"""
        Error_T
        =
        |{true_value:.10f}-{trap_value:.10f}|
        =
        {trap_error:.5E}
        """
    )

    # STEP 4
    odd_sum = np.sum(
        y_values[1:-1:2]
    )

    even_sum = np.sum(
        y_values[2:-1:2]
    )

    st.markdown("""
    <div class="step-card">

    <span class="step-number">
    STEP 04
    </span>

    <h3>Simpson's Rule</h3>

    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"""
        \tilde A_S
        =
        \frac{h}{3}
        [
        f(a)+f(b)
        +4\sum_{\text{odd}}f(x_i)
        +2\sum_{\text{even}}f(x_i)
        ]
        """
    )

    st.write(
        f"ผลรวมตำแหน่งคี่ = {odd_sum:.10f}"
    )

    st.write(
        f"ผลรวมตำแหน่งคู่ = {even_sum:.10f}"
    )

    st.latex(
        rf"""
        \tilde A_S
        =
        \frac{{{h:.10f}}}{{3}}
        [
        {y_values[0]:.10f}
        +
        {y_values[-1]:.10f}
        +
        4({odd_sum:.10f})
        +
        2({even_sum:.10f})
        ]
        """
    )

    st.latex(
        rf"""
        \boxed{{\tilde A_S={simp_value:.10f}}}
        """
    )

    st.latex(
        rf"""
        Error_S
        =
        |{true_value:.10f}-{simp_value:.10f}|
        =
        {simp_error:.5E}
        """
    )


# ============================================================
# TAB 3 — VISUALIZATION
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">📈 Interactive Visualization</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'กราฟจะเปลี่ยนแปลงอัตโนมัติตามค่า a และ b ที่ผู้ใช้กำหนด'
        '</div>',
        unsafe_allow_html=True
    )

    x_plot = np.linspace(
        a,
        b,
        graph_points
    )

    y_plot = f(x_plot)

    fig = go.Figure()

    # Function
    fig.add_trace(
        go.Scatter(
            x=x_plot,
            y=y_plot,
            mode="lines",
            name="f(x) = 1 + eˣ",
            line=dict(
                width=4
            )
        )
    )

    # Area
    fig.add_trace(
        go.Scatter(
            x=np.concatenate(
                [x_plot, x_plot[::-1]]
            ),
            y=np.concatenate(
                [
                    y_plot,
                    np.zeros_like(y_plot)
                ]
            ),
            fill="toself",
            mode="none",
            name="Area"
        )
    )

    fig.add_vline(
        x=a,
        line_dash="dash",
        annotation_text=f"a = {a:.2f}"
    )

    fig.add_vline(
        x=b,
        line_dash="dash",
        annotation_text=f"b = {b:.2f}"
    )

    fig.update_layout(
        title={
            "text": "Area Under f(x) = 1 + eˣ",
            "font": {
                "size": 22
            }
        },
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        height=580,
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Lower Bound",
            f"{a:.2f}"
        )

    with c2:
        st.metric(
            "Upper Bound",
            f"{b:.2f}"
        )

    with c3:
        st.metric(
            "Exact Area",
            f"{true_value:.6f}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Additional Media / Illustration
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🖼️ Mathematical Illustration</div>',
        unsafe_allow_html=True
    )

    fig2, ax = plt.subplots(
        figsize=(11, 4.5)
    )

    x_img = np.linspace(
        a,
        b,
        400
    )

    y_img = f(x_img)

    ax.plot(
        x_img,
        y_img,
        linewidth=3,
        label="f(x) = 1 + e^x"
    )

    ax.fill_between(
        x_img,
        y_img,
        alpha=0.20
    )

    ax.axvline(
        a,
        linestyle="--",
        linewidth=1.5
    )

    ax.axvline(
        b,
        linestyle="--",
        linewidth=1.5
    )

    ax.set_title(
        "Numerical Integration Illustration",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "x",
        fontsize=12
    )

    ax.set_ylabel(
        "f(x)",
        fontsize=12
    )

    ax.grid(
        alpha=0.2
    )

    ax.legend()

    fig2.tight_layout()

    st.pyplot(
        fig2,
        use_container_width=True
    )

    plt.close(fig2)


# ============================================================
# TAB 4 — ERROR ANALYSIS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">📉 Error Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'เปรียบเทียบค่าความคลาดเคลื่อนของทั้งสองวิธี '
        'เมื่อ n = 8, 16, 32 และ 64'
        '</div>',
        unsafe_allow_html=True
    )

    n_values = [
        8,
        16,
        32,
        64
    ]

    rows = []

    for n_i in n_values:

        trap_i = trapezoidal_rule(
            a,
            b,
            n_i
        )

        simp_i = simpsons_rule(
            a,
            b,
            n_i
        )

        rows.append(
            {
                "n": n_i,
                "Trapezoidal Error":
                    abs(true_value - trap_i),
                "Simpson Error":
                    abs(true_value - simp_i)
            }
        )

    error_df = pd.DataFrame(rows)

    # TABLE
    st.markdown(
        "### 📋 Error Table"
    )

    st.dataframe(
        error_df.style.format(
            {
                "Trapezoidal Error":
                    "{:.5E}",
                "Simpson Error":
                    "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # ERROR GRAPH
    st.markdown(
        "### 📊 n vs Error"
    )

    error_fig = go.Figure()

    error_fig.add_trace(
        go.Scatter(
            x=error_df["n"],
            y=error_df["Trapezoidal Error"],
            mode="lines+markers",
            name="Trapezoidal",
            line=dict(
                width=3
            ),
            marker=dict(
                size=9
            )
        )
    )

    error_fig.add_trace(
        go.Scatter(
            x=error_df["n"],
            y=error_df["Simpson Error"],
            mode="lines+markers",
            name="Simpson",
            line=dict(
                width=3
            ),
            marker=dict(
                size=9
            )
        )
    )

    error_fig.update_layout(
        title="Error Comparison",
        xaxis_title="Number of intervals (n)",
        yaxis_title="Error",
        yaxis_type="log",
        template="plotly_white",
        height=520,
        hovermode="x unified"
    )

    st.plotly_chart(
        error_fig,
        use_container_width=True
    )

    st.info(
        "ใช้ Logarithmic Scale ที่แกน Error "
        "เพื่อให้สามารถมองเห็นความแตกต่างของ Error "
        "ระหว่าง Trapezoidal และ Simpson ได้ชัดเจน"
    )

    # FULL RESULT TABLE
    st.markdown(
        "### 📑 Numerical Results"
    )

    result_rows = []

    for n_i in n_values:

        trap_i = trapezoidal_rule(
            a,
            b,
            n_i
        )

        simp_i = simpsons_rule(
            a,
            b,
            n_i
        )

        result_rows.append(
            {
                "n": n_i,
                "A": true_value,
                "Trapezoidal":
                    trap_i,
                "Error (Trap.)":
                    abs(true_value - trap_i),
                "Simpson":
                    simp_i,
                "Error (Simp.)":
                    abs(true_value - simp_i)
            }
        )

    result_df = pd.DataFrame(
        result_rows
    )

    st.dataframe(
        result_df.style.format(
            {
                "A": "{:.6f}",
                "Trapezoidal": "{:.6f}",
                "Error (Trap.)": "{:.5E}",
                "Simpson": "{:.6f}",
                "Error (Simp.)": "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 5 — N = 64
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">🏆 Comparison when n = 64</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'เปรียบเทียบ Trapezoidal และ Simpson โดยกำหนด n = 64 '
        'ตามโจทย์ Project #3'
        '</div>',
        unsafe_allow_html=True
    )

    n64 = 64

    trap64 = trapezoidal_rule(
        a,
        b,
        n64
    )

    simp64 = simpsons_rule(
        a,
        b,
        n64
    )

    trap64_error = abs(
        true_value - trap64
    )

    simp64_error = abs(
        true_value - simp64
    )

    # RESULT CARDS

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Exact Value A",
            f"{true_value:.6f}"
        )

    with c2:

        st.metric(
            "Trapezoidal Error",
            f"{trap64_error:.5E}"
        )

    with c3:

        st.metric(
            "Simpson Error",
            f"{simp64_error:.5E}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLE

    comparison_df = pd.DataFrame(
        {
            "Method": [
                "Trapezoidal",
                "Simpson"
            ],
            "A": [
                true_value,
                true_value
            ],
            "A_tilde": [
                trap64,
                simp64
            ],
            "Error = |A - A_tilde|": [
                trap64_error,
                simp64_error
            ]
        }
    )

    st.markdown(
        "### 📋 Comparison Table"
    )

    st.dataframe(
        comparison_df.style.format(
            {
                "A": "{:.6f}",
                "A_tilde": "{:.6f}",
                "Error = |A - A_tilde|":
                    "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # EXACT ASSIGNMENT OUTPUT

    st.markdown(
        "### 💻 Output Format"
    )

    st.code(
        f"""
Method          A_tilde       Error A
-----------------------------------------
Trapezoidal     {trap64:.6f}    {trap64_error:.5E}
Simpson         {simp64:.6f}    {simp64_error:.5E}
""",
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <b>Project #3 — Numerical Integration</b><br>

        Trapezoidal Rule • Simpson's Rule • Error Analysis<br>

        Numerical Methods / Streamlit Application

    </div>
    """,
    unsafe_allow_html=True
)
