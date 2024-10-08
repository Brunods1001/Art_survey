# Main script for Art survey data collection
# to run the app: streamlit run your_script.py [-- script args]
# ctrl + c to stop the app

import streamlit as st
from streamlit_sortables import sort_items
# st.snow()
# st.toast('Ready!', icon='🥞')v

st.title("In Basket LLM draft generation survey")
st.caption("Some caption here")
st.markdown("**Purpose**: something")
st.markdown("**Methods**: something")

st.divider()
st.subheader("About you")
st.text_input("Institution:", key="institution")
st.session_state.institution
with st.container():
    col1, col2 = st.columns(2)
    col1.markdown("Has your institution piloted in basket LLM draft generation?")
    col2.toggle("Yes", "No", key="pilot")
st.checkbox("My instutition has piloted in basket LLM draft generation")#, key="pilot")
st.multiselect("Role:", ["Health system leadership", "Implementation team for LLM draft generation"],
               key="role")
st.markdown("Role:")
st.checkbox("Health system leadership")
st.checkbox("Implementation team for LLM draft generation")
st.number_input("Years in current role:", key="role_y", value=None)
st.checkbox("We have halted use of LLM draft generation", key="halt")
if st.session_state.halt:
    st.text_input("Reason for halting:", key="halt_reason")

st.divider()
st.subheader("About your institution's LLM draft generation implementation")
st.markdown("This type of question might have problems.")
# sort of ranking
# documentation: https://pypi.org/project/streamlit-sortables/
# github: https://github.com/ohtaman/streamlit-sortables
st.write("Rank the following metrics you'd find most useful for assessing LLM draft generation:")
original_items = [
    {'header': "I care about these:",  'items': ['Utilization', 'EHR vendor-provided free text feedback', 'EHR vendor-provided quantitative feedback',
                  'Institutional survey', 'Performance on a set of challenging messages (e.g. "red teaming")', 
                  'Patient feedback', 'In basket volume', 'Burnout scores']},
    {'header': "I don't care about these:", 'items': ['Other']}
]
sorted_items = sort_items(original_items, multi_containers=True)
if "Other" in sorted_items[0]["items"]:
     st.text_input("Other:")

st.divider()
st.subheader("ROI")
st.markdown("Pre- and post-implementation benefits")
with st.container():
    col1, col2 = st.columns(2)
    col1.markdown("Increased billable visits")
    with col2:
        st.feedback("thumbs")
        st.feedback("faces")
        st.feedback("stars")
        st.select_slider(label="",
                         options=["strongly disagree","disagree","ambivalent","agree","strongly agree"], 
                         value="ambivalent")
    col1.markdown("Increased messaging throughput/efficiency")
    col1.markdown("Prestige of my instutition")
    col1.caption("I expected implementing ART would improve external views of my institution. ")

st.divider()
st.subheader("Future directions")
st.radio("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
          ["increase", "maintain", "reduce"], index=None)
st.selectbox("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
             ["increase", "maintain", "reduce"], index=None)
st.select_slider("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
                 options=["reduce", "maintain", "increase"], value="maintain")