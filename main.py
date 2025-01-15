#!/usr/bin/env python3

import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import json
import requests
from io import BytesIO
import math

# Configuration file path
CONFIG_FILE = "config.json"

def load_config():
    """Load URLs from the configuration file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config file.")
        return []

def fetch_website_thumbnail(url):
    """Fetch the website thumbnail from a favicon provider."""
    try:
        # Using the google favicon service to get the website's favicon
        favicon_url = f"https://www.google.com/s2/favicons?sz=64&domain={url}"
        response = requests.get(favicon_url, stream=True)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Error: Could not fetch thumbnail for {url}. HTTP {response.status_code}")
    except Exception as e:
        print(f"Error: Failed to fetch thumbnail for {url}. Exception: {e}")
    return None

def open_url(url):
    """Open the given URL in the default web browser."""
    webbrowser.open(url)

def create_app():
    """Create the Tkinter app."""
    # Load configuration
    config = load_config()

    # Create main window
    root = tk.Tk()
    root.title("Virtual StreamDeck")

    # Calculate grid size for buttons
    num_buttons = len(config)
    grid_size = math.ceil(math.sqrt(num_buttons))

    # Add buttons for each URL
    for index, entry in enumerate(config):
        if "label" in entry and "url" in entry:
            try:
                # Fetch and resize the image
                image = fetch_website_thumbnail(entry["url"])
                if image:
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)

                    # Create button with image
                    button = tk.Button(root, image=photo, command=lambda url=entry["url"]: open_url(url))
                    button.image = photo
                else:
                    # Create button with text if no thumbnail is available
                    button = tk.Button(root, text=entry["label"], command=lambda url=entry["url"]: open_url(url), width=12, height=6)

                # Place button in grid
                row, col = divmod(index, grid_size)
                button.grid(row=row, column=col, padx=10, pady=10)
            except Exception as e:
                print(f"Warning: Could not create button for {entry['label']}. Error: {e}")
        else:
            print("Warning: Invalid entry in config file. Skipping.")

    # Adjust window size dynamically
    root.update_idletasks()
    root.minsize(root.winfo_width(), root.winfo_height())

    # Run the app
    root.mainloop()

if __name__ == "__main__":
    create_app()
