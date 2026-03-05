import streamlit as st
from chatbot_logic import get_response, get_characters

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Vault",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CHARACTERS = get_characters()

# ── CSS ────────────────────────────────────────────────────────────────────────
def get_css(accent_color: str = "#FF4D6D"):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    background: #0d0d12 !important;
    color: #e8e6e1 !important;
    font-family: 'Inter', sans-serif;
}}

[data-testid="stAppViewContainer"] > .main {{
    background: #0d0d12 !important;
}}

[data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
footer {{ display: none !important; }}

.vault-header {{
    text-align: center;
    padding: 2.5rem 1rem 1rem;
    position: relative;
}}

.vault-header h1 {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 6vw, 3.5rem);
    letter-spacing: -0.02em;
    color: #fff;
    line-height: 1.1;
}}

.vault-header h1 span {{
    color: {accent_color};
}}

.vault-subtitle {{
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.4rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 400;
}}

.lock-icon {{
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
    display: block;
}}

/* Character selection cards */
.char-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    max-width: 520px;
    margin: 0 auto;
    padding: 0.5rem;
}}

.char-card {{
    background: #161620;
    border: 1.5px solid #222;
    border-radius: 16px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.char-card:hover {{
    border-color: {accent_color};
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}}

.char-card.selected {{
    border-color: {accent_color};
    background: #1a1a24;
    box-shadow: 0 0 0 1px {accent_color}44, 0 8px 24px rgba(0,0,0,0.4);
}}

.char-emoji {{ font-size: 2rem; margin-bottom: 0.4rem; display: block; }}
.char-name {{
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #fff;
}}
.char-tagline {{
    font-size: 0.75rem;
    color: #888;
    margin-top: 0.2rem;
    line-height: 1.4;
}}
.char-badge {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {accent_color};
    font-weight: 500;
    margin-top: 0.3rem;
}}

/* Input fields */
.stTextInput > div > div > input {{
    background: #161620 !important;
    border: 1.5px solid #2a2a35 !important;
    border-radius: 12px !important;
    color: #e8e6e1 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}}

.stTextInput > div > div > input:focus {{
    border-color: {accent_color} !important;
    box-shadow: 0 0 0 3px {accent_color}22 !important;
}}

.stTextInput > div > div > input::placeholder {{ color: #444 !important; }}

/* Buttons */
.stButton > button {{
    background: {accent_color} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}}

.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px {accent_color}44 !important;
}}

/* Chat area */
.chat-wrapper {{
    max-width: 680px;
    margin: 0 auto;
    padding: 0 0.5rem;
}}

.active-char-bar {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #161620;
    border: 1px solid #222;
    border-radius: 12px;
    padding: 0.65rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #aaa;
}}

.active-char-bar strong {{
    color: {accent_color};
    font-family: 'Syne', sans-serif;
}}

.privacy-note {{
    font-size: 0.72rem;
    color: #444;
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}}

/* Message bubbles */
.msg-user {{
    display: flex;
    justify-content: flex-end;
    margin: 0.5rem 0;
}}

.msg-user .bubble {{
    background: {accent_color}22;
    border: 1px solid {accent_color}44;
    color: #e8e6e1;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 75%;
    font-size: 0.92rem;
    line-height: 1.55;
    white-space: pre-wrap;
}}

.msg-ai {{
    display: flex;
    justify-content: flex-start;
    margin: 0.5rem 0;
    gap: 0.5rem;
    align-items: flex-end;
}}

.msg-ai .avatar {{
    font-size: 1.4rem;
    flex-shrink: 0;
    margin-bottom: 2px;
}}

.msg-ai .bubble {{
    background: #161620;
    border: 1px solid #252530;
    color: #ddd;
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1.1rem;
    max-width: 78%;
    font-size: 0.92rem;
    line-height: 1.6;
    white-space: pre-wrap;
}}

/* Chat input row */
.chat-input-area {{
    display: flex;
    gap: 0.5rem;
    align-items: flex-end;
    position: sticky;
    bottom: 0;
    background: #0d0d12;
    padding: 0.75rem 0 0.5rem;
    border-top: 1px solid #1a1a22;
    margin-top: 0.5rem;
}}

.exit-hint {{
    text-align: center;
    font-size: 0.72rem;
    color: #333;
    margin-top: 0.3rem;
    letter-spacing: 0.05em;
}}

/* Divider */
hr {{
    border: none !important;
    border-top: 1px solid #1e1e28 !important;
    margin: 1.5rem 0 !important;
}}

/* Label colors */
label, .stTextInput label {{
    color: #888 !important;
    font-size: 0.8rem !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: #0d0d12; }}
::-webkit-scrollbar-thumb {{ background: #2a2a35; border-radius: 4px; }}

/* Welcome section */
.welcome-section {{
    max-width: 480px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
}}

.section-label {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #444;
    margin-bottom: 0.8rem;
    padding-left: 0.2rem;
}}

.alias-note {{
    font-size: 0.78rem;
    color: #555;
    margin-top: 0.4rem;
    padding-left: 0.2rem;
}}

/* Scrollable chat messages */
.messages-container {{
    max-height: 58vh;
    overflow-y: auto;
    padding: 0.5rem 0;
}}

[data-testid="stChatMessage"] {{
    background: transparent !important;
}}

/* ── News Ticker ── */
.ticker-wrap {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #111118;
    border-top: 2px solid {accent_color};
    z-index: 9999;
    display: flex;
    align-items: center;
    height: 36px;
    overflow: hidden;
}}
.ticker-tag {{
    background: {accent_color};
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0 1rem;
    height: 100%;
    display: flex;
    align-items: center;
    white-space: nowrap;
    flex-shrink: 0;
}}
.ticker-track {{
    display: flex;
    animation: ticker-scroll 30s linear infinite;
    white-space: nowrap;
}}
.ticker-track:hover {{ animation-play-state: paused; }}
.ticker-item {{
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    color: #bbb;
    padding: 0 2.5rem;
    letter-spacing: 0.03em;
}}
.ticker-item b {{ color: {accent_color}; }}
@keyframes ticker-scroll {{
    0%   {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
}}
[data-testid="stAppViewContainer"] > .main > .block-container {{
    padding-bottom: 55px !important;
}}
</style>
"""

# ── Session State Init ─────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "select"  # select | chat
if "character" not in st.session_state:
    st.session_state.character = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_char_temp" not in st.session_state:
    st.session_state.selected_char_temp = None

# ── Inject CSS ─────────────────────────────────────────────────────────────────
accent = CHARACTERS[st.session_state.character]["color"] if st.session_state.character else "#FF4D6D"
st.markdown(get_css(accent), unsafe_allow_html=True)

# ── News Ticker (always visible) ───────────────────────────────────────────────
# ✏️  Edit the names below to your actual group members
TEAM = [
    "Yash Maheshwari" ,"Vansh Singhal","Kushagra Arora","Nischay Chauhan","Ashish"
]
ticker_items = " &nbsp;★&nbsp; ".join([f"<span class='ticker-item'><b>✦</b> {name}</span>" for name in TEAM])
# duplicate for seamless loop
ticker_items_double = ticker_items + " &nbsp;★&nbsp; " + ticker_items

st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker-tag">🔐 Made by</div>
    <div style="overflow:hidden; flex:1;">
        <div class="ticker-track">{ticker_items_double}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — Character & Alias Selection
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "select":

    st.markdown("""
    <div class="vault-header">
        <span class="lock-icon">🔐</span>
        <h1>The <span>Vault</span></h1>
        <p class="vault-subtitle">say anything · be anyone · it all disappears</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-section">
        <div class="section-label">Choose your companion</div>
    </div>
    """, unsafe_allow_html=True)

    # Character cards using Streamlit columns
    col1, col2 = st.columns(2)
    char_names = list(CHARACTERS.keys())

    def make_card(name, col):
        char = CHARACTERS[name]
        is_sel = st.session_state.selected_char_temp == name
        border_style = f"border: 2px solid {char['color']};" if is_sel else "border: 1.5px solid #222;"
        bg_style = "background: #1a1a24;" if is_sel else "background: #161620;"
        with col:
            st.markdown(f"""
            <div class="char-card {'selected' if is_sel else ''}" 
                 style="{border_style} {bg_style}">
                <span class="char-emoji">{char['emoji']}</span>
                <div class="char-name">{name}</div>
                <div class="char-tagline">{char['tagline']}</div>
                <div class="char-badge">{'♀ girl' if char['gender'] == 'girl' else '♂ boy'}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Pick {name}", key=f"pick_{name}"):
                st.session_state.selected_char_temp = name
                st.rerun()

    make_card(char_names[0], col1)
    make_card(char_names[1], col2)
    col3, col4 = st.columns(2)
    make_card(char_names[2], col3)
    make_card(char_names[3], col4)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Alias input
    st.markdown("""
    <div class="welcome-section">
        <div class="section-label">Your alias for this session</div>
    </div>
    """, unsafe_allow_html=True)

    alias_input = st.text_input(
        "",
        placeholder="Ghost, Shadow, anything you want...",
        key="alias_field",
        label_visibility="collapsed",
    )
    st.markdown("""
    <p class="alias-note">🤫 No real names needed. This is your private space.</p>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 3rem;">
        <p style="font-size:0.68rem; color:#2a2a35; letter-spacing:0.15em; text-transform:uppercase; font-family:'Syne',sans-serif;">
            made with 🤍 by
        </p>
        <p style="font-size:0.8rem; color:#3a3a48; margin-top:0.35rem; letter-spacing:0.06em;">
            Yash &nbsp;·&nbsp; Muskan &nbsp;·&nbsp; Member C &nbsp;·&nbsp; Member D
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Enter the Vault →", key="enter_btn"):

        if not st.session_state.selected_char_temp:
            st.warning("Pick a companion first.")
        elif not alias_input.strip():
            st.warning("Give yourself an alias.")
        else:
            st.session_state.character = st.session_state.selected_char_temp
            st.session_state.user_alias = alias_input.strip()
            st.session_state.stage = "chat"
            st.session_state.messages = []
            # Opening message from character
            char = CHARACTERS[st.session_state.character]
            opening_lines = {
                "Tokyo": f"Hey {alias_input.strip()} 👋 I'm Tokyo. No rules here, no judgment — just us. What's going on in that head of yours?",
                "Nairobi": f"Hey {alias_input.strip()} 🌻 I'm Nairobi. Whatever you're carrying right now — you don't have to carry it alone anymore. Talk to me.",
                "Berlin": f"{alias_input.strip()}. I'm Berlin. This space is yours — I won't repeat a word of it, and I won't judge a single thought. Begin.",
                "Rio": f"Yooo {alias_input.strip()}! 💙 It's Rio. Okay so this is literally a no-BS zone — say whatever, feel whatever. I'm here for it. What's up?",
            }
            st.session_state.messages.append({
                "role": "assistant",
                "content": opening_lines[st.session_state.character],
            })
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — Chat
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "chat":

    char = CHARACTERS[st.session_state.character]

    st.markdown(f"""
    <div class="vault-header" style="padding:1.2rem 1rem 0.5rem;">
        <h1>The <span>Vault</span></h1>
    </div>
    """, unsafe_allow_html=True)

    # Active bar
    st.markdown(f"""
    <div class="chat-wrapper">
        <div class="active-char-bar">
            <span>{char['emoji']}</span>
            <span>Talking with <strong>{st.session_state.character}</strong> as <strong style="color:#aaa">{st.session_state.user_alias}</strong></span>
            <span class="privacy-note">🔒 vanishes on exit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Messages
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-ai">
                <div class="avatar">{char['emoji']}</div>
                <div class="bubble">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Input
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with st.container():
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "",
                placeholder="Say anything... (type 'exit' to close the vault)",
                key="chat_input",
                label_visibility="collapsed",
            )
        with btn_col:
            send = st.button("Send", key="send_btn")

    st.markdown("""
    <p class="exit-hint">type <strong>exit</strong> anytime to close the vault — everything disappears 🔒</p>
    """, unsafe_allow_html=True)

    # Handle send
    if send and user_input.strip():
        text = user_input.strip()

        # EXIT command
        if text.lower() in ["exit", "bye", "quit", "goodbye", "close"]:
            st.session_state.stage = "goodbye"
            st.rerun()

        # Normal message
        st.session_state.messages.append({"role": "user", "content": text})

        # Build history for API (exclude the opening AI message from "history" passed in,
        # since it's injected by persona - keep last N turns only for efficiency)
        history = [m for m in st.session_state.messages[:-1]]

        with st.spinner(f"{st.session_state.character} is typing..."):
            reply = get_response(
                message=text,
                history=history,
                character=st.session_state.character,
                user_alias=st.session_state.user_alias,
            )

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — Goodbye
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "goodbye":

    char = CHARACTERS.get(st.session_state.character, list(CHARACTERS.values())[0])

    goodbyes = {
        "Tokyo": "Gone. Like it never happened. Take care of yourself out there. 🔥",
        "Nairobi": "The vault is sealed. Whatever you shared here was safe, and it stays safe. You're not alone. 🌻",
        "Berlin": "All things that begin must end. What was said here belongs to no one now. Walk on. 🖤",
        "Rio": "Vault's locked up. You did good coming here. Take care of yourself, yeah? 💙",
    }

    st.markdown(f"""
    <div class="vault-header" style="padding-top:4rem;">
        <span class="lock-icon">🔐</span>
        <h1>Vault <span>Sealed</span></h1>
        <p class="vault-subtitle">{goodbyes.get(st.session_state.character, 'All gone. Take care.')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#444; font-size:0.82rem; line-height:1.8;">
        This session is over.<br>
        No logs. No memory. It's all gone.<br><br>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Open a New Vault →", key="restart_btn"):
            for key in ["stage", "character", "user_alias", "messages", "selected_char_temp"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()