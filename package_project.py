import os
import zipfile

source_dir = os.path.abspath("C:/Users/ghada/.gemini/antigravity/scratch/rag-assistant-project/rag-assistant-project")
output_zip = os.path.abspath("C:/Users/ghada/Downloads/rag-assistant-project-updated.zip")

exclude_dirs = {".venv", "__pycache__", ".ipynb_checkpoints", ".git", ".pytest_cache"}
exclude_extensions = {".pyc", ".log"}

with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as ziph:
    for root, dirs, files in os.walk(source_dir):
        # Exclude directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file == ".env" or any(file.endswith(ext) for ext in exclude_extensions):
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, source_dir)
            ziph.write(abs_path, rel_path)

print(f"Successfully packaged project to: {output_zip}")
