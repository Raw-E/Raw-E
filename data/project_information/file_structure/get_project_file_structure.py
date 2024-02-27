import os

def save_directory_contents(path, output_file, indent_level=0):
    """
    Recursively saves the directory structure along with files to a specified file,
    excluding __pycache__ directories.
    
    This function traverses the directory structure from a given starting path, writing
    each directory and file encountered to an output file. Directories are indicated with
    brackets, and indentation is used to represent the hierarchy. The __pycache__ directories
    are explicitly excluded from this listing.

    Args:
        path (str): The directory path to start from.
        output_file (file): An open file object to write the directory contents to.
        indent_level (int): The current level of indentation to represent hierarchy, used for recursive calls.
    """
    # Ensure the path is absolute to avoid relative path errors
    abs_path = os.path.abspath(path)
    
    # Get a sorted list of all entries in the directory for consistent ordering
    entries = sorted(os.listdir(abs_path))
    
    for entry in entries:
        if entry == "__pycache__":
            continue  # Skip __pycache__ directories to avoid clutter
        
        full_entry_path = os.path.join(abs_path, entry)
        if os.path.isdir(full_entry_path):
            # Write the directory name with indentation to indicate hierarchy
            output_file.write('    ' * indent_level + f"[{entry}/]\n")
            # Recursively list the contents of the directory
            save_directory_contents(full_entry_path, output_file, indent_level + 1)
        else:
            # Write the file name with indentation to indicate its position in the hierarchy
            output_file.write('    ' * indent_level + f"- {entry}\n")

if __name__ == "__main__":
    # Define the starting directory and output file name
    project_directory = "../../.."
    output_filename = "project_file_structure.txt"
    
    # Open the output file and write the header with the project directory path
    with open(output_filename, "w") as output_file:
        output_file.write(f"Project File Structure for: {os.path.abspath(project_directory)}\n\n")
        # Start the recursive process of saving the directory contents
        save_directory_contents(project_directory, output_file)
    
    # Inform the user that the process is complete
    print(f"Project file structure has been saved to {output_filename}")