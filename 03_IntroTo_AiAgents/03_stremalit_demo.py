"""
🚀 STREAMLIT MASTERCLASS
Run:  pip install streamlit pandas numpy
      streamlit run streamlit_masterclass.py

Every lesson is a real function. The app shows its LIVE OUTPUT and its own SOURCE CODE
side by side, so you learn by reading and interacting at the same time.
"""
import inspect
import textwrap
import time

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Streamlit Masterclass", page_icon="🚀", layout="wide")

# ───────────────────────── Lesson registry ─────────────────────────
LESSONS = {}


def lesson(section, title):
    """Decorator: registers a function as a lesson under a sidebar section."""
    def deco(fn):
        LESSONS.setdefault(section, []).append((title, fn))
        return fn
    return deco


def render(title, fn):
    st.subheader(title)
    out, code = st.tabs(["▶ Live output", "</> Code"])
    with out:
        fn()
    with code:
        body = inspect.getsource(fn).split("\n")[2:]  # drop decorator + def line
        st.code(textwrap.dedent("\n".join(body)), language="python")
    st.divider()


# ═════════════════════ 1. TEXT & DISPLAY ═════════════════════
@lesson("1 · Text & Display", "Text elements")
def _():
    st.title("Title")
    st.header("Header")
    st.subheader("Subheader")
    st.markdown("**Bold**, *italic*, `code`, :red[colored], :blue-background[highlight] and emoji :sparkles:")
    st.caption("Small grey caption text")
    st.latex(r"E = mc^2")
    st.code("print('hello')", language="python")
    st.write("`st.write` is the Swiss-army knife: strings, numbers, dataframes, dicts...", {"a": 1})


@lesson("1 · Text & Display", "Metrics, status boxes, toasts")
def _():
    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", "$12.4k", "+8%")
    c2.metric("Churn", "2.1%", "-0.4%", delta_color="inverse")
    c3.metric("Users", "1,204", "+32")
    st.success("Success message")
    st.info("Info message")
    st.warning("Warning message")
    st.error("Error message")
    if st.button("Show toast", key="toast"):
        st.toast("Saved!", icon="✅")


# ═════════════════════ 2. WIDGETS ═════════════════════
@lesson("2 · Input Widgets", "Basic inputs (each returns its value)")
def _():
    name = st.text_input("Name", "Ada", key="w_name")
    bio = st.text_area("Bio", key="w_bio", height=70)
    age = st.number_input("Age", 0, 120, 25, key="w_age")
    score = st.slider("Score", 0, 100, (20, 80), key="w_score")  # tuple = range slider
    st.write(f"Hello **{name}**, age {age}, score range {score}")


@lesson("2 · Input Widgets", "Choice widgets")
def _():
    city = st.selectbox("City", ["Delhi", "Mumbai", "Varanasi"], key="w_city")
    skills = st.multiselect("Skills", ["Python", "SQL", "ML", "Viz"], default=["Python"], key="w_sk")
    level = st.radio("Level", ["Beginner", "Pro"], horizontal=True, key="w_lvl")
    agree = st.checkbox("I agree", key="w_agree")
    dark = st.toggle("Dark mode", key="w_dark")
    size = st.select_slider("Size", ["S", "M", "L", "XL"], value="M", key="w_size")
    pills = st.pills("Tags", ["A", "B", "C"], selection_mode="multi", key="w_pills")
    st.json({"city": city, "skills": skills, "level": level, "agree": agree,
             "dark": dark, "size": size, "tags": pills})


@lesson("2 · Input Widgets", "Date, color, files, camera-style inputs")
def _():
    d = st.date_input("Date", key="w_date")
    col = st.color_picker("Color", "#7C3AED", key="w_col")
    f = st.file_uploader("Upload a CSV", type="csv", key="w_file")
    if f:
        st.dataframe(pd.read_csv(f).head())
    st.write(d, col)
    st.download_button("Download sample", "a,b\n1,2", "sample.csv", key="w_dl")


# ═════════════════════ 3. LAYOUT ═════════════════════
@lesson("3 · Layout", "Columns, tabs, expander, container")
def _():
    left, right = st.columns([2, 1], gap="large")  # width ratio 2:1
    left.write("Wide column")
    right.write("Narrow column")

    t1, t2 = st.tabs(["📈 Tab one", "📋 Tab two"])
    with t1:
        st.write("Inside tab one")
    with t2:
        st.write("Inside tab two")

    with st.expander("Click to expand"):
        st.write("Hidden content")

    with st.container(border=True):
        st.write("A bordered container groups elements")

    with st.popover("Popover"):
        st.write("Floating panel")


