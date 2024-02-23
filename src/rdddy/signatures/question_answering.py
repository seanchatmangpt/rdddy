from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class QuestionAnswering(Signature):
    """
    Documentation of the task's expected LM function and output.
    """

    context = InputField(desc="Contains cited relevant facts.")
    question = InputField(desc="The question to be answered.")

    answer = OutputField(desc="Descriptive answer to the question.")
