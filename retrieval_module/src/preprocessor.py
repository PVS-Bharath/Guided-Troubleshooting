import re

class TextPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text

if __name__ == "__main__":
    p = TextPreprocessor()
    print("Cleaned:", p.clean_text("  My Phone   is HOT!  "))