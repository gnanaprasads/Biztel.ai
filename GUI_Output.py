import json
import tkinter as tk
from tkinter import filedialog, messagebox

def load_word_positions(text_content):
    """
    Parse the text content into a list of word dictionaries
    """
    word_positions = []
    for item in text_content:
        word_positions.append({
            'word': item['word'],
            'bounding_box': item['bounding_box']
        })
    return word_positions

def scale_coordinates(coords, doc_width, doc_height):
    """
    Convert normalized coordinates (0-1) to actual document coordinates
    """
    x = coords[0] * doc_width
    y = coords[1] * doc_height
    width = coords[2] * doc_width
    height = coords[3] * doc_height
    return [x, y, width, height]
def is_word_in_box(word_coords, user_box):
    """
    Check if a word's bounding box intersects with the user-drawn box
    """
    word_left = word_coords[0]
    word_top = word_coords[1]
    word_right = word_left + word_coords[2]
    word_bottom = word_top + word_coords[3]

    box_left = user_box[0]
    box_top = user_box[1]
    box_right = user_box[2]
    box_bottom = user_box[3]

    return not (word_right < box_left or
                word_left > box_right or
                word_bottom < box_top or
                word_top > box_bottom)

def find_words_in_box(words_data, doc_width, doc_height, user_box):
    """
    Find all words that fall within the user-drawn bounding box
    """
    words_found = []

    for word_data in words_data:
        word_coords = scale_coordinates(word_data['bounding_box'], doc_width, doc_height)

        if is_word_in_box(word_coords, user_box):
            words_found.append(word_data['word'])

    return words_found

def process_input():
    try:
        # Get user inputs
        doc_width = int(entry_width.get())
        doc_height = int(entry_height.get())
        user_box = [
            int(entry_x1.get()),
            int(entry_y1.get()),
            int(entry_x2.get()),
            int(entry_y2.get())
        ]

        # Load JSON file
        file_path = filedialog.askopenfilename(title="Select words_position_dict.txt", 
                                               filetypes=(("JSON files", "*.txt"), ("All files", "*.*")))
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a valid file.")
            return

        with open(file_path, 'r') as file:
            content = json.load(file)

        words_data = load_word_positions(content)
        found_words = find_words_in_box(words_data, doc_width, doc_height, user_box)

        # Display results in a scrollable text widget
        result_textbox.config(state=tk.NORMAL)
        result_textbox.delete(1.0, tk.END)

        if found_words:
            result_textbox.insert(tk.END, "Words found within the bounding box:\n" + "\n".join(found_words))
        else:
            result_textbox.insert(tk.END, "No words found within the bounding box.")

        result_textbox.config(state=tk.DISABLED)

    except FileNotFoundError:
        messagebox.showerror("File Error", "words_position_dict.txt file not found")
    except json.JSONDecodeError:
        messagebox.showerror("JSON Error", "Invalid JSON format in input file")
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please enter numeric values.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create GUI
root = tk.Tk()
root.title("Word Finder in Bounding Box")
root.geometry("800x400")  # Adjusted for left and right frames

# Left frame for inputs
left_frame = tk.Frame(root, width=400, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Document dimensions inputs
tk.Label(left_frame, text="Document Width:", font=("times new roman", 12)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_width = tk.Entry(left_frame, font=("Times new roman", 12))
entry_width.grid(row=0, column=1, padx=5, pady=5)

tk.Label(left_frame, text="Document Height:", font=("times new roman", 12)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_height = tk.Entry(left_frame, font=("times new roman", 12))
entry_height.grid(row=1, column=1, padx=5, pady=5)

# Bounding box inputs
tk.Label(left_frame, text="Bounding Box x1:", font=("times new roman", 12)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_x1 = tk.Entry(left_frame, font=("times new roman", 12))
entry_x1.grid(row=2, column=1, padx=5, pady=5)

tk.Label(left_frame, text="Bounding Box y1:", font=("times new roman", 12)).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_y1 = tk.Entry(left_frame, font=("times new roman", 12))
entry_y1.grid(row=3, column=1, padx=5, pady=5)

tk.Label(left_frame, text="Bounding Box x2:", font=("times new roman", 12)).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
entry_x2 = tk.Entry(left_frame, font=("times new roman", 12))
entry_x2.grid(row=4, column=1, padx=5, pady=5)

tk.Label(left_frame, text="Bounding Box y2:", font=("times new roman", 12)).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
entry_y2 = tk.Entry(left_frame, font=("times new roman", 12))
entry_y2.grid(row=5, column=1, padx=5, pady=5)

# Process button
tk.Button(left_frame, text="Find Words", command=process_input, font=("times new roman", 12)).grid(row=6, column=0, columnspan=2, pady=10)

# Right frame for results
right_frame = tk.Frame(root, width=400, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(right_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_textbox = tk.Text(right_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED, font=("times new roman", 12))
result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=result_textbox.yview)

# Run the GUI
root.mainloop()
