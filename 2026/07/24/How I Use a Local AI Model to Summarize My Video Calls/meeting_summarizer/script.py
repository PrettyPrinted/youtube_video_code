import os
import subprocess

from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

MEETINGS_DIR = "/mnt/d/Meetings"

def main():
    while True:
        contents = os.listdir(MEETINGS_DIR)
        if contents:
            extension = contents[0].split(".")[-1:][0]
            if extension in ["mp4", "mkv"]:
                process_meeting(contents[0])
                break

def process_meeting(filename):
    print(f"Processing {filename}...")
    filename_prefix = filename.split(".")[0]
    print("Creating wav file...")
    result = subprocess.run(["ffmpeg", "-i", f"{os.path.join(MEETINGS_DIR, filename)}", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", f"{filename_prefix}_audio.wav"], capture_output=True, text=True)

    print("Generating transcript...")
    result = subprocess.run(["/home/anthony/whisper.cpp/build/bin/whisper-cli", "-f", f"/home/anthony/meeting_summarizer/{filename_prefix}_audio.wav"], cwd="/home/anthony/whisper.cpp", capture_output=True, text=True)
    transcript = result.stdout

    

    print("Saving transcript...")
    with open(f"{filename_prefix}_transcript.txt", "w") as f:
        f.write(transcript)
    print(result.stderr)
    with open(f"{filename_prefix}_transcript.txt", "r") as f:
        transcript = f.read()
    summarize(transcript, filename_prefix)

    # move files to processed directory

def summarize(transcript, filename_prefix):
    print("Summarizing transcript...")
    agent = Agent(  
    'openai-responses:gpt-5.4-mini-2026-03-17',  
        instructions=(  
            '''summarize the following meeting transcript and give me the action items'''
        ),
    )

    result = agent.run_sync(transcript)

    print("Saving summary...")
    with open(f"{filename_prefix}_summary.txt", "w") as f:
        f.write(result.output)


if __name__ == "__main__":
    main()
