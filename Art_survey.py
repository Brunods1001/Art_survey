# Main script for Art survey data collection
# to run the app: streamlit run your_script.py [-- script args]
# ctrl + c to stop the app

# git status
# git add Art_survey.py requirements.txt
# git commit -m "Updated"
# git push
# git log

# Notes from meeting with Will 10/16/24
# only show questions if they have piloted
# ranking - show numbers?
# ROI - list things, then show Likert for expectatioins vs reality
#   also show Likert as discrete things; maybe smiley faces with a key
#   try radio buttons too
# future directions - radio buttons

import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
# from streamlit_gsheets import GSheetsConnection
# conn = st.connection("gsheets", type=GSheetsConnection)

# st.toast('Ready!', icon='🥞')

def grid_2col_1row(height):
    col1, col2 = st.columns(2)
    col1 = col1.container(height=height, border=False)
    col2 = col2.container(height=height, border=False)
    return col1, col2
def grid_3col_1row(height):
    col1, col2, col3 = st.columns(3)
    col1 = col1.container(height=height, border=False)
    col2 = col2.container(height=height, border=False)
    col3 = col3.container(height=height, border=False)
    return col1, col2, col3
placeholder = st.empty()
def submitted():
    data = st.session_state.get("data", [])
    print("submitted", data)
    st.session_state.submitted = True
    if isinstance(data, list):
        with open("data.csv", "a") as f:
            txt = ",".join(str(d) for d in data) + "\n"
            f.write(txt)
    elif isinstance(data, pd.DataFrame):
        try:
            df = pd.read_csv("data.csv")
            print("read data.csv")
        except FileNotFoundError:
            print("File not found")
            data.to_csv("data.csv")
        else:
            df = pd.concat([data, df], ignore_index=True)
            print("writing to data.csv")
            df.to_csv("data.csv")
            print("wrote to data.csv")
    # with placeholder.container():
    #     st.title("In Basket LLM draft generation survey")
    #     st.caption("Some caption here")
    #     st.markdown("**Purpose**: something")
    #     st.markdown("**Methods**: something")
    #     st.title("Submitted!")
    #     st.write("Thank you for your submission!")
    # st.snow()
    st.balloons()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
halt_reason=""
other_metric=""
role_leader=""
role_implementation=""
halt=""
halt_reason=""
# sorted_metrics=""
faces=""
likert=""
invest1=""


if st.session_state.submitted:
    with placeholder.container():
        st.title(":gray[In Basket LLM draft generation survey]")
        st.caption("Some caption here")
        st.write(""":gray[**Purpose**: something]  
                 :gray[**Methods**: something]""")
        st.title(":red[Submitted!]")
        st.write(":rainbow[Thank you for your submission!]")
    st.stop()

