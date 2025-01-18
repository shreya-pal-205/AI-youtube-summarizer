from http.client import responses

import streamlit as st
import google.generativeai as genai
import os

from click import prompt
from youtube_transcript_api import YouTubeTranscriptApi



# Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDOmZ6Tlt3XAZwRgqP5Jd2a5X3KmbZVBW0"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])







# custom funtions
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')


def extract_transcript_details(youtube_video_url):
    video_id = youtube_video_url.split('=')[-1]
    transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

    t = ""
    for i in transcript_text:
        t += " " + i["text"]

    return t



def generate_video_summary(transcript_text):
    prompt = """You are youtube video summarizer. You will be taking the transcript text and summarize the entire video and provide the summary in points within 200 words. The transcript text will be appended here:"""
    response = model.generate_content([transcript_text,prompt])
    return response.text


def generate_video_questions(transcript_text):
    prompt = f"""You are an AI assistant helping the user generate a question and a corresponding answer based on the following text:
    '{transcript_text}'.Generate 5 questions.And also write problem number.Each problem should have:
    - A clear question
    - The correct answer clearly indicated
    Format:
    ## Problem
    Question: [Question]
    Answer: [Answer] """
    response = model.generate_content([transcript_text,prompt])
    return response.text





# app create==============
st.title("Image to Text Extractor & Generator")
st.write("Upload an image and get details about it.")

youtube_link = st.text_input("Enter youtuve video url:")

if youtube_link:
    video_id = youtube_link.split('=')[-1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=500)

if st.button("Generate Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_video_summary(transcript_text)
        st.write(summary)

if st.button("Generate Questions"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        questions = generate_video_questions(transcript_text)
        for ques in questions.split("## Problem"):
            if ques.strip():
                st.write(ques.split('Answer:')[0].strip())
                st.write("Answers:",ques.split('Answer:')[1].strip())





