from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class CustomerFeedbackAnalysis(Signature):
    """
    Perform sentiment analysis on customer comments.
    """
    customer_comments = InputField(desc="The comments provided by the customer.")

    sentiment_analysis = OutputField(desc="The sentiment analysis results for the customer comments.")

class GenerateSearchQuery(dspy.Signature):
"""Write a simple search query that will help answer a complex question."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    query = dspy.OutputField(dtype=dspy.SearchQuery)