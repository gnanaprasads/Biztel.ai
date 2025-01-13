import json

def load_word_positions(text_content):
    """
    Parse the text content into a list of word dictionaries
    """
    # Convert string representation of list of dicts to actual list of dicts
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
    # Word coordinates
    word_left = word_coords[0]
    word_top = word_coords[1]
    word_right = word_left + word_coords[2]
    word_bottom = word_top + word_coords[3]
    
    # User box coordinates
    box_left = user_box[0]
    box_top = user_box[1]
    box_right = user_box[2]
    box_bottom = user_box[3]
    
    # Check for intersection
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
        # Scale the normalized coordinates to actual document coordinates
        word_coords = scale_coordinates(word_data['bounding_box'], doc_width, doc_height)
        
        # Check if word intersects with user box
        if is_word_in_box(word_coords, user_box):
            words_found.append(word_data['word'])
    
    return words_found

def main():
    # Document dimensions
    DOC_WIDTH = 1263
    DOC_HEIGHT = 1644
    
    # User-drawn bounding box [x1, y1, x3, y3]
    USER_BOX = [358, 140, 498, 171]
    
    # Read and parse the input file
    try:
        with open('words_position_dict.txt', 'r') as file:
            content = json.load(file)
        
        # Load word positions
        words_data = load_word_positions(content)
        
        # Find words in the user-drawn box
        found_words = find_words_in_box(words_data, DOC_WIDTH, DOC_HEIGHT, USER_BOX)
        
        # Output results
        if found_words:
            print("Words found within the bounding box:")
            for word in found_words:
                print(f"- {word}")
        else:
            print("No words found within the bounding box.")
            
    except FileNotFoundError:
        print("Error: words_position_dict.txt file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in input file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()