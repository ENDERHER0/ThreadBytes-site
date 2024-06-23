import tkinter as tk
import os
from tkinter import messagebox, ttk

from moviepy.editor import *
from pytube import YouTube


class ClipCutApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Set window size, background color, and padding
        self.master.geometry("600x300")  # Reduced height
        self.master.configure(bg="black")
        self.master.configure(padx=20, pady=20)

        # Set font style
        font_style = ("Arial", 12)

        # Create and place elements using grid
        title_label = tk.Label(self.master, text="ClipCut", font=("Arial", 20, "bold"), fg="white", bg="black")
        title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2, sticky="n")

        url_label = tk.Label(self.master, text="YouTube URL:", font=font_style, fg="white", bg="black")
        url_label.grid(row=1, column=0, pady=5, sticky="w")
        self.url_entry = tk.Entry(self.master, font=font_style, width=40)  # Wider text box
        self.url_entry.grid(row=1, column=1, pady=5, sticky="w")

        fileName_label = tk.Label(self.master, text="File Name:", font=font_style, fg="white", bg="black")
        fileName_label.grid(row=2, column=0, pady=5, sticky="w")
        self.fileName_entry = tk.Entry(self.master, font=font_style, width=20)  # Shorter text box
        self.fileName_entry.grid(row=2, column=1, pady=5, sticky="w")

        videoMaxLength_label = tk.Label(self.master, text="Video Max Length (seconds):", font=font_style, fg="white",
                                        bg="black")
        videoMaxLength_label.grid(row=3, column=0, pady=5, sticky="w")
        self.videoMaxLength_var = tk.StringVar(value="60")  # Default value
        videoMaxLength_entry = tk.Spinbox(self.master, from_=1, to=float('inf'), textvariable=self.videoMaxLength_var,
                                          font=font_style, width=10)  # No maximum limit
        videoMaxLength_entry.grid(row=3, column=1, pady=5, sticky="w")

        download_button = tk.Button(self.master, text="Download and Cut Video", command=self.download_and_cut,
                                    font=font_style)
        download_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="n")

        # Create a single progress bar
        self.progress_bar = ttk.Progressbar(self.master, length=500, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=2, pady=10, sticky="n")

    def download_and_cut(self):
        url = self.url_entry.get()
        fileName = self.fileName_entry.get()
        parentDirector = ""
        videoMaxLength = float(self.videoMaxLength_var.get())

        try:
            if not os.path.exists(fileName):
                os.makedirs("YoutubeDownloads/" + fileName)

            yt = YouTube(url)
            mp4Stream = yt.streams.filter(file_extension="mp4", res="720p").first()
            print("Format: MP4")
            print("Resolution: 720p")
            latestDownload = mp4Stream.download(output_path="YoutubeDownloads")

            clip = VideoFileClip(latestDownload)
            audio = AudioFileClip(latestDownload)

            duration = float(clip.duration)
            print("Duration: " + str(duration))

            clipMaxDuration = videoMaxLength
            clipDuration = 0
            cut = 0
            extraCut = 0

            while duration >= clipMaxDuration:
                if videoMaxLength * 2 > duration > videoMaxLength:
                    cut += 1
                    extraCut = int(duration)
                    break
                duration -= clipMaxDuration
                cut += 1

            print("Total Clips: " + str(cut))
            print("Extra Video: " + str(extraCut))

            # Create progress bar for both download and cut
            self.progress_bar["maximum"] = 100
            self.progress_bar["value"] = 0
            self.master.update()

            for i in range(cut):
                newClip = clip
                newAudio = audio

                print("Cutting Video")

                if i < cut - 1:
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

                # Update progress bar
                self.progress_bar["value"] = (i + 1) * (100 / cut)
                self.master.update()

            messagebox.showinfo("Process Completed", "Videos downloaded and cut successfully.")
            self.progress_bar["value"] = 0

            # Reset input values after process completion
            self.reset_inputs()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.progress_bar["value"] = 0

    def reset_inputs(self):
        self.url_entry.delete(0, tk.END)
        self.fileName_entry.delete(0, tk.END)
        self.videoMaxLength_var.set("60")  # Default value


# Create main window
root = tk.Tk()
root.title("ClipCut")
app = ClipCutApp(master=root)

# Start the GUI event loop
app.mainloop()
