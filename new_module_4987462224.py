import dspy
from typer import Typer

app = Typer()


lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class BookDescToProductInfo(dspy.Module):
    """Converts book descriptions to product information"""
    
    def forward(self, book_desc):
        pred = dspy.Predict("book_desc -> product_info")
        
        result = pred(book_desc=book_desc).product_info
        return result

def main():

    book_desc = """If you’re a business leader, you already know that Lean Six Sigma is one of the most popular and powerful business tools in the world today. You also probably know that implementing the process can be more than a little challenging. This step-by-step guide shows you how to customize and apply the principles of Lean Six Sigma to your own organizational needs, giving you more options, strategies, and solutions than you’ll find in any other book on the subject. With these simple, proven techniques, you can:

* Assess your current business model and shape your future goals
* Plan and prepare a Lean Six Sigma program that’s right for your company
* Engage your leadership and your team throughout the entire process
* Align your LSS efforts with the culture and values of your business
* Develop deeper insights into your customer experience
* Master the art of project selection and pipeline management
* Tackle bigger problems and find better solutions
* Become more efficient, more productive, and more profitable

This innovative approach to the Lean Six Sigma process allows you to mold and shape your strategy as you go, making small adjustments along the way that can have a big impact. In this book, you’ll discover the most effective methods for deploying LSS at every level, from the leaders at the top to the managers in the middle to the very foundation of your company culture. You’ll hear from leading business experts who have guided companies through the LSS process―and get the inside story on how they turned those companies around. You’ll also learn how to use the latest, greatest management tools like Enterprise Kaizen, Customer Journey Maps, and Hoshin Planning. Everything you need to implement Lean Six Sigma―smoothly and successfully―is right here at your fingertips. Also included is a special chapter focusing exclusively on how to implement Lean Six Sigma in healthcare.

When it comes to running a business, there is no better way to improve efficiency, increase productivity, and escalate profits than Lean Six Sigma. And there is no better book on how to make it work than Innovating Lean Six Sigma."""  # Initialize your inputs here. Adjust as necessary.

    book_desc_to_product_info = BookDescToProductInfo()
    print(book_desc_to_product_info.forward(book_desc=book_desc))


# @app.command()
# def module_test(book_desc):
#     """Converts book descriptions to product information"""
#     book_desc_to_product_info = BookDescToProductInfo()
#
#     print(book_desc_to_product_info.forward(book_desc=book_desc))


if __name__ == "__main__":
    # app()
    main()