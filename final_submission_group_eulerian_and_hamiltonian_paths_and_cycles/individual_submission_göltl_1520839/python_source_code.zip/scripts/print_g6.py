import os
import glob

# Change directory to Downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
os.chdir(downloads_path)

graphs = []

# Print contents of every .g6 file
for file_path in glob.glob("*.g6"):
    with open(file_path, "r", encoding="utf-8") as f:
        graphs.append('rb"' + f.read().strip() + '"')


print(",\n".join(graphs))
