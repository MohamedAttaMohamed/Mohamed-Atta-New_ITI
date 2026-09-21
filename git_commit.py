import os
import dulwich.porcelain as porcelain

repo_path = os.path.abspath("C:/Users/ghada/.gemini/antigravity/scratch/rag-assistant-project/rag-assistant-project")

# Initialize repo if not initialized
if not os.path.exists(os.path.join(repo_path, ".git")):
    r = porcelain.init(repo_path)
    print("Initialized Git repository.")
else:
    r = porcelain.open_repo(repo_path)
    print("Opened existing Git repository.")

# Add files
porcelain.add(repo_path)
print("Staged files for commit.")

# Commit
commit_id = porcelain.commit(
    repo_path,
    message=b"RAG assistant: notebook, FastAPI backend, Streamlit frontend, DSA dataset",
    author=b"Mohamed Atta <mohamed@example.com>",
    committer=b"Mohamed Atta <mohamed@example.com>"
)

print(f"Committed successfully with commit ID: {commit_id.decode('ascii')}")