# else:
with placeholder.container():
    st.title("In Basket LLM draft generation survey")
    st.caption("Some caption here")
    st.write("""**Purpose**: something  
             **Methods**: something""")
    
    ###########################
    # download button
    df = pd.read_csv("data.csv")
    df = df.to_csv().encode("utf-8")
    st.download_button(label="Download data", 
                       data=df,
                       file_name="data.csv", mime="text/csv",
                       type="primary")
    #############################
    st.divider()

    st.subheader("About you")
    col1, col2 = grid_2col_1row(50)
    col1.markdown("Institution:")
    institution = col2.text_input("Institution:", key="institution", label_visibility="collapsed")
    col1, col2 = grid_2col_1row(50)
    col1.markdown("Has your institution piloted in basket LLM draft generation?")
    pilot = col2.toggle(label="Has your institution piloted in basket LLM draft generation?", value=False, label_visibility="collapsed", key="pilot")
    if pilot:
        col1, col2 = grid_2col_1row(100)
        col1.markdown("Role:")
        with col2:
            role_leader = st.checkbox("Health system leadership", key="role_leader")
            role_implementation = st.checkbox("Implementation team for LLM draft generation", key="role_implementation")
        col1, col2 = grid_2col_1row(50)
        col1.markdown("Years in current role:")
        role_y = col2.number_input("Years in current role:", key="role_y", value=None, label_visibility="collapsed")
        col1, col2 = grid_2col_1row(50)
        col1.markdown("We have halted use of LLM draft generation.")
        halt = col2.toggle(label="We have halted use of LLM draft generation", value=False, label_visibility="collapsed", key="halt")
        if st.session_state.halt:
            col1, col2 = grid_2col_1row(50)
            col1.markdown("Reason for halting:")
            halt_reason = col2.text_input("Reason for halting:", key="halt_reason", label_visibility="collapsed")

        # st.checkbox("My instutition has piloted in basket LLM draft generation")#, key="pilot")
        # st.multiselect("Role:", ["Health system leadership", "Implementation team for LLM draft generation"])
        # halt = st.checkbox("We have halted use of LLM draft generation", key="halt")

        st.divider()
        st.subheader("About your institution's LLM draft generation implementation")
        # sort of ranking
        # documentation: https://pypi.org/project/streamlit-sortables/
        # github: https://github.com/ohtaman/streamlit-sortables
        # st.write("Rank the following metrics you'd find most useful for assessing LLM draft generation:")
        original_metrics = [
            {'header': "Rank the following metrics you'd find most useful for assessing LLM draft generation. If you don't care about a metric, leave it in the 'I don't care about these' section below.",  
            'items': ['Utilization', 'EHR vendor-provided free text feedback', 'EHR vendor-provided quantitative feedback',
                        'Institutional survey', 'Performance on a set of challenging messages (e.g. "red teaming")', 
                        'Patient feedback', 'In basket volume', 'Burnout scores']},
            {'header': "I don't care about these:", 'items': ['Other']}
        ]
        sorted_metrics = sort_items(original_metrics, multi_containers=True, key="sorted_metrics", direction="vertical")
        if "Other" in sorted_metrics[0]["items"]:
            other_metric = st.text_input("Other:", placeholder="Please describe", key="other_metric")

        st.divider()
        st.subheader("ROI")
        # st.markdown("Pre- and post-implementation benefits:")
        # Financial benefits: increased billable visits
        # Financial benefits: increased messaging throughput/efficiency
        # Prestige: I expected implementing ART would improve external views of my institution. 
        # Message quality: I had high expectations for the quality of AI-generated draft messages prior to implementation
        # Workflow integration: I expected smooth integration of AI-generated draft messages into existing workflows 
        # Usability: I expected ART would facilitate an improved user interface for In Basket messaging 
        # Burden/burnout: I expected ART would reduce provider burden
        # Burden/burnout: I expected ART would reduce provider burnout
        # Patients: I expected ART would improve patient outcomes
        # Patients: I expected ART would improve patient satisfaction
        st.caption("Key: faces denote strongly disagree, disagree, neutral, agree, strongly agree")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("**Benefits:**")
        col2.markdown("**Expectations pre-implementation:**")
        col3.markdown("**Reality post-implementation:**")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Increased billable visits")
        ROI_billable_visits_pre = col2.feedback("faces", key="ROI_billable_visits_pre")
        ROI_billable_visits_post = col3.feedback("faces", key="ROI_billable_visits_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Increased messaging throughput/efficiency")
        ROI_messaging_pre = col2.feedback("faces", key="ROI_messaging_pre")
        ROI_messaging_post = col3.feedback("faces", key="ROI_messaging_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Prestige of my institution")
        ROI_prestige_pre = col2.feedback("faces", key="ROI_prestige_pre")
        ROI_prestige_post = col3.feedback("faces", key="ROI_prestige_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Message quality")
        ROI_quality_pre = col2.feedback("faces", key="ROI_quality_pre")
        ROI_quality_post = col3.feedback("faces", key="ROI_quality_post")
        col1, col2, col3 = grid_3col_1row(120)
        col1.markdown("Workflow integration")
        col1.caption("I expected smooth integration of AI-generated drafts into existing workflows.")
        ROI_workflow_pre = col2.feedback("faces", key="ROI_workflow_pre")
        ROI_workflow_post = col3.feedback("faces", key="ROI_workflow_post")
        col1, col2, col3 = grid_3col_1row(120)
        col1.markdown("Usability")
        col1.caption("I expected AI-generated drafts would facilitate an improved user interface for In Basket messaging.")
        ROI_usability_pre = col2.feedback("faces", key="ROI_usability_pre")
        ROI_usability_post = col3.feedback("faces", key="ROI_usability_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Reduce provider burden")
        ROI_burden_pre = col2.feedback("faces", key="ROI_burden_pre")
        ROI_burden_post = col3.feedback("faces", key="ROI_burden_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Reduce provider burnout")
        ROI_burnout_pre = col2.feedback("faces", key="ROI_burnout_pre")
        ROI_burnout_post = col3.feedback("faces", key="ROI_burnout_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Improve patient outcomes")
        ROI_outcomes_pre = col2.feedback("faces", key="ROI_outcomes_pre")
        ROI_outcomes_post = col3.feedback("faces", key="ROI_outcomes_post")
        col1, col2, col3 = grid_3col_1row(50)
        col1.markdown("Improve patient satisfaction")
        ROI_satisfaction_pre = col2.feedback("faces", key="ROI_satisfaction_pre")
        ROI_satisfaction_post = col3.feedback("faces", key="ROI_satisfaction_post")
        
        # thumbs = st.feedback("thumbs")
        # faces = st.feedback("faces")
        # stars = st.feedback("stars")
        likert = st.select_slider(label="Another way to show Likert scale but probably less discrete/intuitive:",
            options=["strongly disagree","disagree","ambivalent","agree","strongly agree"], 
            value="ambivalent")

        st.divider()
        st.subheader("Future directions")
        col1, col2 = grid_2col_1row(80)
        col1.write("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?")
        with col2:
            invest1 = st.radio("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
                ["increase", "maintain", "reduce"], index=None, label_visibility="collapsed")
        # invest2 = st.selectbox("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
        #             ["increase", "maintain", "reduce"], index=None)
        # invest3 = st.select_slider("After piloting LLM draft generation at your institution, do you plan to increase, maintain, or reduce investment into LLM draft generation?",
        #                 options=["reduce", "maintain", "increase"], value="maintain")

    
    
    
    
    ##########################################################################################################
    st.divider()
    
    st.subheader("Troubleshooting")
    # if st.session_state.institution="1K3A"
        # wrap in fragment to prevent app from rerunning when someone clicks this
        # https://docs.streamlit.io/develop/concepts/architecture/fragments
    with st.form(key="form"):
        df_row = [institution, pilot, role_leader, role_implementation, halt, halt_reason, 
                    # sorted_metrics[0]["items"], 
                    other_metric, 
                    faces, likert, 
                    invest1]
        st.session_state.data = df_row
        st.form_submit_button(label="Submit", on_click=submitted)
    df = pd.DataFrame([df_row], columns=["institution", "pilot", "role_leader", "role_implementation", 
                                        "halt", "halt_reason",
                                        #  "sorted_metrics", 
                                        "other_metric", "faces", "likert",
                                        "invest1"])
    st.dataframe(df)
    df = pd.concat([pd.DataFrame([df_row], columns=df.columns), df], ignore_index=True)
    
    st.divider()
    st.write("st.session_state.submitted: ", st.session_state.submitted)
    institution
    pilot
    role_leader
    role_implementation
    halt
    halt_reason
    # sorted_metrics[0]["items"]
    other_metric
    faces
    likert
    invest1