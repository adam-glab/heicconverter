from heictojpeg import HEIC2JPEG
from tkinter import filedialog, messagebox
import os
import tkinter as tk

selected_folder = ""
selected_files = []
processed_files = []
processing = False
instance = None

def open_folder():
    global selected_folder, selected_files
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder = folder_path
        try:
            contents = os.listdir(folder_path)
            # Filter by .heic files
            selected_files = [os.path.join(folder_path, file_name) for file_name in contents if file_name.lower().endswith(".heic") and os.path.isfile(os.path.join(folder_path, file_name))]
            content_str = "\n".join(selected_files)
            messagebox.showinfo("Folder Contents", f"HEIC images found {folder_path}:\n{content_str}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def process_files():
    global selected_files, processed_files, processing, instance
    if not selected_files:
        messagebox.showwarning("No Files Selected", "Please select a folder with eligible files of HEIC type.")
        return
    try:
        output_directory = os.path.join(selected_folder, "jpeg_converted")
        if os.path.exists(output_directory):
            raise FileExistsError("The output folder already exists.")
        os.makedirs(output_directory, exist_ok=True)

        btn_save.config(state=tk.DISABLED)
        btn_cancel.config(state=tk.NORMAL)
        processing = True  # Set processing flag
        all_files_processed = True

        for file_path in selected_files:
            if not processing:
                all_files_processed = False
                break  # Exit processing if the user canceled
            
            instance = HEIC2JPEG(file_path, output_directory)
            instance.save()
            
            processed_files.append(file_path)
            processed_text.insert(tk.END, f"{file_path}\n")
            processed_text.update_idletasks()

        btn_save.config(state=tk.NORMAL)
        btn_cancel.config(state=tk.DISABLED)
        processing = False
        instance = None

        if all_files_processed:
            messagebox.showinfo("Processing Complete", f"Processed {len(selected_files)} files successfully.")
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

if __name__ == '__main__':
    window = tk.Tk()
    window.title("HEIC2JPEG")

    window.minsize(400, 200)
    window.columnconfigure(0, weight=1)
    window.maxsize(800,600)

    buttons_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(buttons_frame, text="Open directory", command=open_folder)
    btn_save = tk.Button(buttons_frame, text="Convert", command=process_files)
    btn_cancel = tk.Button(buttons_frame, text="Cancel", command=cancel_processing, state=tk.DISABLED)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)    
    btn_cancel.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    buttons_frame.grid(row=0, column=0, sticky="nsew")

    processed_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    processed_label = tk.Label(processed_frame, text="Converted photos:")
    processed_label.pack(side=tk.TOP, anchor=tk.W)
    processed_text = tk.Text(processed_frame, wrap=tk.WORD, height=10, width=30)
    processed_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    processed_frame.grid(row=1, column=0, sticky="nsew")

    # Vertical extension
    window.grid_rowconfigure(1, weight=1)
    window.mainloop()