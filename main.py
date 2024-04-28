from pytube import YouTube
import urllib.request
import customtkinter
from PIL import Image, ImageDraw
import os, threading
from tkinter import PhotoImage
from moviepy.editor import *


# Modes: system (default), light, dark
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk(fg_color="#ecedff")
app.geometry("480x100")
app.title("YT Video Downloader")
app.iconbitmap("yt_icon.ico")
app.maxsize(480, 100)
app.minsize(480, 100)
app.bind_all("<Button-1>", lambda event: event.widget.focus_set())

gobutt_img = customtkinter.CTkImage(
    light_image=Image.open("youtube.png"),
    dark_image=Image.open("youtube.png"),
    size=(32, 32),
)
retry = customtkinter.CTkImage(
    light_image=Image.open("reloading.png"),
    dark_image=Image.open("reloading.png"),
    size=(32, 32),
)
downloadd = customtkinter.CTkImage(
    light_image=Image.open("download.png"),
    dark_image=Image.open("download.png"),
    size=(32, 32),
)
gobutt_imgey = customtkinter.CTkImage(
    light_image=Image.open("youtube (2).png"),
    dark_image=Image.open("youtube (2).png"),
    size=(32, 32),
)

gifloader = Image.open("yt.gif")
loadframes = gifloader.n_frames
imgObj = [
    PhotoImage(file="yt.gif", format=f"gif -index {i}") for i in range(loadframes)
]
count = 0
showanimation = None


gifloader1 = Image.open("done.gif")
loadframes1 = gifloader1.n_frames
imgObj1 = [
    PhotoImage(file="done.gif", format=f"gif -index {i}") for i in range(loadframes1)
]
count1 = 0
showanimation1 = None


