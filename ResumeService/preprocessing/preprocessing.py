import re


class TextPreprocessor:

    def __init__(self, text: str):
        self.text = text.lower()

    def clean_text(self) -> str:
        """
        Perform basic text cleaning.
        """
        text = self.text

        # remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        # remove special characters except basic punctuation
        text = re.sub(r"[^\w\s.,@+-]", "", text)

        return text.strip()

    def preprocess(self) -> str:
        """
        Run full preprocessing pipeline.
        """
        return self.clean_text()









