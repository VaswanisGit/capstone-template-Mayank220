import os

class DocTools:
    @staticmethod
    def generate_report(content: str, filename: str = "validation_report.txt") -> str:
        """
        Generates a text report from the provided content.
        Returns the absolute path of the generated file.
        """
        print(f"    [DocTools] Generating report: {filename}")
        
        # Ensure directory exists if path is provided, else use current dir
        # For this stub, we'll just write to the current working directory or specified path
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            abs_path = os.path.abspath(filename)
            print(f"    [DocTools] Report saved to: {abs_path}")
            return abs_path
        except Exception as e:
            print(f"    [DocTools] Error saving report: {e}")
            return ""