def add_corners(im, rad):
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new("L", im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def download_window():
    # storing url before forgetting
    urll = str(url.get())
    print(urll)
    app.withdraw()

    def check_if_avail(itagg):
        if isinstance(itagg, int):
            itagg = [itagg]

        for i in itagg:
            if yt.streams.get_by_itag(i) is not None:
                return i
            else:
                return None

    try:
        if urll != "":
            # storing thumbnail for future use
            yt = YouTube(urll)
            thumb_url = yt.thumbnail_url

            vid_title = yt.title
            if len(vid_title) > 50:
                vid_title = vid_title[0:51] + "..."

            urllib.request.urlretrieve(thumb_url, "thumb.png")
            thumbnail = Image.open("thumb.png")
            thumbnail = add_corners(thumbnail, 30)

            thumbnail_final = customtkinter.CTkImage(
                light_image=thumbnail, dark_image=thumbnail, size=(320, 180)
            )

            ytitle = (
                yt.title.replace("?", "")
                .replace(":", "")
                .replace("=", "")
                .replace("|", "")
                .replace("/", "")
                .replace("\\", "")
            )
            username = os.getlogin()

            def main_window():

                dnld.configure(fg_color="#ecedff")

                for child in dnld.winfo_children():
                    child.destroy()

                def download(type, itag, quality):
                    name = quality + " " + ytitle
                    auditag = [140, 251]

                    if type == "prog":
                        yt.streams.get_by_itag(itag=itag).download(
                            f"C:/Users/{username}/Downloads", filename=f"{name}.mp4"
                        )

                    if type == "adap":
                        if check_if_avail(itag) is not None:
                            print("Starting Audio Download...")
                            yt.streams.get_by_itag(auditag[1]).download(
                                filename=f"{quality}audio.mp3"
                            )
                            print("audio downloaded")
                            print("Starting Video Download...")
                            yt.streams.get_by_itag(check_if_avail(itag)).download(
                                filename=f"{name}.mp4"
                            )
                            print("video downloaded")
                            videoclip = VideoFileClip(f"{name}.mp4")
                            audioclip = AudioFileClip(f"{quality}audio.mp3")

                            new_audioclip = CompositeAudioClip([audioclip])
                            videoclip.audio = new_audioclip
                            videoclip.write_videofile(
                                f"C:/Users/{username}/Downloads/{name}.mp4"
                            )

                            os.remove(f"{quality}audio.mp3")
                            os.remove(f"{name}.mp4")

                    else:
                        print("Not Available")

                def stop_animation(button):
                    global showanimation1
                    # Cancel the scheduled animation function
                    app.after_cancel(showanimation1)
                    # Change the image back to downloadd
                    button.configure(image=downloadd)

                def check_thread(button, count, thread):
                    if thread.is_alive():
                        button.after(
                            100, check_thread, button, count, thread
                        )  # Check again after 100 ms
                    else:
                        # Schedule downanimation to run after a delay
                        button.after(
                            100, lambda: downanimation(button, count)
                        )  # 1000 ms = 1 second
                        # Schedule stop_animation to run after a longer delay
                        button.after(
                            5180, lambda: stop_animation(button)
                        )  # 4000 ms = 4 seconds

                def downloadAndAnimate(type, itag, quality, button, count):
                    downloading = threading.Thread(
                        name="Downloading", target=download, args=(type, itag, quality)
                    )

                    downloading.start()

                    check_thread(button=button, count=count, thread=downloading)

                bg = customtkinter.CTkFrame(
                    master=dnld,
                    width=500,
                    height=540,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#f8f9fe",
                    bg_color="#ecedff",
                )
                bg.place(relx=0.085, rely=0.05)

                img = customtkinter.CTkLabel(
                    master=bg,
                    width=320,
                    height=180,
                    text="",
                    image=thumbnail_final,
                    bg_color="#f8f9fe",
                )
                img.place(relx=0.185, rely=0.04)

                title = customtkinter.CTkButton(
                    master=bg,
                    width=450,
                    height=30,
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    hover=False,
                    text=vid_title,
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                title.place(relx=0.044, rely=0.39)

                dnlds = customtkinter.CTkScrollableFrame(
                    master=bg,
                    width=425,
                    height=10,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#f8f9fe",
                    fg_color="#ecedff",
                    scrollbar_button_color="#f8f9fe",
                    scrollbar_fg_color="#ecedff",
                    scrollbar_button_hover_color="white",
                )
                dnlds.place(relx=0.044, rely=0.463)

                # 144p
                onefourfourp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                onefourfourpquality = customtkinter.CTkLabel(
                    master=onefourfourp,
                    height=50,
                    width=50,
                    text="144p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                onefourfourptype = customtkinter.CTkLabel(
                    master=onefourfourp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                onefourfourpdownld = customtkinter.CTkButton(
                    master=onefourfourp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: onefourfourpdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [160], "144p", onefourfourpdownld, count1
                        )
                    ),
                )
                # 240p
                twofortyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                twofortypquality = customtkinter.CTkLabel(
                    master=twofortyp,
                    height=50,
                    width=50,
                    text="240p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                twofortyptype = customtkinter.CTkLabel(
                    master=twofortyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                twofortypdownld = customtkinter.CTkButton(
                    master=twofortyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: twofortypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [133], "240p", twofortypdownld, count1
                        )
                    ),
                )

                # 360p
                threesixtyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                threesixtypquality = customtkinter.CTkLabel(
                    master=threesixtyp,
                    height=50,
                    width=50,
                    text="360p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                threesixtyptype = customtkinter.CTkLabel(
                    master=threesixtyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                threesixtypdownld = customtkinter.CTkButton(
                    master=threesixtyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: threesixtypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "prog", 18, "360p", threesixtypdownld, count1
                        )
                    ),
                )

                # 480p
                foureightyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                foureightypquality = customtkinter.CTkLabel(
                    master=foureightyp,
                    height=50,
                    width=50,
                    text="480p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                foureightyptype = customtkinter.CTkLabel(
                    master=foureightyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                foureightypdownld = customtkinter.CTkButton(
                    master=foureightyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: foureightypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [135], "480p", foureightypdownld, count1
                        )
                    ),
                )

                # 720p
                sevententyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                seventwentypquality = customtkinter.CTkLabel(
                    master=sevententyp,
                    height=50,
                    width=50,
                    text="720p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                seventwentyptype = customtkinter.CTkLabel(
                    master=sevententyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                seventwentypdownld = customtkinter.CTkButton(
                    master=sevententyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: seventwentypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", 22, "720p", seventwentypdownld, count1
                        )
                    ),
                )

                # 1080p
                teneightyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                teneightypquality = customtkinter.CTkLabel(
                    master=teneightyp,
                    height=50,
                    width=50,
                    text="1080p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                teneightyptype = customtkinter.CTkLabel(
                    master=teneightyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                teneightypdownld = customtkinter.CTkButton(
                    master=teneightyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: teneightypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [248, 335], "1080p", teneightypdownld, count1
                        )
                    ),
                )

                # 1440p
                fourteenfortyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                fourteenfortypquality = customtkinter.CTkLabel(
                    master=fourteenfortyp,
                    height=50,
                    width=50,
                    text="1440p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                fourteenfortyptype = customtkinter.CTkLabel(
                    master=fourteenfortyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                fourteenfortypdownld = customtkinter.CTkButton(
                    master=fourteenfortyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: fourteenfortypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [271, 336], "1440p", fourteenfortypdownld, count1
                        )
                    ),
                )

                # 2160p
                twentyonesixtyp = customtkinter.CTkFrame(
                    master=dnlds,
                    width=425,
                    height=50,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    bg_color="#ecedff",
                    fg_color="#f8f9fe",
                )
                twentyonesixtypquality = customtkinter.CTkLabel(
                    master=twentyonesixtyp,
                    height=50,
                    width=50,
                    text="2160p",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                twentyonesixtyptype = customtkinter.CTkLabel(
                    master=twentyonesixtyp,
                    height=50,
                    width=50,
                    text="mp4",
                    bg_color="#f8f9fe",
                    fg_color="#f8f9fe",
                    text_color="black",
                    font=("Poppins Black", 15),
                )
                twentyonesixtypdownld = customtkinter.CTkButton(
                    master=twentyonesixtyp,
                    width=35,
                    height=45,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    image=downloadd,
                    text="",
                )
                app.after(
                    50,
                    lambda: twentyonesixtypdownld.configure(
                        command=lambda: downloadAndAnimate(
                            "adap", [313, 337], "2160p", twentyonesixtypdownld, count1
                        )
                    ),
                )

                # [160, 133, 18, 135, 22, 335, 336, 337, 313, 271, 248, 140, 251]

                if results[0] == True:
                    onefourfourp.pack(pady=5)
                    onefourfourpquality.place(relx=0.01)
                    onefourfourptype.place(relx=0.43)
                    onefourfourpdownld.place(relx=0.86, rely=0.05)

                if results[1] == True:
                    twofortyp.pack(pady=5)
                    twofortypquality.place(relx=0.01)
                    twofortyptype.place(relx=0.43)
                    twofortypdownld.place(relx=0.86, rely=0.05)

                if results[2] == True:
                    threesixtyp.pack(pady=5)
                    threesixtypquality.place(relx=0.01)
                    threesixtyptype.place(relx=0.43)
                    threesixtypdownld.place(relx=0.86, rely=0.05)

                if results[3] == True:
                    foureightyp.pack(pady=5)
                    foureightypquality.place(relx=0.01)
                    foureightyptype.place(relx=0.43)
                    foureightypdownld.place(relx=0.86, rely=0.05)

                if results[4] == True:
                    sevententyp.pack(pady=5)
                    seventwentypquality.place(relx=0.01)
                    seventwentyptype.place(relx=0.43)
                    seventwentypdownld.place(relx=0.86, rely=0.05)

                if results[5] == True or results[10] == True:
                    teneightyp.pack(pady=5)
                    teneightypquality.place(relx=0.01)
                    teneightyptype.place(relx=0.43)
                    teneightypdownld.place(relx=0.86, rely=0.05)

                if results[6] == True or results[9] == True:
                    fourteenfortyp.pack(pady=5)
                    fourteenfortypquality.place(relx=0.01)
                    fourteenfortyptype.place(relx=0.43)
                    fourteenfortypdownld.place(relx=0.86, rely=0.05)

                if results[7] == True or results[8] == True:
                    twentyonesixtyp.pack(pady=5)
                    twentyonesixtypquality.place(relx=0.01)
                    twentyonesixtyptype.place(relx=0.43)
                    twentyonesixtypdownld.place(relx=0.86, rely=0.05)

                tryagain = customtkinter.CTkButton(
                    master=dnld,
                    width=120,
                    command=open_strt,
                    height=40,
                    corner_radius=10,
                    border_color="white",
                    border_width=2,
                    fg_color="#ecedff",
                    bg_color="#f8f9fe",
                    hover_color="#f8f9fe",
                    text="Another One?",
                    image=retry,
                    font=("Poppins Black", 14),
                    text_color="red",
                )
                tryagain.place(relx=0.357, rely=0.863)

            def open_strt():
                app.deiconify()
                dnld.destroy()
                url.delete(0, customtkinter.END)

            dnld = customtkinter.CTkToplevel(fg_color="black")
            dnld.geometry("600x600")
            dnld.title("YT Video Downloader")
            dnld.after(250, lambda: dnld.iconbitmap("yt_icon.ico"))
            dnld.maxsize(600, 600)
            dnld.minsize(600, 600)

            frame = customtkinter.CTkFrame(
                master=dnld, fg_color="black", width=600, height=600
            )
            frame.place(relx=0, rely=0)

            loader = customtkinter.CTkLabel(
                master=dnld, text="", image="", width=300, height=300, bg_color="black"
            )
            Loading = customtkinter.CTkLabel(
                master=dnld,
                font=("Poppins Black", 27.5),
                text="Sometimes, a buffer is important...",
                text_color="white",
                bg_color="black",
            )
            lol = customtkinter.CTkLabel(
                master=dnld,
                font=("Poppins", 15),
                text="noo, believe me, I am Serious!",
                text_color="#444444",
                bg_color="black",
            )

            diff_itags = [160, 133, 18, 135, 22, 335, 336, 337, 313, 271, 248, 140, 251]
            results = []

            # filling results
            def func():
                for itagg in diff_itags:
                    check = check_if_avail(itagg)
                    if check == None:
                        results.append(False)
                    else:
                        results.append(True)
                print(results)

            # declaring a thread to run alongside the program
            main_func = threading.Thread(target=func)

            def animation(count):
                if loader.winfo_exists():
                    global showanimation
                    newImage = imgObj[count]
                    if count == loadframes - 1:
                        count = 0
                    loader.configure(image=newImage)
                    count += 1

                    showanimation = app.after(50, lambda: animation(count))

            def downanimation(button, count):
                global showanimation1
                newImage = imgObj1[count]
                if count == loadframes1 - 1:
                    count = 0
                button.configure(image=newImage)
                count += 1

                showanimation1 = app.after(
                    50, lambda: downanimation(button=button, count=count)
                )

            def animestrt():
                loader.place(relx=0.2375, rely=0.15)
                Loading.place(relx=0.09, rely=0.8)
                lol.place(relx=0.09, rely=0.86)
                animation(count)

            animestrt()
            main_func.start()

            app.after(7500, main_window)

        else:
            url.delete(0, customtkinter.END)
            url.configure(placeholder_text="    Please Enter A Valid Youtube URL")

    except Exception as e:

        url.delete(0, customtkinter.END)
        url.configure(placeholder_text="    Please Enter A Valid Youtube URL")
        print(f"An Error Occured --> {e}")


fg = customtkinter.CTkLabel(
    master=app,
    width=460,
    height=75,
    corner_radius=0,
    fg_color="#ecedff",
    text="",
    bg_color="#ecedff",
)
fg.place(relx=0.0225, rely=0.1)


url = customtkinter.CTkEntry(
    master=fg,
    width=385,
    height=60,
    corner_radius=7.5,
    bg_color="#ecedff",
    border_width=2,
    border_color="#ffffff",
    text_color="#ff0000",
    fg_color="#f8f9fe",
    placeholder_text="    Enter Video URL",
    placeholder_text_color="#ff0000",
    font=("Poppins Black", 15),
)
url.place(relx=0.014, rely=0.125)


gobutt = customtkinter.CTkButton(
    master=fg,
    text="",
    command=download_window,
    fg_color="#f8f9fe",
    border_color="white",
    hover_color="#ecedff",
    border_width=2,
    bg_color="#ecedff",
    width=60,
    height=60,
    corner_radius=7.5,
    image=gobutt_img,
)
gobutt.place(relx=0.86, rely=0.125)


app.mainloop()
