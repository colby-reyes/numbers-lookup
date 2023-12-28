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

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import io
import pandas as pd
from dataclasses import dataclass
import streamlit as st
import os

@dataclass
class VersionInfo:
    version = "1.0.0"
    description = """`Numbers Lookup` version 1.0.0"""

def get_sharepoint_df(
        # sheetname: str,
        username: str,
        password: str,
        url: str,
):
    # authenticate
    ctx_auth = AuthenticationContext(url)
    if ctx_auth.acquire_token_for_user(username, password):
        ctx = ClientContext(url, ctx_auth)
        # web = ctx.web
        # ctx.load(web)
        ctx.execute_query()
        print("Authentication successful")

    response = File.open_binary(ctx, url)

    # %% save data to BytesIO stream
    bytes_file_obj = io.BytesIO()
    bytes_file_obj.write(response.content)
    bytes_file_obj.seek(0)  # set file object to start

    # %% read excel file and each sheet into pandas dataframe
    df = pd.read_excel(bytes_file_obj)#, sheet_name=sheetname)

    # return sharepoint_df
    return df

@st.cache_resource(show_spinner=False)
def GetSharepointSpread(
    url: str,
    username: str,
    password: str,
):
    try:
        ctx_auth = AuthenticationContext(url)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(url, ctx_auth)
            # web = ctx.web
            # ctx.load(web)
            ctx.execute_query()
            # st.toast("Authentication successful")

        response = File.open_binary(ctx, url)
        print("Authentication successful")
        st.toast("`reponse` successful")

        # %% save data to BytesIO stream
        bytes_file_obj = io.BytesIO()
        st.toast("`bytes_file_obj` call successful")
        bytes_file_obj.write(response.content)
        st.toast("write `bytes_file_obj` to context successful")
        bytes_file_obj.seek(0)  # set file object to start
        st.toast("set file object to start successful")

        # %% read excel file and each sheet into pandas dataframe
        df = pd.read_excel(bytes_file_obj)  # , sheet_name=sheetname)
        return ("Authentication Successful",df)
    except Exception as e:
        return (f"Error: {e}",None)