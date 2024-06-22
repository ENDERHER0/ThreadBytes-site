import os
from pytube import YouTube
from moviepy.editor import *
#Ask User for youtube url
url = input("Input URL: ")
fileName = input("Name for clip file: ")
videoMaxLength = float(input("Time in seconds for clip max length: "))
if not os.path.exists(fileName):os.mkdir("YoutubeDownloads/" + fileName)
yt = YouTube(url)
#format
mp4_files = yt.streams.filter(file_extension="mp4")
print("Format: MP4")
mp4_720p_files = mp4_files.get_by_resolution("720p")
print("Resolution: 720p")
latestDownload = mp4_720p_files.download("YoutubeDownloads")
#Get video ready for cutting
clip = VideoFileClip(latestDownload)
audio = AudioFileClip(latestDownload)
duration = float(clip.duration)
print("Duration: " + str(duration))
clipMaxDuration = videoMaxLength
clipDuration = 0
cut = 0
#Cut the video if its longer than 65 seconds
while(duration >= clipMaxDuration) :
    if(duration < videoMaxLength*2) & (duration > videoMaxLength):
        cut += 1
        extraCut = int(duration)
        break
    duration -= clipMaxDuration
    cut += 1 
print("Total Clips: " + str(cut))
print("Extra Video: " + str(extraCut))
#Cut and Save each clip
for i in range(cut):
    newClip = clip
    newAudio = audio
    print("Cutting Video")
    if(i < cut - 1) :
        newClip = newClip.subclip(clipDuration, clipMaxDuration)
        newAudio = newAudio.subclip(clipDuration, clipMaxDuration)
        newAudio.cutout(newClip.duration, newAudio.duration)
    else:
        newClip = newClip.subclip(clipDuration, clipDuration + extraCut)
        newAudio = newAudio.subclip(clipDuration, clipDuration + extraCut)
        newAudio.cutout(extraCut, newAudio.duration)
    newClip.write_videofile("YoutubeDownloads/" + fileName + "/Clip_" + str(i + 1) + ".mp4")
    print("Video: " + str(i + 1) + " Saved")
    clipDuration += videoMaxLength
    clipMaxDuration += videoMaxLength
input("Process Completed")






def create_window():
    root = tk.Tk()
    root.title("ClipCut")

    root.geometry("600x300")  # Reduced height
    root.configure(bg="black")
    root.configure(padx=20, pady=20)

    font_style = ("Arial", 12)

    title_label = tk.Label(root, text="ClipCut", font=("Arial", 20, "bold"), fg="white", bg="black")
    title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2, sticky="n")

    url_label = tk.Label(root, text="YouTube URL:", font=font_style, fg="white", bg="black")
    url_label.grid(row=1, column=0, pady=5, sticky="w")
    url_entry = tk.Entry(root, font=font_style, width=40)
    url_entry.grid(row=1, column=1, pady=5, sticky="w")

    fileName_label = tk.Label(root, text="File Name:", font=font_style, fg="white", bg="black")
    fileName_label.grid(row=2, column=0, pady=5, sticky="w")
    fileName_entry = tk.Entry(root, font=font_style, width=20)
    fileName_entry.grid(row=2, column=1, pady=5, sticky="w")

    videoMaxLength_label = tk.Label(root, text="Video Max Length (seconds):", font=font_style, fg="white", bg="black")
    videoMaxLength_label.grid(row=3, column=0, pady=5, sticky="w")
    videoMaxLength_var = tk.StringVar(value="60")
    videoMaxLength_entry = tk.Spinbox(root, from_=1, to=float('inf'), textvariable=videoMaxLength_var, font=font_style, width=10)
    videoMaxLength_entry.grid(row=3, column=1, pady=5, sticky="w")

    download_button = tk.Button(root, text="Download and Cut Video", command=download_and_cut, font=font_style)
    download_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="n")

    progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
    progress_bar.grid(row=5, column=0, columnspan=2, pady=10, sticky="n")

    root.mainloop()