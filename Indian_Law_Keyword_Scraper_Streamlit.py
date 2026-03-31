import os
import streamlit as st
import requests
from bs4 import BeautifulSoup

# ================= KEYWORDS =================
KEYWORDS = [
    "governing law", "jurisdiction", "applicable law", 
    "laws of", "subject to the laws of", "under the laws of", "this agreement shall be governed", 
    "this agreement is governed", "venue shall be", "exclusive jurisdiction", "disputes shall be resolved", 
    "governed and construed", "laws and regulations of", "legal jurisdiction", "law of the state", "courts of", 
    "this contract shall be governed by", "shall be construed in accordance with", "exclusive venue for any dispute", 
    "subject to exclusive jurisdiction", "submitted to the jurisdiction of", "in accordance with the laws of", 
    "will be interpreted under the laws of", "controlled by the laws of", "adjudicated in the courts of", 
    "enforced under the laws of", "resolved under the laws of", "governed exclusively by", "governing jurisdiction", 
    "choice of law", "forum selection", "legal venue", "place of jurisdiction", "litigation must be filed in", 
    "laws that govern this agreement", "resolution under applicable laws", "disputes will be governed", 
    "will be tried in the courts of", "subject to the courts of", "interpretation shall follow the laws of", 
    "all disputes arising out of", "under the exclusive jurisdiction", "any claim shall be brought in", 
    "regulated by the laws of", "competent courts of", "Indian Law", "Indian Law","Indian Laws","governing laws",
    "applicable laws","law of","subject to the law of","under the law of","dispute shall be resolved",
    "governed by","law and regulation of","laws of the state","laws of the states","court of",
    "exclusive venue for any disputes","in accordance with the law of","will be interpreted under the law of",
    "controlled by the law of","adjudicated in the court of","enforced under the law of","resolved under the law of",
    "choice of laws","litigation should be filed in","litigation to be filed in","litigation has to be filed in",
    "law that govern this agreement","law that governs this agreement","Dispute resolution under Indian laws",
    "Dispute resolution under Indian law","Laws in India","Law in India","Laws of India","Law of India","Laws followed in India",
    "Law followed in India","governed by the law of India","governed by the laws of India","governed by"
]

# ================= NORMALIZE =================
def normalize(text):
    return " ".join(text.lower().split())

# ================= FETCH PAGE DATA =================
def get_page_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ")

        return normalize(text)

    except Exception as e:
        return ""

# ================= KEYWORD MATCH =================
def extract_keywords(page_text):
    found = []
    for kw in KEYWORDS:
        if normalize(kw) in page_text:
            found.append(kw)
    return list(dict.fromkeys(found))

# ================= STREAMLIT UI =================
st.set_page_config(page_title="ILKEY Page Checker", layout="centered")

st.title("🔍 ILKEY Keyword Checker (Page Content Only)")

url = st.text_input("Enter website URL")

check = st.button("Check")

if check:

    if not url:
        st.error("Please enter a URL")

    else:

        with st.spinner("Reading page content..."):

            page_text = get_page_text(url)

        keywords_found = extract_keywords(page_text)

        if keywords_found:
            st.code(str(keywords_found), language="python")
        else:
            st.code("No ILKEY found in this page")
