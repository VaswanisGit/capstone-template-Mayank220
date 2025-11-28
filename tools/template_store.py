# Template Store
import os
from typing import List, Dict, Any

class TemplateStore:
    @staticmethod
    def load_snippets(path: str = "snippets") -> List[Dict[str, Any]]:
        """
        Loads all text files from the snippets directory.
        Returns list of dicts with id, text, provenance.
        """
        snippets = []
        if not os.path.exists(path):
            print(f"    [TemplateStore] Warning: Path {path} does not exist.")
            return snippets
            
        for filename in os.listdir(path):
            if filename.endswith(".txt"):
                full_path = os.path.join(path, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    snippets.append({
                        "id": filename,
                        "text": content,
                        "provenance": f"local_snippet_{filename}"
                    })
        return snippets

    @staticmethod
    def search_snippets(query: str) -> List[Dict[str, Any]]:
        """
        Stub for searching snippets. Currently returns all snippets.
        """
        print(f"    [TemplateStore] Searching snippets for: {query}")
        return TemplateStore.load_snippets()
