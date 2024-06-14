from chat_downloader import ChatDownloader
from youtube_transcript_api import YouTubeTranscriptApi
import scrapetube
import datetime
from deepmultilingualpunctuation import PunctuationModel
# # https://chat-downloader.readthedocs.io/en/latest/items.html

url = 'https://www.youtube.com/watch?v=yRlnHVHE18k'
url_id = url.split('=')[1]

transcript_data = list(YouTubeTranscriptApi.get_transcript(url_id))

#set max delay to number of seconds between time updates
max_delay = 0
i = 0

sentences = []
current_sentence = ''
last_times = (0, 0)

while i < len(transcript_data):
    if last_times[1] == 0:
        last_times = (last_times[0], last_times[1] + transcript_data[i]['duration'])
        current_sentence += transcript_data[i]['text']
        continue

    current_start = transcript_data[i]['start']
    current_end = current_start + transcript_data[i]['duration']

    if current_start - last_times[0] <= max_delay:
        last_times = (last_times[0], current_end)
        current_sentence += ' ' + transcript_data[i]['text']
    else:
        # print(str(datetime.timedelta(seconds=last_times[0])))
        sentences.append([str(datetime.timedelta(seconds=last_times[0])), current_sentence])
        current_sentence = transcript_data[i]['text']
        last_times = (current_start, current_end)


    i += 1

sentences.append([str(datetime.timedelta(seconds=last_times[0])), current_sentence])

file = open("captions/captions.txt","w") 
punct_model = PunctuationModel()
for i in range(len(sentences)):
    new_text = punct_model.restore_punctuation(sentences[i][1])
    file.write(sentences[i][0] + " " + str(new_text) + "\n")
file.close()