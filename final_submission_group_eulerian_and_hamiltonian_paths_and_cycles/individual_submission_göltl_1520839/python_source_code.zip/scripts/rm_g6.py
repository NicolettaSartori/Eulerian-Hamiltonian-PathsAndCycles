import os
import glob

# Change directory to Downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
os.chdir(downloads_path)

# Delete every .g6 file permanently
for file_path in glob.glob("*.g6"):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
