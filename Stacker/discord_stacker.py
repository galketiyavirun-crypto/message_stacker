
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import re
import moviepy.editor as mpy


class DiscordStackVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Screenshot Stack to Video")

        self.frames = []
        self.durations = []

        # UI
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        tk.Button(
            self.frame,
            text="Load Screenshots & Stack",
            command=self.load_and_stack_images
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            self.frame,
            text="Set Durations",
            command=self.set_durations
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            self.frame,
            text="Export Video",
            command=self.export_video
        ).grid(row=0, column=2, padx=5)

        self.image_label = tk.Label(root, text="Preview will appear here")
        self.image_label.pack(pady=10)

    # -------------------------
    # Natural sorting
    # -------------------------
    def natural_key(self, s):
        return [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)
        ]

    # -------------------------
    # Load and stack images
    # -------------------------
    def load_and_stack_images(self):
        folder = filedialog.askdirectory()

        if not folder:
            return

        files = sorted(
            [
                f for f in os.listdir(folder)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ],
            key=self.natural_key
        )

        if not files:
            messagebox.showerror("No Images", "No images found.")
            return

        self.frames.clear()
        self.durations.clear()

        current_group = []

        for file in files:
            full_path = os.path.join(folder, file)

            img = Image.open(full_path).convert("RGB")

            self.show_image(img)

            is_main = messagebox.askyesno(
                "Main Message?",
                f"Is this image:\n\n{file}\n\na MAIN message?"
            )

            # New message chain starts
            if is_main:
                if current_group:
                    self.create_stacked_frames(current_group)

                current_group = [img]

            else:
                current_group.append(img)

        # Final group
        if current_group:
            self.create_stacked_frames(current_group)

        messagebox.showinfo(
            "Done",
            f"{len(self.frames)} stacked frames generated."
        )

    # -------------------------
    # Create progressive stacks
    # -------------------------
    def create_stacked_frames(self, images):
        stacked = images[0].copy()

        self.frames.append(stacked.copy())

        for img in images[1:]:

            total_height = stacked.height + img.height
            total_width = max(stacked.width, img.width)

            new_stack = Image.new(
                "RGB",
                (total_width, total_height),
                color=(54, 57, 63)
            )

            new_stack.paste(stacked, (0, 0))
            new_stack.paste(img, (0, stacked.height))

            stacked = new_stack

            self.frames.append(stacked.copy())

    # -------------------------
    # Set frame durations
    # -------------------------
    def set_durations(self):
        if not self.frames:
            messagebox.showwarning(
                "No Frames",
                "Load and stack images first."
            )
            return

        self.durations.clear()

        for idx in range(len(self.frames)):

            while True:
                try:
                    duration = simpledialog.askfloat(
                        "Frame Duration",
                        f"Duration for frame {idx + 1} (seconds):",
                        initialvalue=1.75,
                        minvalue=0.1
                    )

                    if duration is None:
                        return

                    self.durations.append(duration)
                    break

                except:
                    messagebox.showerror(
                        "Invalid Input",
                        "Please enter a valid number."
                    )

    # -------------------------
    # Show preview image
    # -------------------------
    def show_image(self, img):
        preview = img.copy()
        preview.thumbnail((800, 600))

        tk_img = ImageTk.PhotoImage(preview)

        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img

        self.root.update()

    # -------------------------
    # Export video
    # -------------------------

    def export_video(self):

        if not self.frames:
            messagebox.showwarning(
                "No Frames",
                "No frames available."
            )
            return

        if len(self.durations) != len(self.frames):
            messagebox.showwarning(
                "Durations Missing",
                "Set durations first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")],
            title="Save Video"
        )

        if not save_path:
            return

        clips = []
        temp_files = []

        try:

        # Load sound ONCE
            audio_source = None

            if os.path.exists("discord.mp3"):
                audio_source = mpy.AudioFileClip("discord.mp3")

            for idx, frame in enumerate(self.frames):

                temp_path = f"_temp_frame_{idx}.png"

                frame.save(temp_path)

                temp_files.append(temp_path)

            # Create image clip
                clip = mpy.ImageClip(temp_path)

                clip = clip.set_duration(self.durations[idx])

            # Add audio
                if audio_source:

                    audio = audio_source.subclip(
                        0,
                        min(audio_source.duration, self.durations[idx])
                    )

                    audio = audio.volumex(1.0)

                    clip = clip.set_audio(audio)

                clips.append(clip)

        # Combine clips
            final_video = mpy.concatenate_videoclips(
                clips,
                method="compose"
            )

        # Export video
            final_video.write_videofile(
                save_path,
                fps=24,
                codec="libx264",
                audio=True,
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True
            )

            messagebox.showinfo(
                "Export Complete",
                f"Saved to:\n{save_path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )
 
        finally:

        # Cleanup
            for file in temp_files:
                if os.path.exists(file):
                    os.remove(file)




if __name__ == "__main__":

    root = tk.Tk()

    app = DiscordStackVideoApp(root)

    root.mainloop()
















