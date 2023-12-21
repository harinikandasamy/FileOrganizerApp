from flask import Flask, render_template, request
from pathlib import Path
import os

app = Flask(__name__)

file_formats = {
    "Images": [".jpeg", ".jpg", ".gif", ".png"],
    "Videos": [".wmv", ".mov", ".mp4", ".avi"],
    "Documents": [".pdf"],
    "Others": []
}


def organize_files(source_folder, target_folder):
        for entry in os.scandir(source_folder):
            if entry.is_file():
                file_path = Path(entry)
                file_extension = file_path.suffix.lower()

                target_dir = target_folder / "Others"
                for category, extensions in file_formats.items():
                    if file_extension in extensions:
                        target_dir = target_folder / category
                        break

                target_dir.mkdir(parents=True, exist_ok=True)
                target_file_path = target_dir / file_path.name

                os.rename(file_path, target_file_path)
                print(f"Moved '{file_path}' to '{target_file_path}'")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        source_folder = Path(request.form["source_folder"])
        target_folder = Path(request.form["target_folder"])

        organize_files(source_folder, target_folder)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
