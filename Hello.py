# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import streamlit as st
from streamlit.logger import get_logger
from utils import GetSharepointSpread, VersionInfo, get_sharepoint_df
import hmac

LOGGER = get_logger(__name__)

# @st.cache_resource()
def get_sharepoint_spreadsheets():
    with st.spinner("Refreshing Data..."):
        msg1, df1 = GetSharepointSpread(
            st.secrets.urls.url1,
            st.secrets.sharepoint_credentials.uname,
            st.secrets.sharepoint_credentials.pwd,
        )
        st.toast(msg1)

        msg2, df2 = GetSharepointSpread(
            st.secrets.urls.url2,
            st.secrets.sharepoint_credentials.uname,
            st.secrets.sharepoint_credentials.pwd,
        )
        st.toast(msg2)

        # if (df1 is not None) or (df2 is not None):
        #     st.session_state.df_list = [df1, df2]
        return df1,df2


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Login"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        get_sharepoint_spreadsheets()
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


def run_dashboard():
    #get_sharepoint_spreadsheets()
    # u_df, p_df = 0,1
    u_df, p_df = get_sharepoint_spreadsheets()
    df_dict = {"Current Info": p_df, "Historical Info (UB only)": u_df}
    sel = st.selectbox("Select Data to View: ", options=df_dict.keys(), index=0)

    st.title(f"{sel} Lookup")
    # df_select = st.session_state.df_list[df_dict[sel]]
    df_select = df_dict[sel]

    ## SIDEBAR
    # Sidebar Configuration
    st.sidebar.image(
        "https://www.logolynx.com/images/logolynx/4f/4f42c461be2388aca949521bbb6a64f1.gif",
        width=200,
    )
    st.sidebar.markdown(f"# {sel} Lookup")
    st.sidebar.markdown(f"{sel} by Department and Date")
    st.sidebar.markdown("---")
    st.sidebar.button("Refresh", on_click=get_sharepoint_spreadsheets)

    st.write(df_select)


if check_password():
    run_dashboard()
else:
    st.stop()


