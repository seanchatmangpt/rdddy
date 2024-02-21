from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class ProductRecommendation(Signature):
    """
    This signature takes in a customer's profile and browsing history and outputs recommended products.
    """
    customer_profile = InputField(desc="The customer's profile information.")
    browsing_history = InputField(desc="The customer's browsing history.")

    recommended_products = OutputField(desc="The list of recommended products.")
    