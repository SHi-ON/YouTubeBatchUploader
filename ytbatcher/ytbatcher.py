import os
import time

from moviepy.editor import VideoFileClip, concatenate_videoclips

EXTENSIONS = ['.mp4', '.mov', '.mkv', '.3gp', '.avi', '.wmv', '.flv']
LOG_FILENAME = 'batched_videos.txt'


def extract_video_paths():
    paths = os.listdir('video_files')
    return [p for p in paths for e in EXTENSIONS if e in p.lower()]


def merge_videos(aggregate_clips, aggregate_names):
    handle = open(LOG_FILENAME, 'a')
    for i in range(len(aggregate_clips)):
        render = concatenate_videoclips(aggregate_clips[i])
        filename = 'video_' + str(i) + '.mp4'
        render.write_videofile(filename, codec='libx264')

        log_filenames = '\n'.join(aggregate_names[i])
        handle.write('Merged in video_' + str(i) + ': \n' + log_filenames + '\n')
    handle.close()
    print("Videos generated successfully.")


def aggregate_videos():
    current_dir = os.getcwd()
    video_paths = extract_video_paths()

    clips_aggregated = list()
    names_aggregated = list()
    clips = list()
    names = list()
    clips_dur = 0
    for video in video_paths:
        file_path = os.path.join(current_dir, 'video_files', video)
        clip = VideoFileClip(file_path)
        if clips_dur < 3600:
            clips.append(clip)
            names.append(video)
            clips_dur += clip.duration
        else:
            clips_aggregated.append(clips)
            names_aggregated.append(names)
            clips = list()
            names = list()
            clips_dur = 0
    if clips_dur != 0:
        clips_aggregated.append(clips)
        names_aggregated.append(names)
    return clips_aggregated, names_aggregated


def upload_video():
    current_dir = os.getcwd()
    video_paths = extract_video_paths()
    for video in video_paths:
        file_path = os.path.join(current_dir, 'video_files', video)
        # file_title = os.path.splitext(video)[0]
        upload_params = 'python ytbatcher/upload_video.py --file="' + file_path + '" --title=' + '"' + video + '"'
        print("---------------start uploading " + file_path + "---------------")
        os.system(upload_params)
        time.sleep(3)


if __name__ == '__main__':
    upload_video()
    # agg_clips, agg_names = aggregate_videos()
    # merge_videos(agg_clips, agg_names)

