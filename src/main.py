from heicconverter import HEICCONVERTER
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
            current_directory_text.config(state=tk.NORMAL)
            current_directory_text.delete(1.0, tk.END)
            current_directory_text.insert(tk.END, selected_folder)
            current_directory_text.config(state=tk.DISABLED)
            messagebox.showinfo("Folder Contents", f"HEIC images found {folder_path}:\n{content_str}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def process_images():
    global selected_images, processed_images, processing, instance
    if not selected_images:
        messagebox.showwarning("No Images Selected", "Please select a folder with eligible images of HEIC type.")
        return
    try:
        custom_folder_name = output_folder_entry.get()
        if not custom_folder_name:
            messagebox.showerror("Error", "Please enter a folder name.")
            return
        output_directory = os.path.join(selected_folder, custom_folder_name)
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
            
            original_file_name = os.path.splitext(os.path.basename(file_path))[0]
            instance = HEICCONVERTER(file_path, output_directory)
            extension = ".jpeg" if selected_format == ".jpeg" else ".png"
            processed_file_name = original_file_name + extension
            instance.save(extension)
            
            processed_images.append(file_path)
            processed_text.insert(tk.END, f"{original_file_name}.HEIC --> {processed_file_name}\n")
            processed_text.update_idletasks()

        btn_save.config(state=tk.NORMAL)
        btn_cancel.config(state=tk.DISABLED)
        processing = False
        instance = None

        if all_images_processed:
            messagebox.showinfo("Processing Complete", f"Processed all {len(selected_images)} images successfully.")
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
    
def show_app_info():
    app_info = """
    HEIC Converter

    1. Click "Open directory" to select a folder containing HEIC images.
    2. Choose the desired output format (JPEG or PNG).
    3. Enter a custom folder name for the converted files (optional).
    4. Click "Convert photos" to start the conversion process.
    5. To cancel the conversion, click "Cancel."
    6. Processed files will be displayed below.

    Note: Only HEIC files will be converted.
    """
    messagebox.showinfo("How to use", app_info)

if __name__ == '__main__':
    window = tk.Tk()
    window.title("HEIC Converter")

    window.minsize(400, 200)
    window.columnconfigure(0, weight=1)
    window.maxsize(800,600)

    buttons_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    
    btn_open = tk.Button(buttons_frame, text="Open directory", command=open_folder)
    btn_save = tk.Button(buttons_frame, text="Convert photos", command=process_images)
    btn_cancel = tk.Button(buttons_frame, text="Cancel", command=cancel_processing, state=tk.DISABLED)
    btn_info = tk.Button(buttons_frame, text="How to use", command=show_app_info)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)    
    btn_cancel.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    btn_info.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    
    format_label = tk.Label(buttons_frame, text="Select Format:")
    format_label.grid(row=1, column=1, padx=5)
    radio_frame = tk.Frame(buttons_frame)
    radio_frame.grid(row=1, column=2, columnspan=2)

    radio_jpeg = tk.Radiobutton(radio_frame, text="JPEG", variable=selected_format, value=".jpeg", command=lambda: select_format(".jpeg"))
    radio_png = tk.Radiobutton(radio_frame, text="PNG", variable=selected_format, value=".png", command=lambda: select_format(".png"))
    radio_jpeg.grid(row=0, column=0, sticky="w")
    radio_png.grid(row=0, column=1, sticky="w")
    
    folder_name_label = tk.Label(buttons_frame, text="Folder Name:")
    folder_name_label.grid(row=2, column=1, padx=5, pady=5)

    default_folder_name = "output"
    output_folder_entry = tk.Entry(buttons_frame)
    output_folder_entry.insert(0, default_folder_name)
    output_folder_entry.grid(row=2, column=2, padx=5, pady=5)

    buttons_frame.grid(row=0, column=0, sticky="nsew")
    
    current_directory_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    current_directory_label = tk.Label(current_directory_frame, text="Current Directory:")
    current_directory_label.pack(side=tk.TOP, anchor=tk.W)
    current_directory_text = tk.Text(current_directory_frame, wrap=tk.WORD, height=1, width=30)
    current_directory_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    current_directory_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    processed_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    processed_label = tk.Label(processed_frame, text="Converted photos:")
    processed_label.pack(side=tk.TOP, anchor=tk.W)
    processed_text = tk.Text(processed_frame, wrap=tk.WORD, height=10, width=30)
    processed_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    processed_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    # Vertical extension
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.mainloop()