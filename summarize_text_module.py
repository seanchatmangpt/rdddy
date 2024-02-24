import dspy
from typer import Typer

app = Typer()


lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class SummarizeText(dspy.Module):
    """This module summarizes text using a pre-trained model."""

    def forward(self, text):
        pred = dspy.Predict("text -> summary")

        result = pred(text=text).summary
        return result

def main():

    text = ""  # Initialize your inputs here. Adjust as necessary.

    summarize_text = SummarizeText()
    print(summarize_text.forward(text=text))


@app.command()
def module_test(text):
    """This module summarizes text using a pre-trained model."""
    summarize_text = SummarizeText()

    print(summarize_text.forward(text=text))


if __name__ == "__main__":
    app()
    