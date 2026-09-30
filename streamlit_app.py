import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Project #3 - Numerical Integration",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📐 Project #3</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Comparison of Numerical Integration Approximations'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# MATHEMATICAL PROBLEM
# ============================================================

st.markdown(
    '<div class="section-title">📖 Problem Statement</div>',
    unsafe_allow_html=True
)

st.write(
    "จงประมาณค่าของอินทิกรัลต่อไปนี้ด้วยวิธี "
    "**Trapezoidal Rule** และ **Simpson's Rule**"
)

st.latex(
    r"""
    A=\int_a^b(1+e^x)\,dx
    """
)

st.write(
    "โดยกำหนดค่า a, b และ n จากส่วน Input ทางด้านซ้าย"
)

st.markdown("---")


# ============================================================
# SIDEBAR : INPUT
# ============================================================

st.sidebar.title("⚙️ Input Parameters")

st.sidebar.markdown(
    "กำหนดค่าพารามิเตอร์สำหรับการคำนวณ"
)

# Widget Type 1 : number_input
a = st.sidebar.number_input(
    "ค่า a",
    value=0.0,
    step=0.1,
    format="%.2f",
    help="ขอบเขตล่างของอินทิกรัล"
)

# Widget Type 1 : number_input
b = st.sidebar.number_input(
    "ค่า b",
    value=1.0,
    step=0.1,
    format="%.2f",
    help="ขอบเขตบนของอินทิกรัล"
)

# Widget Type 2 : selectbox
n = st.sidebar.selectbox(
    "จำนวนช่วง n",
    options=[8, 16, 32, 64],
    index=0,
    help="จำนวนช่วงที่ใช้ในการประมาณค่า"
)

