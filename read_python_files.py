import os

def read_python_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(file_path)

if __name__ == "__main__":
    target_directory = "."  # You can change this to the desired directory
    read_python_files(target_directory)