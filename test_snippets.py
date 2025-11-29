from tools.template_store import TemplateStore

def test_snippets():
    print("Testing Snippets...")
    snippets = TemplateStore.load_snippets()
    
    # Check if we loaded the snippets
    assert len(snippets) >= 2
    
    # Check investor one pager content
    one_pager = next((s for s in snippets if "investor_one_pager" in s["id"]), None)
    assert one_pager is not None
    assert "Value Proposition" in one_pager["text"]
    assert "The Ask" in one_pager["text"]
    
    # Check validation brief content
    brief = next((s for s in snippets if "validation_brief" in s["id"]), None)
    assert brief is not None
    assert "Problem Statement" in brief["text"]
    assert "Competitive Landscape" in brief["text"]
    
    print("Snippet tests passed.")

if __name__ == "__main__":
    test_snippets()