@lesson("3 · Layout", "Sidebar & placeholders (st.empty)")
def _():
    st.sidebar.caption("Anything via st.sidebar.* or `with st.sidebar:` lives here")
    slot = st.empty()  # a single-element placeholder you can overwrite
    if st.button("Run countdown", key="cd"):
        for i in range(3, 0, -1):
            slot.metric("Countdown", i)
            time.sleep(0.5)
        slot.success("Liftoff 🚀")


# ═════════════════════ 4. DATA & CHARTS ═════════════════════
@st.cache_data
def make_df(n=30):
    rng = np.random.default_rng(1)
    return pd.DataFrame({"day": pd.date_range("2025-01-01", periods=n),
                         "sales": rng.integers(50, 200, n).cumsum(),
                         "visits": rng.integers(10, 60, n)})


@lesson("4 · Data & Charts", "Dataframes & editable tables")
def _():
    df = make_df()
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={"sales": st.column_config.ProgressColumn("Sales", max_value=int(df.sales.max())),
                                "day": st.column_config.DateColumn("Date")})
    edited = st.data_editor(df.head(5), num_rows="dynamic", key="editor")  # user can edit!
    st.caption(f"Edited rows return as a DataFrame: {edited.shape}")


@lesson("4 · Data & Charts", "Built-in charts")
def _():
    df = make_df().set_index("day")
    kind = st.segmented_control("Chart", ["line", "bar", "area"], default="line", key="ck")
    {"line": st.line_chart, "bar": st.bar_chart, "area": st.area_chart}[kind or "line"](df)
    st.scatter_chart(df, x="visits", y="sales")
    st.map(pd.DataFrame({"lat": [25.32], "lon": [82.97]}), zoom=8)  # Varanasi
    # Need more power? st.pyplot(fig), st.plotly_chart(fig), st.altair_chart(chart)


# ═════════════════════ 5. STATE ═════════════════════
@lesson("5 · State & Flow", "Rerun model + session_state + callbacks")
def _():
    # GOLDEN RULE: every interaction re-runs the script top→bottom.
    # Normal variables reset. st.session_state survives.
    if "count" not in st.session_state:
        st.session_state.count = 0

    def add(n):  # callbacks run BEFORE the rerun
        st.session_state.count += n

    c1, c2, c3 = st.columns(3)
    c1.button("➕ 1", on_click=add, args=(1,), key="s_add")
    c2.button("➕ 10", on_click=add, args=(10,), key="s_add10")
    c3.button("Reset", on_click=lambda: st.session_state.update(count=0), key="s_rst")
    st.metric("Persistent counter", st.session_state.count)

    plain = 0
    plain += 1
    st.write("Plain variable (always 1 after rerun):", plain)
    st.text_input("Widgets with a key are stored here too", key="s_echo")
    st.write("session_state['s_echo'] =", st.session_state.get("s_echo"))


@lesson("5 · State & Flow", "Forms (batch inputs → one rerun)")
def _():
    with st.form("signup"):
        email = st.text_input("Email")
        plan = st.selectbox("Plan", ["Free", "Pro"])
        ok = st.form_submit_button("Submit")  # nothing reruns until this is clicked
    if ok:
        st.success(f"Registered {email} on {plan}")


@lesson("5 · State & Flow", "Control flow: stop, rerun, fragments")
def _():
    @st.fragment  # only this block reruns on interaction – fast!
    def mini():
        v = st.slider("Fragment slider", 0, 10, 5, key="frag")
        st.write("Only this fragment reran:", v, time.strftime("%X"))

    mini()
    st.write("Full page rendered at:", time.strftime("%X"))
    # st.stop()  → halt script here   |   st.rerun() → restart script immediately


# ═════════════════════ 6. PERFORMANCE ═════════════════════
@lesson("6 · Performance", "Caching")
def _():
    @st.cache_data(ttl=60)  # for DATA (df, lists, numbers). Returns a copy.
    def slow_square(n):
        time.sleep(1.5)
        return n * n

    @st.cache_resource  # for GLOBAL OBJECTS (DB connections, ML models). Shared, not copied.
    def get_model():
        return {"model": "pretend-big-model"}

    n = st.number_input("n", 1, 100, 5, key="cache_n")
    t = time.time()
    result = slow_square(n)
    st.write(f"{n}² = {result} in {time.time() - t:.2f}s  (change n, then go back: instant!)")
    st.write(get_model())
    # slow_square.clear() empties that cache; st.cache_data.clear() empties all


