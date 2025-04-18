import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class LabelingApp:
    def __init__(self, root, image_folder, output_file, max_width=500, max_height=500):
        self.root = root
        self.image_folder = image_folder
        self.output_file = output_file
        self.max_width = max_width
        self.max_height = max_height

        # Rename files to replace spaces with underscores
        self.rename_files()

        # Get list of image files (adjust extensions as needed)
        self.image_files = sorted([f for f in os.listdir(image_folder)
                                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        self.index = 0

        # Create UI elements
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.button = tk.Button(root, text="Next", command=self.next_image)
        self.button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.load_image()

    def rename_files(self):
        """Renames files by replacing spaces with underscores only if necessary."""
        for filename in os.listdir(self.image_folder):
            if " " in filename and "_" not in filename:  # Only rename if spaces exist and _ is not present
                new_filename = filename.replace(" ", "_")
                old_path = os.path.join(self.image_folder, filename)
                new_path = os.path.join(self.image_folder, new_filename)

                # Ensure no duplicate filename issue
                counter = 1
                while os.path.exists(new_path):
                    name, ext = os.path.splitext(new_filename)
                    new_filename = f"{name}_{counter}{ext}"
                    new_path = os.path.join(self.image_folder, new_filename)
                    counter += 1

                os.rename(old_path, new_path)

    def load_image(self):
        if self.index < len(self.image_files):
            image_path = os.path.join(self.image_folder, self.image_files[self.index])
            try:
                pil_image = Image.open(image_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {image_path}\n{e}")
                self.index += 1
                self.load_image()
                return

            # Dynamically resize while preserving aspect ratio using LANCZOS resampling
            w, h = pil_image.size
            scale = min(self.max_width / w, self.max_height / h)
            new_width = int(w * scale)
            new_height = int(h * scale)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image)
            self.status_label.config(text=f"Image {self.index+1}/{len(self.image_files)}: {self.image_files[self.index]}")
        else:
            messagebox.showinfo("Done", "All images have been labeled.")
            self.root.quit()

    def next_image(self):
        label_text = self.entry.get().strip() or "N/A"
        image_name = self.image_files[self.index]
        
        # Append image name and label to output file (tab-separated)
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"{image_name}\t{label_text}\n")
        
        self.entry.delete(0, tk.END)
        self.index += 1
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Labeling Tool")
    image_folder = "image_folder\medication"   # Folder containing images in the same directory
    output_file = "labels.txt"      # Output file for labels
    app = LabelingApp(root, image_folder, output_file, max_width=500, max_height=500)
    root.mainloop()
