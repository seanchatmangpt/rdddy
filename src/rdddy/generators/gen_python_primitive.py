import ast

from dspy import Module, OpenAI, settings, ChainOfThought, Assert


class GenPythonPrimitive(Module):
    def __init__(self, primitive_type, lm=None):
        if lm is None:
            turbo = OpenAI(max_tokens=500)

            settings.configure(lm=turbo)

        super().__init__()

        if primitive_type is set:
            raise ValueError("Set not supported.")

        self.prompt = None
        self.primitive_type = primitive_type
        self.output_key = f"{primitive_type.__name__}_python_primitive_string"
        generation_query = f"prompt -> {self.output_key}"
        correction_query = f"prompt, error -> {self.output_key}"

        # DSPy modules for generation and correction
        self.cot = ChainOfThought(generation_query)
        self.correct_cot = ChainOfThought(correction_query)

    def forward(self, prompt: str):
        self.prompt = prompt
        # Generate the primitive
        cot_result = self.cot(prompt=prompt)
        output = cot_result.get(self.output_key)

        # Try validating the primitive
        try:
            if self.primitive_type is str:
                return output
            if self.primitive_type is bool and "false" in output.lower():
                return False
            if self.primitive_type is bool and "true" in output.lower():
                return True

            Assert(
                self.validate_primitive(output),
                f"You need to create a valid python {self.primitive_type.__name__} "
                f"primitive type for \n{self.output_key}\n"
                f"You will be penalized for not returning only a {self.primitive_type.__name__} for "
                f"{self.output_key}",
            )

            return ast.literal_eval(output)
        except (SyntaxError, AssertionError, ValueError) as error:
            print(error)
            # Try again
            try:
                cot_result = self.correct_cot(prompt=prompt, error=str(error))
                output = cot_result.get(self.output_key)

                return ast.literal_eval(output)
            except (SyntaxError, ValueError) as error:
                raise ValueError(
                    f"Unable to correctly generate a python "
                    f"{self.primitive_type.__name__} from {self.prompt}. "
                )

    def validate_primitive(self, output) -> bool:
        try:
            return isinstance(ast.literal_eval(output), self.primitive_type)
        except SyntaxError as error:
            return False


def main():
    module = GenPythonPrimitive(
        primitive_type=list,
    )

    result = module.forward(
        "Create a list of planets in our solar system sorted by largest to smallest"
    )

    assert result == ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Earth', 'Venus', 'Mars', 'Mercury']

    print(f"The number of planets in the solar system is {result}")


if __name__ == '__main__':
    main()
