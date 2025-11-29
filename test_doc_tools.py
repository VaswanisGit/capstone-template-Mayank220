import os
from tools.doc_tools import DocTools

def test_doc_tools():
    print("Testing DocTools...")
    
    content = "This is a test report.\nValidation Score: 100\n"
    filename = "test_report.txt"
    
    # Generate report
    path = DocTools.generate_report(content, filename)
    
    # Verify file exists
    assert os.path.exists(path)
    assert os.path.isfile(path)
    
    # Verify content
    with open(path, "r", encoding="utf-8") as f:
        read_content = f.read()
        assert read_content == content
        
    print("DocTools tests passed.")
    
    # Cleanup
    os.remove(path)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_doc_tools()
