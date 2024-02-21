from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class SalesPrediction(Signature):
    """
    Use historical sales data and current market trends to predict future sales.
    """
    historical_sales_data = InputField(desc="Data on past sales performance.")
    current_market_trends = InputField(desc="Information on current market trends.")

    future_sales_estimate = OutputField(desc="Estimated future sales based on historical data and current market trends.")
    