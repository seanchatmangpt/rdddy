import dspy

lm = dspy.OpenAI(max_tokens=2000)
dspy.settings.configure(lm=lm)


class GenerateHygenTemplate(dspy.Signature):
    """Generate a Hygen template based on specified requirements.
    ---
    to: app/emails/<%= name %>.html
    ---


    Hello <%= name %>,
    <%= message %>
    (version <%= version %>)
    """

    requirements = dspy.InputField(
        desc="Specifications or requirements for the Hygen template"
    )
    template = dspy.OutputField(desc="Generated Hygen template code")


class HygenTemplateGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_template = dspy.ChainOfThought(GenerateHygenTemplate)

    def forward(self, requirements):
        # The ChainOfThought could involve parsing the requirements,
        # determining the structure and variables needed for the Hygen template,
        # and then constructing the template code.
        template_code = self.generate_template(requirements=requirements).template
        return dspy.Prediction(template=template_code)


def main():
    # Example usage
    generator = HygenTemplateGenerator()

    # Define your requirements here. This should be a detailed description of what the Hygen template needs to do.

    requirements = """Generate a React component with props, state, and a basic render function. The component should be a functional
    component using React Hooks. """

    # Generate the Hygen template
    pred = generator(requirements)

    # Output the generated template
    print(f"Generated Hygen Template:\n{pred.template}")

    # Write pred.template to disk

    with open("template.ejs.t", "w") as f:
        f.write(pred.template)


if __name__ == "__main__":
    main()
