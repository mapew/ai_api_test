import streamlit as st
from google import genai
from google.genai import types
from random import randint
import sqlite3
import fitz

with open("apikey", "r") as file:
    my_api_key = file.read().strip()

with open("instruct.md", "r") as file:
    HRD_BOT_P = file.read().strip()

client = genai.Client(api_key=my_api_key)

model_name = "gemini-2.0-flash"

def write_a_report_deviation(detial:str, reason_deviation:str, justification: str, other_in:str):
    """
        Write a deviation report, and save on pdf file
    """
    print("###### detail ######")
    print(detial)
    print("\n")
    print("###### reason for deviation ######")
    print(reason_deviation)
    print("\n")
    print("###### Justification for release or 'Use as Is' ######")
    print(justification)
    print("\n")
    print("###### Other Instructions ######")
    print(other_in)

    doc = fitz.open()

    page = doc.new_page()

    rect = fitz.Rect(10, 10, 600, 600)

    text = f"""###### detail ###### 
    {detial} 
    ###### reason for deviation ###### 
    {reason_deviation}
    ###### Final Decision ######
    {justification}
    ###### Other Instructions ######
    {other_in}
    """

    page.insert_textbox(rect, text, fontsize=12, color=(0, 0, 0))

    doc.save("test.pdf")
    doc.close()


def write_a_report_reject(detial:str,reason_reject:str, final_dec:str,other_in:str):
    """
        Write a rejection report, and save on pdf file
    """
    print("###### detail ######")
    print(detial)
    print("\n")
    print("###### reason for deviation ######")
    print(reason_reject)
    print("\n")
    print("###### Final Decision ######")
    print(final_dec)
    print("\n")
    print("###### Other Instructions ######")
    print(other_in)

    doc = fitz.open()

    page = doc.new_page()

    rect = fitz.Rect(10, 10, 600, 600)

    text = f"""###### detail ###### 
    {detial} 
    ###### reason for deviation ###### 
    {reason_reject}
    ###### Final Decision ######
    {final_dec}
    ###### Other Instructions ######
    {other_in}"""

    page.insert_textbox(rect, text, fontsize=12, color=(0, 0, 0))

    doc.save("test.pdf")
    doc.close()

def add_to_system(lot :str,pro_or_in : str, action: str,reason: str) -> int:
    """Add new to system with lot code, product or ingredient name, action, reason 
    Returns: the hold number that need to show User.
    """
 
    datas = {
    "Item": lot,
    "Lot": pro_or_in,
    "Reason": reason,
    "Action" : action
    }

    conn = sqlite3.connect("test.db")

    cursor = conn.cursor()
    sqlcommend = "INSERT INTO Hold (ITEM, LOT, REASON, ACTION) VALUES (?,?,?,?)"
    values = (datas.get("Item"),datas.get("Lot"),datas.get("Reason"),datas.get("Action"))

    try:
        cursor.execute(sqlcommend,values)
    except sqlite3.Error as e:
        return (f"Error inserting data: {e}")

    conn.commit()
    conn.close()

    print(datas)

    return randint(1, 100)

action_system = [
    add_to_system,
    write_a_report_deviation,
    write_a_report_reject,
]


st.title("Hold and Dispose Assistance")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=model_name,
        config=types.GenerateContentConfig(system_instruction=HRD_BOT_P,tools=action_system),   
    )

user_input = st.chat_input("Say something", accept_file=True, file_type=["jpg", "jpeg", "png"])

if user_input and user_input.text:
    st.session_state.chat_history.append({"role": "user", "content": user_input.text})
    response = st.session_state.chat_session.send_message(user_input.text)
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input and user_input.files:
    st.image(user_input.files[0])
