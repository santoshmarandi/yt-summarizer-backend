from http.server import BaseHTTPRequestHandler
import json, os, requests
from youtube_transcript_api import YouTubeTranscriptApi

GEMINI_KEY = os.environ.get("AIzaSyBZssPgpTsXPRuM1raxq2USMS5bYcJGLMo")

def extract_video_id(url):
    if "v=" in url:
            return url.split("v=")[1].split("&")[0]
                if "youtu.be/" in url:
                        return url.split("youtu.be/")[1].split("?")[0]
                            return None

                            def fetch_transcript(video_id):
                                try:
                                        data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','hi'])
                                                return " ".join([p['text'] for p in data])
                                                    except:
                                                            return None

                                                            def call_gemini(prompt):
                                                                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
                                                                    params = {"key": GEMINI_KEY}
                                                                        headers = {"Content-Type": "application/json"}
                                                                            body = {"contents":[{"parts":[{"text": prompt}]}]}
                                                                                resp = requests.post(url, params=params, headers=headers, json=body)
                                                                                    return resp.json()

                                                                                    class handler(BaseHTTPRequestHandler):
                                                                                        def do_POST(self):
                                                                                                content_length = int(self.headers['Content-Length'])
                                                                                                        body = self.rfile.read(content_length)
                                                                                                                data = json.loads(body)

                                                                                                                        url = data.get("url")
                                                                                                                                command = data.get("command", {})

                                                                                                                                        vid = extract_video_id(url)
                                                                                                                                                if not vid:
                                                                                                                                                            self.send_response(400)
                                                                                                                                                                        self.send_header("Content-type", "application/json")
                                                                                                                                                                                    self.end_headers()
                                                                                                                                                                                                self.wfile.write(json.dumps({"error":"Invalid URL"}).encode())
                                                                                                                                                                                                            return

                                                                                                                                                                                                                    transcript = fetch_transcript(vid) or "Transcript not available."
                                                                                                                                                                                                                            prompt = f"""
                                                                                                                                                                                                                                    Summarize this transcript with command:
                                                                                                                                                                                                                                            {json.dumps(command)}
                                                                                                                                                                                                                                                    Transcript:
                                                                                                                                                                                                                                                            {transcript}
                                                                                                                                                                                                                                                                    Return JSON with: title, headings, bullets, timestamps, keywords, quiz.
                                                                                                                                                                                                                                                                            """

                                                                                                                                                                                                                                                                                    result = call_gemini(prompt)

                                                                                                                                                                                                                                                                                            self.send_response(200)
                                                                                                                                                                                                                                                                                                    self.send_header("Content-type", "application/json")
                                                                                                                                                                                                                                                                                                            self.end_headers()
                                                                                                                                                                                                                                                                                                                    self.wfile.write(json.dumps(result).encode())