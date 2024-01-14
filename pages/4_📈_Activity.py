import streamlit as st
import pandas as pd
import numpy as np

st.title("Activity")  

st.write("#### Weekly Activity")
if 'chart_data1' not in st.session_state:
    st.session_state.chart_data1 = pd.DataFrame({
            "Days": [1, 2, 3, 4, 5, 6, 7],
            "Activity Time (hours)": np.random.choice(range(1,4), 7)
        }
    )

st.area_chart(st.session_state.chart_data1, x = "Days", y = "Activity Time (hours)")

st.write("#### Monthly Activity")
if 'chart_data2' not in st.session_state:
    st.session_state.chart_data2 = pd.DataFrame({
            "Days": np.arange(1, 31, 1),
            "Activity Time (hours)": np.random.choice(range(1,4), 30)
        }
    )

st.line_chart(st.session_state.chart_data2, x = "Days", y = "Activity Time (hours)")