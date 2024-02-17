import dspy


class GenPythonClass(dspy.Signature):
    """
    This signature creates python classes from the prompt.
    """

    prompt = dspy.InputField(desc="The prompt used to generate python classes.")

    source = dspy.OutputField(desc="The generated python classes.")
