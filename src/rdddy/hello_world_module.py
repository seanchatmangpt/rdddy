import dspy

lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class SummarizeText(dspy.Module):
    """This module summarizes text using a pre-trained model."""

    def forward(self, text):
        pred = dspy.Predict("text -> summary")

        result = pred(text=text).summary
        return result


def main():
    text = """
In his famous commencement speech delivered at Stanford University in 2005, Steve Jobs emphasized the importance of connecting the dots in life, reflecting on his own journey of personal and professional development. Jobs highlighted how seemingly unrelated experiences and decisions in the past could later align and lead to significant opportunities and achievements. He spoke about how dropping out of college and attending calligraphy classes eventually influenced the design and typography of the Macintosh computer, illustrating the unpredictable but crucial nature of connecting dots in hindsight. This perspective encouraged listeners to trust in their intuition, follow their passions, and have faith that the dots will connect in the future, even if the path forward isn't always clear at the present moment."""  # Initialize your inputs here. Adjust as necessary.

    summarize_text = SummarizeText()
    print(summarize_text.forward(text=text))


if __name__ == '__main__':
    main()