# ═════════════════════ 7. FEEDBACK & CHAT ═════════════════════
@lesson("7 · Feedback & Chat", "Spinner, progress, status")
def _():
    if st.button("Simulate work", key="work"):
        with st.spinner("Crunching..."):
            time.sleep(1)
        bar = st.progress(0, text="Loading")
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1, text="Loading")
        with st.status("Pipeline", expanded=True) as s:
            st.write("Step 1 ✔")
            st.write("Step 2 ✔")
            s.update(label="Done!", state="complete")
        st.balloons()


@lesson("7 · Feedback & Chat", "Chat UI")
def _():
    if "msgs" not in st.session_state:
        st.session_state.msgs = [("assistant", "Hi! Type something.")]
    for role, text in st.session_state.msgs:
        with st.chat_message(role):
            st.write(text)
    if prompt := st.chat_input("Say hi"):
        st.session_state.msgs += [("user", prompt), ("assistant", f"You said: {prompt}")]
        st.rerun()


# ═════════════════════ 8. APP STRUCTURE ═════════════════════
@lesson("8 · App Structure", "Config, secrets, query params, multipage")
def _():
    st.markdown("""
- `st.set_page_config(...)` → **must be the first Streamlit call**
- **Secrets**: put keys in `.streamlit/secrets.toml`, read with `st.secrets["API_KEY"]`
- **Theme/config**: `.streamlit/config.toml`
- **Query params**: `st.query_params["user"] = "ada"` (shareable URLs)
- **Multipage**: create a `pages/` folder, or use `st.navigation([st.Page("a.py"), st.Page("b.py")])`
- **Connections**: `st.connection("sql")` for databases
""")
    st.write("Current query params:", dict(st.query_params))


# ═════════════════════ HOME & CHEAT SHEET ═════════════════════
def home():
    st.title("🚀 Streamlit Masterclass")
    st.markdown("Pick a section in the sidebar. Each lesson has a **Live output** tab and a **Code** tab.")
    st.info("**The one idea that explains everything:** each time a user interacts with a widget, "
            "Streamlit re-runs your whole script top to bottom. Widgets return their current value; "
            "`st.session_state` remembers things; caching avoids repeating slow work.")
    st.code("""
Script runs ─▶ widgets return values ─▶ UI drawn
     ▲                                     │
     └──────── user clicks / types ◀───────┘
""", language="text")


def cheat_sheet():
    st.title("📒 Cheat Sheet")
    a, b = st.columns(2)
    with a:
        st.markdown("##### Display")
        st.code("""st.write(x)  st.markdown("**hi**")
st.title / header / subheader / caption
st.dataframe(df)  st.table(df)  st.json(d)
st.metric("Label", 10, "+2")
st.line_chart(df)  st.bar_chart(df)
st.image("a.png")  st.video(url)
st.success / info / warning / error("msg")""", language="python")
        st.markdown("##### Layout")
        st.code("""c1, c2 = st.columns(2)
with c1: ...
t1, t2 = st.tabs(["A", "B"])
with st.expander("More"): ...
with st.sidebar: ...
with st.container(border=True): ...
slot = st.empty(); slot.write("x")""", language="python")
    with b:
        st.markdown("##### Widgets")
        st.code("""st.button("Go")           -> bool
st.text_input("Name")      -> str
st.number_input("n")       -> number
st.slider("x", 0, 10)      -> number
st.selectbox("c", opts)    -> item
st.multiselect("c", opts)  -> list
st.checkbox / st.toggle    -> bool
st.file_uploader("f")      -> file
st.form("k") + st.form_submit_button()""", language="python")
        st.markdown("##### State, cache, flow")
        st.code("""st.session_state["k"] = 1
st.button("x", on_click=fn, args=(1,))
@st.cache_data      # data
@st.cache_resource  # models / connections
@st.fragment        # partial rerun
st.rerun()   st.stop()
st.secrets["KEY"]   st.query_params""", language="python")
    st.markdown("##### Terminal")
    st.code("pip install streamlit\nstreamlit run app.py\nstreamlit hello   # built-in demo", language="bash")
    st.markdown("**Pro tips:** always give widgets a unique `key` · keep slow code in cached functions · "
                "use `st.form` to avoid reruns on every keystroke · never mutate cached return values.")


# ═════════════════════ ROUTER ═════════════════════
PAGES = ["🏠 Home", *LESSONS.keys(), "📒 Cheat Sheet"]
with st.sidebar:
    st.header("📚 Curriculum")
    page = st.radio("Section", PAGES, label_visibility="collapsed")

if page == "🏠 Home":
    home()
elif page == "📒 Cheat Sheet":
    cheat_sheet()
else:
    st.title(page)
    for title, fn in LESSONS[page]:
        render(title, fn)