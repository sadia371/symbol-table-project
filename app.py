import streamlit as st
import pandas as pd
import json
from datetime import datetime

from lexer import LexicalAnalyzer
import symbol_table


# -----------------------------
# INITIAL SETUP
# -----------------------------

st.set_page_config(page_title="Compiler Dashboard", layout="wide")

lexer = LexicalAnalyzer()
symbols = symbol_table.SymbolTable()

if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# SIDEBAR MENU
# -----------------------------

menu = st.sidebar.selectbox(
    "Compiler Menu",
    [
        "Code Input",
        "Tokens View",
        "Symbol Table",
        "Charts",
        "Save Symbol Tables"
    ]
)

st.sidebar.markdown("### Compiler System Dashboard")


# -----------------------------
# PAGE 1: CODE INPUT
# -----------------------------

if menu == "Code Input":

    st.title("Input Source Code")

    code = st.text_area("Enter Code", height=250,
                        value="int x = 10;\n{\n int y = 20;\n}")

    if st.button("Run Compiler"):

        tokens, errors = lexer.tokenize(code)

        # store in session history
        st.session_state.tokens = tokens
        st.session_state.errors = errors

        # build symbol table
        symbols = symbol_table.SymbolTable()

        for t in tokens:
            symbols.insert(
                t["token"],
                t["lexeme"],
                t["line"],
                t["scope"]
            )

        st.session_state.symbols = symbols

        # save snapshot
        st.session_state.history.append({
            "time": str(datetime.now()),
            "tokens": tokens,
            "symbols": symbols.get_table()
        })

        st.success("Compilation Completed Successfully")


# -----------------------------
# PAGE 2: TOKENS VIEW
# -----------------------------

elif menu == "Tokens View":

    st.title("Generated Tokens")

    tokens = st.session_state.get("tokens", [])

    if tokens:
        df = pd.DataFrame(tokens)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Run compiler first")


# -----------------------------
# PAGE 3: SYMBOL TABLE
# -----------------------------

elif menu == "Symbol Table":

    st.title("Symbol Table")

    symbols = st.session_state.get("symbols", None)

    if symbols:
        df = pd.DataFrame(symbols.get_table())
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No symbol table generated yet")


# -----------------------------
# PAGE 4: CHARTS
# -----------------------------

elif menu == "Charts":

    st.title("Compiler Analytics")

    tokens = st.session_state.get("tokens", [])

    if tokens:

        df = pd.DataFrame(tokens)

        st.subheader("Token Distribution")
        st.bar_chart(df["token"].value_counts())

        st.subheader("Scope Distribution")
        st.bar_chart(df["scope"].value_counts())

    else:
        st.info("No data available")


# -----------------------------
# PAGE 5: SAVE HISTORY
# -----------------------------

elif menu == "Save Symbol Tables":

    st.title("Saved Compiler Runs")

    if st.session_state.history:

        for i, item in enumerate(st.session_state.history):

            st.subheader(f"Run {i+1} - {item['time']}")

            df = pd.DataFrame(item["symbols"])
            st.dataframe(df)

            # download option
            st.download_button(
                f"Download Run {i+1}",
                data=df.to_csv(index=False),
                file_name=f"symbol_table_{i+1}.csv"
            )

    else:
        st.info("No saved runs yet")