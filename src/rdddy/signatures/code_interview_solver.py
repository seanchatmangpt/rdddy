from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class CodeInterviewSolver(Signature):
    """
    This signature should first interpret the problem statement to identify key challenges and requirements.
    Each line of the code solution must be accompanied by comments that explain the purpose and logic of that line,
    ensuring that the thought process behind the solution is clear and educational. The aim is to not only solve
    the interview problem but also to provide a learning experience by demystifying complex solution steps and
    fostering a deeper understanding of algorithmic thinking and coding practices. Python PEP8 compliant.
    In the style of Luciano Ramahlo author of Fluent Python.
    """
    problem_statement = InputField(desc="The problem statement to be solved")

    detailed_code_solution = OutputField(desc="The detailed code solution with comments explaining each line of code. In the style of Luciano Ramahlo author of Fluent Python.")
    