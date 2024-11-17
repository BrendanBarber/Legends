from rich.markdown import Markdown

class Description:
    def __init__(self, text: str):
        self.text = text

    def render(self):
        return Markdown(self.text)

    def __repr__(self):
        return f"Description(text={self.text}"