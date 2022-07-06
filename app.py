import youtube_transcript_api
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, abort
import pickle
from flask import request
import nltk
nltk.download('punkt')
# from datetime

# define a variable to hold you app
app = Flask(__name__)
model = pipeline("summarization")

def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    script = ""
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "
        
    return script

def summarize_transcripts(transcript):
    #use transformers model to summarize transcript
    #if transcript is big, then divide it in 1000-1000 words sentences
    num_iters = int(len(transcript) / 1000)
    summary_text = []
    for i in range(0,num_iters+1):
        start = 0
        start = i * 1000
        end = (i+1) * 1000
        out = model(transcript[start:end],min_length=20,max_length=40)[0]['summary_text']
        summary_text.append(out)
    return " ".join(summary_text)


def handle_bad_request(e):
    return 'bad request! Video Url is missing in the request', 400

def handle_missing_video_id(e):
    return 'bad request! The video has no id/ video is not youtube video',400

# define your resource endpoints
@app.route('/')
def index_page():
    return "Hello world"

@app.errorhandler(400)
def bad_request(e):
    # note that we set the 404 status explicitly
    return 'bad request! Video Url/ Video Id is missing in the request', 400

@app.route('/api/summarize', methods=['GET'])
def fetch_summary():
     video_url = request.args.get("youtube_url")
     if not video_url:
         abort(400)
     video_id = ""
     if video_url:
         video_url_content = video_url.split("=")
         if len(video_url_content) > 1:
             video_id = video_url_content[1]
     if not video_id:
         abort(400)
     transcript = generate_transcript(video_id)
     #  nested_sentences = generate_sentences(mySentence)
     #  print(nested_sentences)
     summary = summarize_transcripts(transcript)
     #  summary = concat_summaries(summaries)
     return summary


# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)

# def generate_sentences(longText):
#     nested = []
#     sent = []
#     length = 0
#     sentences = nltk.sent_tokenize(text=longText)
#     print(len(sentences),sentences)
#     for sentence in sentences:
#         print(sentence)
#         length += len(sentence)
#         if length < 1024:
#             sent.append(sentence)
#         else:
#             nested.append(sent)
#             sent = []
#             length = 0
#     return nested