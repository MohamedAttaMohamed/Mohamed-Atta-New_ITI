import os
import dulwich.porcelain as porcelain

repo_path = os.path.abspath("C:/Users/ghada/.gemini/antigravity/scratch/rag-assistant-project/rag-assistant-project")
remote_url = "https://github.com/MohamedAttaMohamed/Mohamed-Atta-New_ITI.git"

r = porcelain.open_repo(repo_path)

# Update remote origin
config = r.get_config()
config.set(("remote", "origin"), "url", remote_url.encode("utf-8"))
config.write_to_path()
print(f"Updated remote origin to: {remote_url}")

# Re-stage and ensure commit is fresh
porcelain.add(repo_path)
try:
    commit_id = porcelain.commit(
        repo_path,
        message=b"RAG assistant: notebook, FastAPI backend, Streamlit frontend, DSA dataset",
        author=b"Mohamed Atta <mohamed@example.com>",
        committer=b"Mohamed Atta <mohamed@example.com>"
    )
    print(f"Committed changes: {commit_id.decode('ascii')}")
except Exception as e:
    print(f"Commit status: {e}")

print("Repository is ready for push.")
