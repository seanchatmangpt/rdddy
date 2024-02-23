from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class InventoryOptimization(Signature):
    """
    Optimize inventory levels based on current inventory levels and sales forecasts.
    """

    current_inventory_levels = InputField(
        desc="Current inventory levels for each product."
    )
    sales_forecasts = InputField(desc="Forecasted sales for each product.")

    reorder_recommendations = OutputField(
        desc="Recommended reorder quantities for each product."
    )
