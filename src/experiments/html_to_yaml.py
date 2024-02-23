import anyio
from bs4 import BeautifulSoup
from pydantic import BaseModel

from utils.yaml_tools import YAMLMixin


class HTMLTag(BaseModel, YAMLMixin):
    tag_name: str
    attributes: dict = {}
    inner_text: str = ""
    selector: str = ""
    children: list["HTMLTag"] = []

    def __str__(self):
        return self.selector


def export_html_to_yaml(yaml_file_path):
    # Get HTML content from clipboard
    # html_content = pyperclip.paste()
    with open("source.html", encoding="utf-8") as f:
        html_content = f.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find elements with "aria" attributes but skip elements with aria-hidden="true"
    elements_with_aria = soup.find_all(
        lambda tag: any(attr.startswith("aria-") for attr in tag.attrs)
        and not ("aria-hidden" in tag.attrs and tag.attrs["aria-hidden"] == "true")
    )

    # Generate CSS selectors and include inner text for elements with "aria" attributes
    selectors_with_text = []
    parent = HTMLTag(tag_name="html")

    for element in elements_with_aria:
        tag = HTMLTag(tag_name=element.name)
        aria_attributes = [attr for attr in element.attrs if attr.startswith("aria-")]
        selector = element.name
        for attr in aria_attributes:
            aria_value = element.get(attr)
            selector += f'[{attr}="{aria_value}"]'
            tag.selector = selector
            tag.attributes[attr] = aria_value
        inner_text = element.get_text(
            strip=True
        )  # Get inner text without extra whitespace
        if inner_text:
            selector += f'{{text: "{inner_text}"}}'
        selectors_with_text.append(selector)
        print(tag)
        parent.children.append(tag)

    print(parent)
    parent.to_yaml(yaml_file_path)


async def main():
    # Define the path to the YAML file where selectors will be saved
    yaml_file_path = "selectors.yaml"

    # Call the function to export HTML to YAML
    # export_html_to_yaml(yaml_file_path)

    selectors = [str(tag) for tag in HTMLTag.from_yaml(yaml_file_path).children]

    # Sort by longest string first
    selectors = sorted(selectors, reverse=True)

    # Filter out duplicates
    unique = set(selectors)

    print(unique)

    # result = await acreate(prompt=f"Sort by most likely to be chosen by user: {selectors}. Include top 10", max_tokens=500)
    # print(result)
    # await write(contents=result, filename="html_sort.txt")


if __name__ == "__main__":
    anyio.run(main)
