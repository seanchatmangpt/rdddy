from typetemp.template.smart_template import SmartTemplate
from utils.complete import LLMConfig


class Template(SmartTemplate):
    source = """
You are a yaml assistant. A hyperdetailed assistant prompt is a tool that helps users generate highly detailed content. This prompt is designed to assist users in converting their content into YAML format. YAML, or ".

```prompt
{{ prompt }}
```

"""


async def create_yaml(prompt: str, max_tokens=2000):
    """Generate a yaml based on a prompt."""
    return await Template(
        prompt=prompt, config=LLMConfig(max_tokens=max_tokens)
    ).render()


async def main():
    prompt = input("Enter your prompt: ")
    content = await create_yaml(prompt)
    print(content)


if __name__ == "__main__":
    import anyio

    anyio.run(main)
