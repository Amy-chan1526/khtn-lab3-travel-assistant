import streamlit as st
from firebase_client import sign_in, sign_up
from rag import load_and_embed_knowledge_base, retrieve_top_k, generate_rag_answer

# Page layout setup
st.set_page_config(page_title="Saigon Travel Assistant", page_icon="🏙️")

# Initialize session state for user session and chat history
if "user" not in st.session_state:
    st.session_state["user"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Cache knowledge base embeddings once across app runs
@st.cache_resource
def get_cached_knowledge_base():
    return load_and_embed_knowledge_base("knowledge_base.json")


# LOGIN / SIGN-UP VIEW (Unauthenticated)
if st.session_state["user"] is None:
    st.title("🏙️ Saigon Travel Assistant")
    st.write("Please sign in to access the RAG chat assistant.")

    tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

    with tab_login:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In", key="btn_login"):
            if not login_email or not login_password:
                st.error("Please provide both email and password.")
            else:
                res = sign_in(login_email, login_password)
                if res["success"]:
                    st.session_state["user"] = res["email"]
                    st.success("Signed in successfully!")
                    st.rerun()
                else:
                    st.error(f"Sign-in error: {res['error']}")

    with tab_signup:
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up", key="btn_signup"):
            if not signup_email or not signup_password:
                st.error("Please provide valid details.")
            else:
                res = sign_up(signup_email, signup_password)
                if res["success"]:
                    st.session_state["user"] = res["email"]
                    st.success("Account registered successfully!")
                    st.rerun()
                else:
                    st.error(f"Sign-up error: {res['error']}")

# RAG CHAT VIEW (Authenticated)
else:
    # Sidebar user status & logout
    st.sidebar.title("User Session")
    st.sidebar.write(f"Logged in as: **{st.session_state['user']}**")
    if st.sidebar.button("Sign Out"):
        st.session_state["user"] = None
        st.session_state["messages"] = []  # Clear chat history on logout
        st.rerun()

    st.title("🤖 Ho Chi Minh City Assistant")
    st.caption("Ask questions about Ho Chi Minh City landmarks, food, and culture.")

    # Load embedded KB
    try:
        embedded_kb = get_cached_knowledge_base()
    except Exception as err:
        st.error(f"Failed to load knowledge base or reach Ollama server: {err}")
        st.stop()

    # Display prior session chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "retrieved" in msg and msg["retrieved"]:
                with st.expander("🔍 Retreived Entries & Similarity Scores"):
                    for entry, score in msg["retrieved"]:
                        st.markdown(f"- **[{entry['id']}] {entry['title']}** (Cosine: `{score:.4f}`)")
                        st.caption(entry["text"])

    # User query input handling
    if prompt := st.chat_input("Ask a question (e.g., What is Com Tam?)...."):
        if not prompt.strip():
            st.warning("Question cannot be empty.")
        else:
            # Append user message
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Retrieving information..."):
                    try:
                        retrieved = retrieve_top_k(prompt, embedded_kb, top_k=3)
                        answer = generate_rag_answer(prompt, retrieved)
                        
                        st.write(answer)
                        with st.expander("🔍 Retreived Entries & Similarity Scores"):
                            for entry, score in retrieved:
                                st.markdown(f"- **[{entry['id']}] {entry['title']}** (Cosine: `{score:.4f}`)")
                                st.caption(entry["text"])

                        # Store response in session state
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": answer,
                            "retrieved": retrieved
                        })
                    except Exception as exc:
                        st.error(f"Error processing request: {str(exc)}")