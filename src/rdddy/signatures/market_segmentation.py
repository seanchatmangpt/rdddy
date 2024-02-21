from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class MarketSegmentation(Signature):
    """
    Use customer demographics and purchase history to generate segment labels.
    """
    customer_demographics = InputField(desc="Information about the characteristics of customers.")
    purchase_history = InputField(desc="Records of past purchases made by customers.")

    segment_labels = OutputField(desc="Labels indicating which segment each customer belongs to.")
    