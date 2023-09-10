from heictojpeg import HEIC2JPEG
from tkinter import filedialog, messagebox
import tkinter as tk
import os

selected_folder = ""
selected_images = []
processed_images = []
processing = False
instance = None

selected_format = ".jpeg"

def open_folder():
    global selected_folder, selected_images
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder = folder_path
        try:
            contents = os.listdir(folder_path)
            # Filter by .heic images
            selected_images = [os.path.join(folder_path, file_name) 
                               for file_name in contents 
                               if file_name.lower().endswith(".heic") 
                               and os.path.isfile(os.path.join(folder_path, file_name))
                               ]
            content_str = "\n".join(selected_images)
            messagebox.showinfo("Folder Contents", f"HEIC images found {folder_path}:\n{content_str}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def process_images():
    global selected_images, processed_images, processing, instance
    if not selected_images:
        messagebox.showwarning("No Images Selected", "Please select a folder with eligible images of HEIC type.")
        return
    try:
        # TODO: custom output folder name input
        output_directory = os.path.join(selected_folder, "jpeg_converted")
        if os.path.exists(output_directory):
            raise FileExistsError("The output folder already exists.")
        os.makedirs(output_directory, exist_ok=True)

        btn_save.config(state=tk.DISABLED)
        btn_cancel.config(state=tk.NORMAL)
        processing = True
        all_images_processed = True

        for file_path in selected_images:
            if not processing:
                all_images_processed = False
                break  # Exit on user cancellation
            
            instance = HEIC2JPEG(file_path, output_directory)
            extension = ".jpeg" if selected_format == ".jpeg" else ".png"
            instance.save(extension)
            
            processed_images.append(file_path)
            processed_text.insert(tk.END, f"{file_path}\n")
            processed_text.update_idletasks()

        btn_save.config(state=tk.NORMAL)
        btn_cancel.config(state=tk.DISABLED)
        processing = False
        instance = None

        if all_images_processed:
            messagebox.showinfo("Processing Complete", f"Processed {len(selected_images)} images successfully.")
        else:
            messagebox.showinfo("Processing Canceled", "Processing was canceled by the user or completed early.")
    except FileExistsError as fe:
        messagebox.showerror("Error", str(fe))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

# TODO: threading
def cancel_processing():
    global processing, instance
    processing = False
    if instance is not None:
        instance.image.close()

def select_format(format_choice):
    global selected_format
    selected_format = format_choice

if __name__ == '__main__':
    window = tk.Tk()
    window.title("HEIC2JPEG")

    window.minsize(400, 200)
    window.columnconfigure(0, weight=1)
    window.maxsize(800,600)

    buttons_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    
    btn_open = tk.Button(buttons_frame, text="Open directory", command=open_folder)
    btn_save = tk.Button(buttons_frame, text="Convert", command=process_images)
    btn_cancel = tk.Button(buttons_frame, text="Cancel", command=cancel_processing, state=tk.DISABLED)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)    
    btn_cancel.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    
    format_label = tk.Label(buttons_frame, text="Select Format:")
    format_label.grid(row=1, column=1, padx=5)
    radio_jpeg = tk.Radiobutton(buttons_frame, text="JPEG", variable=selected_format, value="jpeg", command=lambda: select_format(".jpeg"))
    radio_png = tk.Radiobutton(buttons_frame, text="PNG", variable=selected_format, value="png", command=lambda: select_format(".png"))
    radio_jpeg.grid(row=1, column=2, sticky="w")
    radio_png.grid(row=1, column=3, sticky="w")

    buttons_frame.grid(row=0, column=0, sticky="nsew")
    
    processed_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    processed_label = tk.Label(processed_frame, text="Converted photos:")
    processed_label.pack(side=tk.TOP, anchor=tk.W)
    processed_text = tk.Text(processed_frame, wrap=tk.WORD, height=10, width=30, state=tk.DISABLED)
    processed_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    processed_frame.grid(row=1, column=0, sticky="nsew")

    # Vertical extension
    window.grid_rowconfigure(1, weight=1)
    window.mainloop()