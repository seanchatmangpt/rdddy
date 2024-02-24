import dspy
from typer import Typer

app = Typer()


lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class SubjectToBlog(dspy.Module):
    """This module takes in a subject and outputs a blog post."""
    
    def forward(self, subject):
        pred = dspy.Predict("subject -> blog_post")
        
        result = pred(subject=subject).blog_post
        return result

def main():

    subject = "Summer fun"  # Initialize your inputs here. Adjust as necessary.

    ds_py_module_template = SubjectToBlog()
    print(ds_py_module_template.forward(subject=subject))


@app.command()
def module_test(subject):
    """This module takes in a subject and outputs a blog post."""
    ds_py_module_template = SubjectToBlog()

    print(ds_py_module_template.forward(subject=subject))


if __name__ == "__main__":
    # app()
    main()
    