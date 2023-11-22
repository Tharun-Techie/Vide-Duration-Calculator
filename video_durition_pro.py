import os
from tkinter import Tk, filedialog, StringVar, ttk
from moviepy.editor import VideoFileClip


def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()  # Close the clip explicitly
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0


def get_total_duration(folder_path):
    total_duration = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
                file_path = os.path.join(root, file)
                duration = get_video_duration(file_path)
                total_duration += duration

    return total_duration


def browse_folder():
    loading_label.config(text="Please wait, calculating...")
    root.update()  # Force update to display the loading message

    folder_path = filedialog.askdirectory()
    if folder_path:
        total_duration = get_total_duration(folder_path)
        if total_duration == 0:
            result_var.set(f"There are no Videos :)")
        elif total_duration > 0:
            result_var.set(f"Total duration of all videos: {total_duration:.2f} seconds or {total_duration / 3600:.2f} Hours")
    else:
        result_var.set("No folder selected.")

    loading_label.config(text="")  # Clear the loading message


# Create the main window
root = Tk()
root.title("Video Duration Calculator")
# Set fixed size and center the window on the screen
window_width = 350
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Custom color theme
style = ttk.Style()
style.theme_create("stylish", parent="alt", settings={
    "TButton": {"configure": {"background": "#ff9a68", "foreground": "white", "font": ('Times New Roman', 12, 'bold')}},
    "TLabel": {"configure": {"foreground": "#333333", "font": ('Times New Roman', 12, 'bold')}},
    "TFrame": {"configure": {"background": "#f0f0f0"}}
})
style.theme_use("stylish")

# Create and configure GUI elements
frame = ttk.Frame(root)
#frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame.place(relx=0.5, rely=0.5, anchor="center")

label = ttk.Label(frame, text="Click below to select a folder:")
label.grid(row=0, column=0, columnspan=2, pady=10)

browse_button = ttk.Button(frame, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=0, pady=10)

loading_label = ttk.Label(frame, text="")
loading_label.grid(row=2, column=0, columnspan=2, pady=10)

result_var = StringVar()
result_label = ttk.Label(frame, textvariable=result_var)
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Configure row and column weights to make resizing work properly
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Run the GUI
root.mainloop()
