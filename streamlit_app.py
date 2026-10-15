import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Project 3: Numerical Integration", layout="wide")

# ----------------------------------------------------------------------
# ฟังก์ชันทางคณิตศาสตร์
# ----------------------------------------------------------------------
def f(x):
    return 1 + np.exp(x)


def exact_integral(a, b):
    """ค่าจริง A = (b - a) + e^b - e^a"""
    return (b - a) + np.exp(b) - np.exp(a)


def trapezoidal(a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 2 * (y[0] + 2 * y[1:-1].sum() + y[-1])


def simpson(a, b, n):
    if n % 2 != 0:
        raise ValueError("Simpson's rule ต้องใช้ n เป็นจำนวนคู่")
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum() + y[-1])


METHODS = {"Trapezoidal": trapezoidal, "Simpson": simpson}

# ----------------------------------------------------------------------
# Sidebar: รับค่าพารามิเตอร์ (Interactive Controls)
# ----------------------------------------------------------------------
st.sidebar.header("⚙️ พารามิเตอร์")
a = st.sidebar.number_input("ค่า a (ขอบล่าง)", value=0.0, step=0.5, min_value=-10.0, max_value=10.0)
b = st.sidebar.number_input("ค่า b (ขอบบน)", value=2.0, step=0.5, min_value=-10.0, max_value=10.0)
n = st.sidebar.slider("จำนวนช่วงย่อย n (เลขคู่)", min_value=2, max_value=200, value=8, step=2)
method_show = st.sidebar.selectbox("วิธีที่ต้องการแสดงบนกราฟ", ["Trapezoidal", "Simpson", "ทั้งสองวิธี"])

if b <= a:
    st.error("ต้องกำหนดให้ b > a")
    st.stop()

A = exact_integral(a, b)

# ----------------------------------------------------------------------
# หัวเรื่อง
# ----------------------------------------------------------------------
st.title("Project 3: Comparison of Numerical Integration Approximations")
st.latex(r"A = \int_{a}^{b} \left(1 + e^{x}\right) dx")

tab_theory, tab_graph, tab_error, tab_summary = st.tabs(
    ["📘 ทฤษฎี", "📈 กราฟพื้นที่", "📊 ตาราง Error", "✅ สรุปผล"]
)

# ----------------------------------------------------------------------
# Tab 1: ทฤษฎี
# ----------------------------------------------------------------------
with tab_theory:
    st.subheader("ค่าจริงของอินทิกรัล")
    st.latex(r"A = \int_{a}^{b} (1+e^{x})\,dx = \left[x + e^{x}\right]_a^b = (b-a) + e^{b} - e^{a}")

    st.subheader("1. Trapezoidal Rule")
    st.latex(r"h = \frac{b-a}{n}, \quad x_i = a + ih")
    st.latex(r"\tilde{A}_{T} = \frac{h}{2}\left[f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n)\right]")

    st.subheader("2. Simpson's Rule (n เป็นเลขคู่)")
    st.latex(
        r"\tilde{A}_{S} = \frac{h}{3}\left[f(x_0) + 4\sum_{i=1,3,5}^{n-1} f(x_i)"
        r" + 2\sum_{i=2,4,6}^{n-2} f(x_i) + f(x_n)\right]"
    )

    st.subheader("ค่าคลาดเคลื่อน (Error)")
    st.latex(r"\text{Error} = \left| A - \tilde{A} \right|")

