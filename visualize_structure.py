"""
Script: visualize_structure.py

Description:
This script generates a visual representation of the folder and file structure
of the current working directory. The output is saved to a file named 
`project_structure.txt` in the root directory where the script is executed.

Features:
- Lists all directories and files in the current working directory.
- Groups directories first, followed by files at each level.
- Uses a tree-like format with proper indentation and symbols (├──, └──, etc.).
- Excludes specified directories and files, such as `.git` and `__pycache__`.

Usage:
1. Place this script in the root directory of your project.
2. Run the script using Python:
   `python visualize_structure.py`
3. Open the generated `project_structure.txt` file to view the folder structure.

Customization:
- Modify the `ignore_list` variable to add or remove files/folders to ignore.
- Adjust indentation or symbols in the `write_structure` function if needed.

Example Output:
PyBUT/
├── assets/
│   ├── fonts/
│   │   └── Rubik-Regular.ttf
│   ├── icon.ico
│   └── logo.png
├── components/
│   ├── backup_manager.py
│   ├── database_manager.py
│   ├── logger.py
│   └── scheduler.py
├── ui/
│   ├── add_task_dialog.py
│   └── edit_task_dialog.py
├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── pybut_tasks.db
└── requirements.txt
"""

import os

def generate_folder_structure():
    # Get the root directory where the script is being run
    root_dir = os.path.abspath(os.getcwd())  # Treat current working directory as root
    script_name = os.path.basename(__file__)
    output_file = os.path.join(root_dir, "project_structure.txt")

    # List of directories and files to ignore
    ignore_list = {".git", "__pycache__", script_name, "project_structure.txt"}

    def write_structure(f, current_dir, level=0):
        # List directories and files in the current directory
        items = sorted(os.listdir(current_dir))
        items = [item for item in items if item not in ignore_list]

        # Separate directories and files
        directories = [item for item in items if os.path.isdir(os.path.join(current_dir, item))]
        files = [item for item in items if not os.path.isdir(os.path.join(current_dir, item))]

        # Write directories first
        for i, directory in enumerate(directories):
            dir_path = os.path.join(current_dir, directory)
            is_last = i == len(directories) - 1 and not files
            prefix = "└── " if is_last else "├── "
            indent = "│   " * level
            f.write(f"{indent}{prefix}{directory}/\n")
            # Recursively write the contents of the directory
            write_structure(f, dir_path, level + 1)

        # Write files after directories
        for i, file in enumerate(files):
            file_path = os.path.join(current_dir, file)
            is_last = i == len(files) - 1
            prefix = "└── " if is_last else "├── "
            indent = "│   " * level
            f.write(f"{indent}{prefix}{file}\n")

    # Start writing to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        root_folder_name = os.path.basename(root_dir)
        f.write(f"{root_folder_name}/\n")
        write_structure(f, root_dir)

    print(f"Folder structure saved to {output_file}")

# Run the function
if __name__ == "__main__":
    generate_folder_structure()