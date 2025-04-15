import os, requests, boto3
from moviepy import *


def create_video(test, directory_name, video_name):
    directory_name = 'downloads'
    local_filename = f"{directory_name}/sample.mp4"
    intro = VideoFileClip(f'{directory_name}/intro investo.mov', has_mask=True)
    slide = VideoFileClip(f'{directory_name}/investocracy transition.mov', has_mask=True)
    gap = ColorClip(size=intro.size, color=(0, 0, 0), duration=4)
    clips = []
    durations = []
    print(f"downloading {local_filename}")
    response = requests.get(test["intro"]["CNBCVideo"]["url"], stream=True)
    response.raise_for_status()  # Check for HTTP errors
    with open(local_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
            file.write(chunk)
    cnbc = VideoFileClip(local_filename)
    cnbc_resized = cnbc.resized(height=1080)  # Scale proportionally by height

    # Pad with black bars to reach exactly 1920x1080
    cnbc_final = cnbc_resized.with_on_color(
        size=(1920, 1080),
        color=(0, 0, 0),
        pos=("center", "center")
    )
    clips.append(cnbc_final)
    durations.append(cnbc_final.duration)
    footages =  []
    for i , footage in enumerate(test["intro"]["footages"]):
        local_filename = f"{directory_name}/intro{i}.mp4"
        print(f"downloading {local_filename}")
        url = footage["url"]
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                file.write(chunk)
        duration = footage["pause_duration"]
        clip = VideoFileClip(local_filename).without_audio().with_duration(duration)
        clip_resized = clip.resized(height=1080)

        clip_final = clip_resized.with_on_color(
            size=(1920, 1080),
            color=(0, 0, 0),
            pos=("center", "center")
        )

        footages.append(clip_final)
    url = test["intro"]["audio_path"]
    local_filename = f"{directory_name}/audio{i}.mp3"
    response = requests.get(url, stream=True) 
    response.raise_for_status()  
    with open(local_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):  
            file.write(chunk)
    audio = AudioFileClip(local_filename)
    new_footage = concatenate_videoclips(footages)
    new_footage_with_audio = new_footage.with_audio(audio)
    clips.append(new_footage_with_audio)
    last_value = durations[-1]
    new = last_value + new_footage.duration
    durations.append(new)
    intro_length = len(durations) -1


    last_value = durations[-1]
    new = last_value + 4
    durations.append(new)
    clips.append(gap)

    for i, item in enumerate(test["content"]):
        # Handle CNBCVideo URL
        local_filename = f"{directory_name}/cnbc{i}.mp4"
        if "CNBCVideo" in item and "url" in item["CNBCVideo"]:
            url = item["CNBCVideo"]["url"]
            print(f"downloading {local_filename}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                    file.write(chunk)
            clip = VideoFileClip(local_filename)
            clip_resized = clip.resized(height=1080)
            clip_final = clip_resized.with_on_color(
                size=(1920, 1080),
                color=(0, 0, 0),
                pos=("center", "center")
            )
            duration = item["CNBCVideo"]["pause_duration"]
            if durations:
                last_value = durations[-1]
                new = last_value + duration
            else:
                new = duration
            durations.append(new)  
            clips.append(clip_final)
            footages =  []
        for j, footage in enumerate(item.get("footages", [])):
            local_filename = f"{directory_name}/{i}footage{j}.mp4"
            if "url" in footage:
                url = footage["url"]
                print(f"downloading {local_filename}")
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Check for HTTP errors
                with open(local_filename, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                        file.write(chunk)
                duration = footage["pause_duration"]
                clip = VideoFileClip(local_filename).without_audio().with_duration(duration)
                clip_resized = clip.resized(height=1080)
                clip_final = clip_resized.with_on_color(
                    size=(1920, 1080),
                    color=(0, 0, 0),
                    pos=("center", "center")
                )
                footages.append(clip_final)
        new_footage = concatenate_videoclips(footages)
        url = item["audio_path"]
        local_filename = f"{directory_name}/audio{i}.mp3"
        response = requests.get(url, stream=True) 
        response.raise_for_status()  
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)
        audio = AudioFileClip(local_filename)
        new_footage_with_audio = new_footage.with_audio(audio)
        clips.append(new_footage_with_audio)
        last_value = durations[-1]
        new = last_value + new_footage.duration
        durations.append(new)

    last_footage = len(clips) -1
    combined_video = concatenate_videoclips(clips)  
    transition_list = []
    for i , duration in enumerate(durations):
        if i == intro_length:
            transition = intro.with_start(durations[i] -1)
        elif i == intro_length + 1 or i == last_footage:
            continue
        else:
            transition = slide.with_start(durations[i] - 1)
        transition_list.append(transition)
    # Concatenate all video clips
    final_video = CompositeVideoClip([combined_video] + transition_list).with_effects([vfx.CrossFadeIn(0.2)])
    # Export the final video
    final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
    path = upload_to_s3(f"output.mp4", f"Investocracy/{video_name}.mp4")
    return path
def upload_to_s3(file_path, s3_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_path,
                       ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded {file_path} to S3 bucket.")
        return s3_path
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {str(e)}")