# Widget Type 3 : slider
graph_points = st.sidebar.slider(
    "ความละเอียดของกราฟ",
    min_value=100,
    max_value=1000,
    value=500,
    step=100,
    help="จำนวนจุดที่ใช้วาดกราฟ"
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Widgets ที่ใช้ใน Project**

    1. number_input
    2. selectbox
    3. slider
    """
)


# ============================================================
# INPUT VALIDATION
# ============================================================

if b <= a:

    st.error(
        "❌ ค่า b ต้องมากกว่าค่า a "
        "กรุณากลับไปแก้ไข Input ทางด้านซ้าย"
    )

    st.stop()


# ============================================================
# FUNCTION
# ============================================================

def f(x):
    """
    Function:
        f(x) = 1 + e^x
    """
    return 1 + np.exp(x)


# ============================================================
# EXACT INTEGRAL
# ============================================================

def exact_integral(a, b):
    """
    ∫(1+e^x)dx = x + e^x
    """

    return (b + np.exp(b)) - (a + np.exp(a))


# ============================================================
# TRAPEZOIDAL RULE
# ============================================================

def trapezoidal_rule(a, b, n):

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = f(x)

    result = h * (
        (y[0] + y[-1]) / 2
        + np.sum(y[1:-1])
    )

    return result


# ============================================================
# SIMPSON'S RULE
# ============================================================

def simpsons_rule(a, b, n):

    if n % 2 != 0:
        raise ValueError(
            "Simpson's Rule requires n to be even."
        )

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = f(x)

    odd_sum = np.sum(y[1:-1:2])

    even_sum = np.sum(y[2:-1:2])

    result = (
        h / 3
        * (
            y[0]
            + y[-1]
            + 4 * odd_sum
            + 2 * even_sum
        )
    )

    return result


# ============================================================
# MAIN CALCULATIONS
# ============================================================

true_value = exact_integral(a, b)

trap_value = trapezoidal_rule(a, b, n)

simp_value = simpsons_rule(a, b, n)

trap_error = abs(true_value - trap_value)

simp_error = abs(true_value - simp_value)

h = (b - a) / n


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📖 Theory",
        "🧮 Step-by-Step",
        "📊 Graph",
        "📋 Error Analysis",
        "🏆 n = 64 Comparison"
    ]
)


# ============================================================
# TAB 1 : THEORY
# ============================================================

with tab1:

    st.header("📖 Mathematical Theory")

    # --------------------------------------------------------
    # Function
    # --------------------------------------------------------

    st.subheader("1. Function")

    st.latex(
        r"""
        f(x)=1+e^x
        """
    )

    # --------------------------------------------------------
    # Exact Integral
    # --------------------------------------------------------

    st.subheader("2. Exact Integral")

    st.latex(
        r"""
        A=\int_a^b(1+e^x)\,dx
        """
    )

    st.latex(
        r"""
        A=[x+e^x]_a^b
        """
    )

    st.latex(
        r"""
        A=(b+e^b)-(a+e^a)
        """
    )

    st.info(
        f"ค่าจริงของอินทิกรัลสำหรับ Input ปัจจุบันคือ "
        f"A = {true_value:.6f}"
    )

    # --------------------------------------------------------
    # Trapezoidal
    # --------------------------------------------------------

    st.subheader("3. Trapezoidal Rule")

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

    # --------------------------------------------------------
    # Simpson
    # --------------------------------------------------------

    st.subheader("4. Simpson's Rule")

    st.latex(
        r"""
        h=\frac{b-a}{n}
        """
    )

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

    # --------------------------------------------------------
    # Error
    # --------------------------------------------------------

    st.subheader("5. Error")

    st.latex(
        r"""
        Error=|A-\tilde A|
        """
    )

    st.markdown("---")

    st.success(
        "สูตรทั้งหมดในส่วนนี้แสดงด้วย st.latex() "
        "ตาม Technical Requirements"
    )


# ============================================================
# TAB 2 : STEP-BY-STEP
# ============================================================

with tab2:

    st.header("🧮 Step-by-Step Calculation")

    st.write(
        f"กำหนดค่าปัจจุบัน: "
        f"a = {a:.2f}, b = {b:.2f}, n = {n}"
    )

    # --------------------------------------------------------
    # Step 1
    # --------------------------------------------------------

    st.subheader("Step 1 — Calculate h")

    st.latex(
        rf"""
        h=\frac{{b-a}}{{n}}
        =
        \frac{{{b:.2f}-{a:.2f}}}{{{n}}}
        =
        {h:.10f}
        """
    )

    # --------------------------------------------------------
    # Step 2
    # --------------------------------------------------------

    st.subheader("Step 2 — Calculate Exact Value")

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
        A={true_value:.10f}
        """
    )

    # --------------------------------------------------------
    # Step 3 : Trapezoidal
    # --------------------------------------------------------

    st.subheader("Step 3 — Trapezoidal Rule")

    x_values = np.linspace(a, b, n + 1)
    y_values = f(x_values)

    interior_sum = np.sum(y_values[1:-1])

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
        f"ผลรวมค่าภายในช่วง = {interior_sum:.10f}"
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
        \tilde A_T={trap_value:.10f}
        """
    )

    st.latex(
        rf"""
        Error_T
        =
        |A-\tilde A_T|
        =
        |{true_value:.10f}-{trap_value:.10f}|
        =
        {trap_error:.5E}
        """
    )

    # --------------------------------------------------------
    # Step 4 : Simpson
    # --------------------------------------------------------

    st.subheader("Step 4 — Simpson's Rule")

    odd_sum = np.sum(y_values[1:-1:2])

    even_sum = np.sum(y_values[2:-1:2])

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
        \tilde A_S={simp_value:.10f}
        """
    )

    st.latex(
        rf"""
        Error_S
        =
        |A-\tilde A_S|
        =
        |{true_value:.10f}-{simp_value:.10f}|
        =
        {simp_error:.5E}
        """
    )

    # --------------------------------------------------------
    # Calculation Table
    # --------------------------------------------------------

    st.subheader("📊 Current Calculation Summary")

    current_summary = pd.DataFrame(
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
                trap_value,
                simp_value
            ],
            "Error": [
                trap_error,
                simp_error
            ]
        }
    )

    st.dataframe(
        current_summary.style.format(
            {
                "A": "{:.6f}",
                "A_tilde": "{:.6f}",
                "Error": "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 : GRAPH
# ============================================================

with tab3:

    st.header("📊 Function and Area Graph")

    st.write(
        "กราฟแสดงฟังก์ชัน "
        r"$f(x)=1+e^x$ "
        "และพื้นที่ใต้กราฟในช่วงที่ผู้ใช้กำหนด"
    )

    # --------------------------------------------------------
    # Dynamic Plotly Graph
    # --------------------------------------------------------

    x_plot = np.linspace(
        a,
        b,
        graph_points
    )

    y_plot = f(x_plot)

    fig = go.Figure()

    # Function line
    fig.add_trace(
        go.Scatter(
            x=x_plot,
            y=y_plot,
            mode="lines",
            name="f(x) = 1 + eˣ",
            line=dict(width=3)
        )
    )

    # Area
    fig.add_trace(
        go.Scatter(
            x=np.concatenate(
                [
                    x_plot,
                    x_plot[::-1]
                ]
            ),
            y=np.concatenate(
                [
                    y_plot,
                    np.zeros_like(y_plot)
                ]
            ),
            fill="toself",
            fillcolor="rgba(100, 149, 237, 0.25)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Area"
        )
    )

    # Vertical line at a
    fig.add_vline(
        x=a,
        line_dash="dash",
        annotation_text=f"a = {a:.2f}"
    )

    # Vertical line at b
    fig.add_vline(
        x=b,
        line_dash="dash",
        annotation_text=f"b = {b:.2f}"
    )

    fig.update_layout(
        title="f(x) = 1 + eˣ",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        height=550,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        f"พื้นที่จริงใต้กราฟในช่วง "
        f"[{a:.2f}, {b:.2f}] = {true_value:.6f}"
    )

    # --------------------------------------------------------
    # Image / Media Requirement
    # --------------------------------------------------------

    st.subheader("🖼️ Mathematical Illustration")

    # Create an image automatically
    # This satisfies the media/image component.

    fig_img, ax_img = plt.subplots(
        figsize=(9, 4)
    )

    x_img = np.linspace(
        a,
        b,
        300
    )

    y_img = f(x_img)

    ax_img.plot(
        x_img,
        y_img,
        linewidth=2.5,
        label="f(x) = 1 + e^x"
    )

    ax_img.fill_between(
        x_img,
        y_img,
        alpha=0.20
    )

    ax_img.axvline(
        a,
        linestyle="--",
        linewidth=1.5
    )

    ax_img.axvline(
        b,
        linestyle="--",
        linewidth=1.5
    )

    ax_img.set_title(
        "Area Under f(x) = 1 + e^x"
    )

    ax_img.set_xlabel("x")

    ax_img.set_ylabel("f(x)")

    ax_img.legend()

    ax_img.grid(
        alpha=0.25
    )

    fig_img.tight_layout()

    st.pyplot(
        fig_img,
        use_container_width=True
    )

    plt.close(fig_img)


# ============================================================
# TAB 4 : ERROR ANALYSIS
# ============================================================

with tab4:

    st.header("📋 Error Analysis")

    st.write(
        "เปรียบเทียบ Error เมื่อ "
        "n = 8, 16, 32 และ 64"
    )

    n_values = [
        8,
        16,
        32,
        64
    ]

    error_rows = []

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

        trap_error_i = abs(
            true_value - trap_i
        )

        simp_error_i = abs(
            true_value - simp_i
        )

        error_rows.append(
            {
                "n": n_i,
                "Trapezoidal Error": trap_error_i,
                "Simpson Error": simp_error_i
            }
        )

    error_df = pd.DataFrame(
        error_rows
    )

    # --------------------------------------------------------
    # Error Table
    # --------------------------------------------------------

    st.subheader("1. Error Table")

    st.dataframe(
        error_df.style.format(
            {
                "Trapezoidal Error": "{:.5E}",
                "Simpson Error": "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Error Graph
    # --------------------------------------------------------

    st.subheader(
        "2. Graph of n vs Error"
    )

    error_fig = go.Figure()

    error_fig.add_trace(
        go.Scatter(
            x=error_df["n"],
            y=error_df["Trapezoidal Error"],
            mode="lines+markers",
            name="Trapezoidal Error"
        )
    )

    error_fig.add_trace(
        go.Scatter(
            x=error_df["n"],
            y=error_df["Simpson Error"],
            mode="lines+markers",
            name="Simpson Error"
        )
    )

    error_fig.update_layout(
        title="Comparison of Error",
        xaxis_title="n",
        yaxis_title="Error",
        yaxis_type="log",
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        error_fig,
        use_container_width=True
    )

    st.info(
        "แกน Error ใช้ logarithmic scale "
        "เพื่อให้สามารถเห็นความแตกต่างของ Error "
        "ระหว่างทั้งสองวิธีได้ชัดเจน"
    )

    # --------------------------------------------------------
    # Data Table for all n
    # --------------------------------------------------------

    st.subheader(
        "3. Numerical Results for Each n"
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
                "Trapezoidal": trap_i,
                "Trapezoidal Error":
                    abs(true_value - trap_i),
                "Simpson": simp_i,
                "Simpson Error":
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
                "Trapezoidal Error": "{:.5E}",
                "Simpson": "{:.6f}",
                "Simpson Error": "{:.5E}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 5 : N = 64 COMPARISON
# ============================================================

with tab5:

    st.header(
        "🏆 Comparison when n = 64"
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

    # --------------------------------------------------------
    # Comparison Table
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Output Format Exactly Like Assignment
    # --------------------------------------------------------

    st.subheader(
        "📄 Output Format"
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

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Exact Value A",
            f"{true_value:.6f}"
        )

    with col2:

        st.metric(
            "Trapezoidal Error",
            f"{trap64_error:.5E}"
        )

    with col3:

        st.metric(
            "Simpson Error",
            f"{simp64_error:.5E}"
        )

    st.markdown("---")

    st.success(
        "ตารางนี้เป็นการเปรียบเทียบโดยกำหนด n = 64 "
        "ตามโจทย์ Project #3"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Project #3 | Comparison of Numerical Integration Approximations"
)

st.caption(
    "Numerical Methods: Trapezoidal Rule & Simpson's Rule"
)
