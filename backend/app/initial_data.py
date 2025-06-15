"""
Script to populate the initial data for the Thematic Bible Visualizer API.
Run this script once after setting up the backend to populate the database with initial data.
"""

import json
import os
from pathlib import Path

# Define the data directory
DATA_DIR = Path(__file__).parent / "data"

def load_json_file(filename):
    """Load JSON data from a file."""
    filepath = DATA_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Main function to load and print the initial data."""
    print("Loading initial data...")
    
    # Load data from JSON files
    try:
        themes = load_json_file("themes.json")
        books = load_json_file("biblical_books.json")
        theme_connections = load_json_file("theme_connections.json")
        book_insights = load_json_file("book_insights.json")
        
        print(f"Loaded {len(themes)} themes")
        print(f"Loaded {len(books)} biblical books")
        print(f"Loaded theme connections for {len(theme_connections)} themes")
        print(f"Loaded insights for {len(book_insights)} books")
        
        # In a real application, you would save this data to your database here
        # For example:
        # for theme in themes:
        #     db.themes.insert_one(theme)
        # 
        # for book in books:
        #     db.books.insert_one(book)
        # etc.
        
        print("\nInitial data loaded successfully!")
        print("Note: This script only prints the data. In a real application, "
              "you would save this data to your database.")
        
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        print("Please make sure all data files exist in the data/ directory.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create empty data files if they don't exist
    for filename in ["themes.json", "biblical_books.json", 
                    "theme_connections.json", "book_insights.json"]:
        filepath = DATA_DIR / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
    
    main()
