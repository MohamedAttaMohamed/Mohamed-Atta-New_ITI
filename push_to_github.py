import os
import dulwich.porcelain as porcelain

repo_path = os.path.abspath("C:/Users/ghada/.gemini/antigravity/scratch/rag-assistant-project/rag-assistant-project")
remote_url = "https://github.com/MohamedAttaMohamed/Mohamed-Atta-New_ITI.git"

r = porcelain.open_repo(repo_path)

try:
    print(f"Attempting push to {remote_url}...")
    porcelain.push(r, remote_url, refspecs=b"refs/heads/main:refs/heads/main")
    print("Successfully pushed to GitHub!")
except Exception as e:
    print(f"Push result: {e}")
