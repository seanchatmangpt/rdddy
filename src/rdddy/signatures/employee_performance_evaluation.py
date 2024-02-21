from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class EmployeePerformanceEvaluation(Signature):
    """
    Generate a performance rating for an employee based on their activities and project outcomes.
    """
    employee_activities = InputField(desc="List of activities performed by the employee.")
    project_outcomes = InputField(desc="List of outcomes achieved by the employee's projects.")

    performance_rating = OutputField(desc="Numeric rating indicating the employee's performance.")
    