import random
import streamlit as st

st.set_page_config(page_title="Quick Decision Maker", page_icon="⚡", layout="centered")

# ---------------------------
# Data
# ---------------------------
OUTDOOR = {
    "👟 Sport": ["Bedminton", "Swimming", "Tennis", "Squash", "Gym"],
    "🎬 Cinema": ["Horror", "Fantasy", "Sci-fi", "Documentary"],
    "🍗 Food": ["Roxor burger", "Nuddles", "Ramen", "Pizza", "Cernohorsky snitzel", "That amazing croissants", "Pad Thai"],
    "૮₍ • ᴥ • ₎ა Dog walking": ["Zelezna studnicka", "Koliba", "Drazdiak", "Marianka", "Forest in Rusovce",
                    "Small walk around neighbourhood", "Short trip around Bratislava"],
    "🍻 Plan with friends": ["Bowling", "Swimming", "Darts", "8 pool", "Laser game", "Restaurant",
                          "Drinking & boardgames", "Short trip", "Shopping"],
    "☕ Coffee": ["Zelezna studnicka", "Vespaio", "Koliba", "Coffee in the old town", "Coffee under the castle"],
}

INDOOR = {
    "🥞 Breakfast meal": {
        "I dont have enough eggs": ["Sadwich", "Baguette", "Oatmeal"],
        "I have enough eggs": ["Pancakes", "Roasted eggs", "Sandwich with eggs"],
    },
    "🍽️ Lunch/Dinner": {
        "I want something new": ["Then cook something new lol"],
        "I dont have Salca": ["Creamy pasta with chicken", "Donner", "Tantuni", "Burger", "Pure with meatballs",
                              "Cernohorsky snitzel", "Potatoes/Rice with chicken", "Bryndzove Halusky",
                              "Fried cheese with fries"],
        "I dont have potatoes": ["Creamy pasta with chicken", "Donner", "Tantuni", "Burger", "Fried cheese with fries"],
        "I am loosing weight": ["Fruit", "Jogurt with musli", "Jogurt salat"],
    },
    "👌 Im bored and I want to do something on my own": {
        "🌞 Its afternoon": ["Watching TR TV shows", "Watching Netflix/Max", "Watching YouTube",
                          "Going for a walk", "Deep cleaning", "Baking a dessert"],
        "🌙 Its evening": ["Reading a book", "Watching TR TV shows", "Watching Netflix/Max",
                        "Watching YouTube", "Baking a dessert"],
    },
    "🤜🤛 Im bored and I dont want to be alone": {
        "🌞 Its afternoon": ["Playing with my dog", "Watching Netflix/Max/YouTube with my husband",
                          "Going for a walk with my husband"],
        "🌙 Its evening": ["Playing co-op videogames", "Calling my family", "Lego with my husband",
                        "Watching Netflix/Max/YouTube with my husband"],
    },
}

# ---------------------------
# Helpers
# ---------------------------
def pick_random(items: list[str]) -> str:
    return random.choice(items) if items else "No options found."

def big_buttons_css():
    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            padding: 1.1rem 1rem;
            font-size: 1.2rem;
            border-radius: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def centered_result_box(text: str):
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin-top:30px;">
            <div style="
                width: 100%;
                max-width: 700px;
                text-align:center;
                padding: 28px 18px;
                border-radius: 18px;
                border: 2px solid rgba(255, 75, 75, 0.35);
                background: rgba(255, 75, 75, 0.06);
                font-size: 28px;
                font-weight: 700;
            ">
                ✅ {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

big_buttons_css()

# ---------------------------
# Session state
# ---------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "mode" not in st.session_state:
    st.session_state.mode = None  # "outdoor" / "indoor"

if "indoor_category" not in st.session_state:
    st.session_state.indoor_category = None

if "indoor_subcategory" not in st.session_state:
    st.session_state.indoor_subcategory = None

if "result" not in st.session_state:
    st.session_state.result = None  # FINAL decision lock

# ---------------------------
# Title
# ---------------------------
st.markdown(
    """
    <h1 style="text-align:center; line-height:1.2;">
    Desperate to decide and time is passing too quickly?<br>
    Dont worry, The <span style="color:#6a943c;">QUICK DECISION MAKER</span> is here for you!
    </h1>
    """,
    unsafe_allow_html=True,
)
st.write("")

# ---------------------------
# If final decision exists -> LOCK everything
# ---------------------------
if st.session_state.result is not None:
    centered_result_box(st.session_state.result)
    st.write("")
    st.info("Locked 🔒 Refresh the page (F5 / Ctrl+R) if you want a new decision.")
    st.stop()

# ---------------------------
# Step 0: BEGIN
# ---------------------------
if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("BEGIN", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.stop()

# ---------------------------
# Step 1: Outdoor vs Indoor 
# ---------------------------
if st.session_state.mode is None:
    st.subheader("Choose a category:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌳 Outdoor activity", use_container_width=True):
            st.session_state.mode = "outdoor"
            st.rerun()  

    with col2:
        if st.button("🏠 Indoor activity", use_container_width=True):
            st.session_state.mode = "indoor"
            st.rerun() 

    st.stop()

# ---------------------------
# Step 2A: Outdoor -> pick a subcategory -> FINAL result set once
# ---------------------------
if st.session_state.mode == "outdoor":
    st.subheader("Outdoor activity — choose one:")
    for cat_name, options in OUTDOOR.items():
        if st.button(f"➡️ {cat_name}"):
            # set FINAL result and lock
            st.session_state.result = f"{cat_name}: {pick_random(options)}"
            st.rerun()

# ---------------------------
# Step 2B: Indoor -> main category -> subcategory -> FINAL result
# ---------------------------
if st.session_state.mode == "indoor":
    st.subheader("Indoor activity — choose one:")

    if st.session_state.indoor_category is None:
        for main_cat in INDOOR.keys():
            if st.button(f"➡️ {main_cat}"):
                st.session_state.indoor_category = main_cat
                st.rerun()
        st.stop()

    st.markdown(f"### {st.session_state.indoor_category}")
    sub_map = INDOOR[st.session_state.indoor_category]

    if st.session_state.indoor_subcategory is None:
        st.write("Choose one:")
        for sub_cat, options in sub_map.items():
            if st.button(f"➡️ {sub_cat}"):
                st.session_state.indoor_subcategory = sub_cat
                st.session_state.result = f"{sub_cat}: {pick_random(options)}"
                st.rerun()