# ----------------------------------------------------------------------
# Tab 2: กราฟพื้นที่ใต้กราฟ (อัปเดตตาม input อัตโนมัติ)
# ----------------------------------------------------------------------
with tab_graph:
    st.subheader(f"พื้นที่ใต้กราฟ f(x) = 1 + eˣ  ในช่วง [{a}, {b}]  (n = {n})")

    pad = (b - a) * 0.3
    x_full = np.linspace(a - pad, b + pad, 400)
    x_area = np.linspace(a, b, 400)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_full, y=f(x_full), mode="lines",
                             line=dict(color="red"), name="f(x) = 1 + eˣ"))
    fig.add_trace(go.Scatter(x=x_area, y=f(x_area), mode="lines", fill="tozeroy",
                             fillcolor="rgba(30,144,255,0.6)", line=dict(color="red"),
                             name="พื้นที่ A (ค่าจริง)"))

    xn = np.linspace(a, b, n + 1)
    if method_show in ("Trapezoidal", "ทั้งสองวิธี"):
        fig.add_trace(go.Scatter(x=xn, y=f(xn), mode="lines+markers",
                                 line=dict(color="orange", dash="dash"),
                                 name=f"Trapezoidal (n={n})"))
    if method_show in ("Simpson", "ทั้งสองวิธี"):
        # วาดพาราโบลาเป็นช่วง ๆ ของ Simpson (ทีละ 2 ช่วงย่อย)
        for k in range(0, n, 2):
            x0, x1, x2 = xn[k], xn[k + 1], xn[k + 2]
            xs = np.linspace(x0, x2, 30)
            ys = np.polyval(np.polyfit([x0, x1, x2], f(np.array([x0, x1, x2])), 2), xs)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines",
                                     line=dict(color="green", dash="dot"),
                                     name=f"Simpson (n={n})", showlegend=(k == 0)))

    fig.update_layout(xaxis_title="x", yaxis_title="f(x)", height=500)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# Tab 3: ตาราง Error ที่ n = 8, 16, 32, 64 และกราฟ n กับ error
# ----------------------------------------------------------------------
with tab_error:
    st.subheader("ตารางแสดงค่า Error ของแต่ละวิธี")
    n_list = [8, 16, 32, 64]
    rows = []
    for ni in n_list:
        at = trapezoidal(a, b, ni)
        as_ = simpson(a, b, ni)
        rows.append({
            "n": ni,
            "Ã Trapezoidal": at,
            "Error Trapezoidal = |A − Ã|": abs(A - at),
            "Ã Simpson": as_,
            "Error Simpson = |A − Ã|": abs(A - as_),
        })
    df_err = pd.DataFrame(rows)
    st.dataframe(
        df_err.style.format({
            "Ã Trapezoidal": "{:.6f}",
            "Error Trapezoidal = |A − Ã|": "{:.5E}",
            "Ã Simpson": "{:.6f}",
            "Error Simpson = |A − Ã|": "{:.5E}",
        }),
        use_container_width=True, hide_index=True,
    )

    st.subheader("กราฟ n เทียบกับ Error")
    log_scale = st.checkbox("แสดงแกน Error แบบ log", value=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_err["n"], y=df_err["Error Trapezoidal = |A − Ã|"],
                              mode="lines+markers", name="Trapezoidal"))
    fig2.add_trace(go.Scatter(x=df_err["n"], y=df_err["Error Simpson = |A − Ã|"],
                              mode="lines+markers", name="Simpson"))
    fig2.update_layout(xaxis_title="n", yaxis_title="Error = |A − Ã|", height=450,
                       yaxis_type="log" if log_scale else "linear",
                       xaxis=dict(tickvals=n_list))
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------------------------
# Tab 4: สรุปผล (n = 64) + Output format
# ----------------------------------------------------------------------
with tab_summary:
    N_FINAL = 64
    st.subheader(f"ตารางเปรียบเทียบ Error เมื่อ n = {N_FINAL}")

    summary_rows = []
    for name, func in METHODS.items():
        approx = func(a, b, N_FINAL)
        summary_rows.append({
            "Method": name,
            "A": A,
            "Ã": approx,
            "Error = |A − Ã|": abs(A - approx),
        })
    df_sum = pd.DataFrame(summary_rows)
    st.dataframe(
        df_sum.style.format({"A": "{:.6f}", "Ã": "{:.6f}", "Error = |A − Ã|": "{:.5E}"}),
        use_container_width=True, hide_index=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("ค่าจริง A", f"{A:.6f}")
    c2.metric("Error (Trapezoidal)", f"{df_sum.loc[0, 'Error = |A − Ã|']:.3E}")
    c3.metric("Error (Simpson)", f"{df_sum.loc[1, 'Error = |A − Ã|']:.3E}")

    better = df_sum.loc[df_sum["Error = |A − Ã|"].idxmin(), "Method"]
    st.success(f"ที่ n = {N_FINAL} วิธี **{better}** ให้ค่าคลาดเคลื่อนน้อยกว่า")

    st.subheader("Output ตามรูปแบบที่กำหนด")
    lines = [f"{'Method':<12}{'A~':>12}{'Error':>14}", "-" * 38]
    for _, r in df_sum.iterrows():
        lines.append(f"{r['Method']:<12}{r['Ã']:>12.6f}{r['Error = |A − Ã|']:>14.5E}")
    st.code("\n".join(lines), language="text")
