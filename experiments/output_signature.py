import dspy

class GenJinjaSignature(dspy.Signature):
    """
    This signature transforms source code into Jinja templates, adhering to best practices for template creation.
    It is designed to take a source code snippet, analyze its structure, and produce a corresponding Jinja template.
    The output template will be well-structured, maintain readability, and include verbose instructions for clarity.

    Best practices incorporated include clear variable naming, usage of control structures for dynamic content,
    ample documentation within the template, and maintaining a structure that mirrors the source while allowing for
    flexibility and scalability in template rendering.
    """
    source = dspy.InputField(
        prefix="Convert to a Jinja Template: ",
        desc="The source code snippet to be converted into a Jinja template. The source should be a valid Python code structure, such as a class or a function, that you wish to render dynamically using Jinja."
    )
    jinja_template = dspy.OutputField(
        prefix="```jinja\n",
        desc="The Jinja template generated from the provided source. This template will embody best practices in template creation, ensuring clarity, maintainability, and ease of use. The template will include dynamic placeholders, control statements, and documentation comments as necessary."
    )


SOURCE = '''class GenerateSearchQuery(dspy.Signature):
    """Write a simple search query that will help answer a complex question."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    query = dspy.OutputField()

### inside your program's __init__ function
self.generate_answer = dspy.ChainOfThought(GenerateSearchQuery)'''


def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)
    cot = dspy.ChainOfThought(GenJinjaSignature)
    template = cot.forward(source=SOURCE).jinja_template
    print(template)


if __name__ == '__main__':
    main()
