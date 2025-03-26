import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class LabelVerificationApp:
    def __init__(self, root, image_folder, label_file):
        self.root = root
        self.image_folder = image_folder
        self.label_file = label_file

        # Load label data
        self.labels = self.load_labels()
        self.index = 0

        # UI Setup
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Image display
        self.image_label = tk.Label(self.frame)
        self.image_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        # Label Information
        self.path_label = tk.Label(self.frame, text="", fg="blue", wraplength=400)
        self.path_label.grid(row=0, column=1, sticky="w")

        self.label_entry = tk.Entry(self.frame, width=50)
        self.label_entry.grid(row=1, column=1, pady=5)

        # Buttons
        self.prev_button = tk.Button(self.frame, text="Previous", command=self.prev_image)
        self.prev_button.grid(row=2, column=1, sticky="w", padx=5)

        self.next_button = tk.Button(self.frame, text="Next", command=self.next_image)
        self.next_button.grid(row=2, column=1, sticky="e", padx=5)

        self.save_button = tk.Button(self.frame, text="Save Label", command=self.save_label)
        self.save_button.grid(row=3, column=1, pady=5)

        self.delete_button = tk.Button(self.frame, text="Delete Image", fg="white", bg="red", command=self.delete_image)
        self.delete_button.grid(row=4, column=1, pady=5)

        self.load_image()

    def load_labels(self):
        """Reads labels.txt and stores data in a list."""
        labels = []
        if not os.path.exists(self.label_file):
            messagebox.showerror("Error", f"Label file '{self.label_file}' not found!")
            self.root.quit()
            return []

        with open(self.label_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    labels.append((parts[0], parts[1]))  # (filename, label)
        return labels

    def load_image(self):
        """Loads the current image and displays label/path."""
        if not self.labels:
            messagebox.showinfo("Done", "No more images to verify.")
            self.root.quit()
            return

        if self.index < 0 or self.index >= len(self.labels):
            self.index = 0  # Reset index if out of range

        image_name, label = self.labels[self.index]
        image_path = os.path.join(self.image_folder, image_name)

        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"Image not found: {image_path}")
            return

        try:
            pil_image = Image.open(image_path)
            pil_image.thumbnail((500, 500), Image.Resampling.LANCZOS)  # Resize for display
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image {image_name}\n{e}")
            return

        # Update text fields
        self.path_label.config(text=f"Path: {image_path}")
        self.label_entry.delete(0, tk.END)
        self.label_entry.insert(0, label)

    def save_label(self):
        """Saves the updated label to labels.txt."""
        if self.index < 0 or self.index >= len(self.labels):
            return

        new_label = self.label_entry.get().strip()
        self.labels[self.index] = (self.labels[self.index][0], new_label)

        # Rewrite the labels file
        with open(self.label_file, "w", encoding="utf-8") as f:
            for filename, label in self.labels:
                f.write(f"{filename}\t{label}\n")

        messagebox.showinfo("Success", "Label saved!")

    def delete_image(self):
        """Deletes the current image and removes its label."""
        if self.index < 0 or self.index >= len(self.labels):
            return

        image_name, _ = self.labels[self.index]
        image_path = os.path.join(self.image_folder, image_name)

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete:\n{image_name}?")
        if not confirm:
            return

        # Delete image file
        if os.path.exists(image_path):
            os.remove(image_path)

        # Remove label from the list and update labels.txt
        del self.labels[self.index]
        with open(self.label_file, "w", encoding="utf-8") as f:
            for filename, label in self.labels:
                f.write(f"{filename}\t{label}\n")

        messagebox.showinfo("Deleted", f"{image_name} has been deleted.")

        # Load next image
        self.load_image()

    def next_image(self):
        """Move to the next image."""
        self.index = (self.index + 1) % len(self.labels) if self.labels else 0
        self.load_image()

    def prev_image(self):
        """Move to the previous image."""
        self.index = (self.index - 1) % len(self.labels) if self.labels else 0
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Label Verification")
    image_folder = "image_folder\Arabic_DataSet"  # Change to your actual image folder
    label_file = "labels.txt"

    app = LabelVerificationApp(root, image_folder, label_file)
    root.mainloop()
