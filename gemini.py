import os
import google.generativeai as genai
import subprocess

os.environ["API_KEY"] = "AIzaSyDhhr2yw8ZbQi79NI06DNyam39ZAPo1w4w"

genai.configure(api_key=os.environ["API_KEY"])
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel('gemini-1.5-flash')

with open("captions/captions.txt", 'r') as file:
    file_content = file.read()
 
response = model.generate_content("What are the most interesting clip times from this following transcript?" + file_content + '\n Answer using the following JSON schema: Clip = {"start_time": time, "transcribed_text": str, "end_time": time} \n Since each clip may be longer than the data given for each time stamp, combine a continuous clip into one entry')

with open("output.txt", "w") as output_f:
    output_f.write(str(response))