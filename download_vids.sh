#!/bin/bash

# Check if the required arguments are provided
if [ $# -ne 4 ]; then
    echo "Usage: $0 <video_url> <start_time> <duration> <output_file>"
    exit 1
fi

video_url=$1
start_time=$2
duration=$3
output_file=$4

# Get the available formats for the video
formats=$(youtube-dl -F "$video_url")

# Extract the format code for the best video-only version in mp4 format
video_format_code=$(echo "$formats" | awk '/video only/ && /mp4/ {print $1}' | tail -1)

# Extract the format code for the best audio-only version based on quality priority
audio_format_code=$(echo "$formats" | awk '/audio only/ && /m4a/ {print $1}' | head -1)

echo "$video_format_code"
echo "$audio_format_code"

# Download the video-only version for the specified time frame
video_download() {
    youtube-dl -g "$video_url" -f "$video_format_code" | xargs -I{} ffmpeg -ss "$start_time" -i "{}" -c copy -t "$duration" "video.mp4"
}

audio_download() {
    youtube-dl -g "$video_url" -f "$audio_format_code" | xargs -I{} ffmpeg -ss "$start_time" -i "{}" -c copy -t "$duration" -vn -acodec copy "audio.aac"
}

video_download &
video_pid=$!

audio_download &
audio_pid=$!

# Wait for both downloads to complete
wait $video_pid $audio_pid


# Combine the video and audio
# ffmpeg -i "video.mp4" -i "audio.m4a" -c copy "$output_file"
ffmpeg -i "video.mp4" -i "audio.aac" -c copy "$output_file" -y

# Clean up the temporary files
rm "video.mp4" "audio.aac"

echo "Video clip downloaded and saved as $output_file"