from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class RiskAssessment(Signature):
    """
    Assess the risk level of an investment portfolio based on market risks.
    """

    investment_portfolio = InputField(desc="The investment portfolio to be assessed.")
    market_risks = InputField(
        desc="The market risks to be considered in the assessment."
    )

    risk_level = OutputField(
        desc="The calculated risk level of the investment portfolio."
    )
