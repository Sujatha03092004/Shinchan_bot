import streamlit as st
import ollama
from streamlit_drawable_canvas import st_canvas

# -----------------------------
# Page Configuration & Styling
# -----------------------------
st.set_page_config(page_title="Shin-chan's Sketchbook", layout="centered")

# INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "snack_count" not in st.session_state:
    st.session_state.snack_count = 0

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🖍️ Shin's Desk")
    st.markdown(f"### 🍪 Chocobi Points: {st.session_state.snack_count}")
    
    hero_mode = st.toggle("🚀 Action Kamen Mode!")
    
    # DYNAMIC GIFS
    if hero_mode:
        st.image("https://media1.tenor.com/m/yeDr-4s-oLMAAAAC/shinchan-crayonshinchan.gif", use_container_width=True)
    else:
        st.image("https://media1.tenor.com/m/ZgIRCUMksogAAAAC/sing-crayon-shin-chan.gif", use_container_width=True)
    
    st.markdown('---')
    model = st.selectbox("Model", ["gemma3:latest", "llava:latest"])
    temp = st.slider("Mischief Level", 0.0, 1.5, 0.9)

    if st.button("🗑️ Throw in Trash"):
        st.session_state.messages = []
        st.session_state.snack_count = 0
        st.rerun()

# --- CSS: LIGHT RED THEME & CONTRAST ---
bg_color = "#E1F5FE" if hero_mode else "#FFEBEE" 
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .stMarkdown, p, span, div, .stChatMessage {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}
    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #D32F2F;
        border-radius: 15px;
        margin-bottom: 10px;
    }}
    h1 {{ color: {"#0D47A1" if hero_mode else "#C62828"} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Action Kamen AI" if hero_mode else "🖍️ しんちゃん AI Sketchbook")

# Persona Definitions
base_persona = "You are Shin-chan. Mischievous, love Chocobi, say Buri Buri."
if hero_mode:
    base_persona = "You are ACTION KAMEN! Heroic, loud, WA-HA-HA-HA! Talk about justice."

# -----------------------------
# DRAWING SECTION WITH AI COMMENTS
# -----------------------------
if not hero_mode:
    st.subheader("🎨 Draw for Shin-chan!")
    c1, c2 = st.columns([1, 2])
    with c1:
        color = st.color_picker("Pick Crayon", "#D32F2F")
    with c2:
        thickness = st.slider("Thickness", 1, 20, 5)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=thickness,
        stroke_color=color,
        background_color="#FFFFFF",
        height=300,
        width=700,
        drawing_mode="freedraw",
        key="verified_canvas",
    )

    if st.button("🖼️ Show Shin-chan!"):
        if canvas_result.image_data is not None:
            # 1. Update Points
            st.session_state.snack_count += 5 
            
            # 2. Add "Drawing" Action to history
            st.session_state.messages.append({"role": "user", "content": "Look! I drew a picture for you on the sketchbook!", "avatar": "👤"})
            
            # 3. Trigger AI comment about the drawing
            with st.spinner("Shin-chan is looking at your art..."):
                comment_prompt = [
                    {"role": "system", "content": base_persona},
                    {"role": "user", "content": "I just finished a drawing on the sketchbook. Comment on my art in your funny Shin-chan style! Use Buri Buri!"}
                ]
                response = ollama.chat(model=model, messages=comment_prompt)
                reply = response["message"]["content"]
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply,
                    "avatar": "🍑"
                })
            st.rerun() 
else:
    st.info("⚡ Action Kamen is on patrol! Justice prevails!")

st.markdown("---")

# -----------------------------
# CHAT SECTION
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.write(msg["content"])

user_input = st.chat_input("Message...")

if user_input:
    st.session_state.snack_count += 1 
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "👤"})
    
    # Prepare history for AI
    ollama_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    ollama_msgs.insert(0, {"role": "system", "content": base_persona})
    
    with st.spinner("Thinking..."):
        response = ollama.chat(model=model, messages=ollama_msgs)
        reply = response["message"]["content"]
        
    st.session_state.messages.append({
        "role": "assistant", 
        "content": reply,
        "avatar": "🚀" if hero_mode else "🍑"
    })
    st.rerun()