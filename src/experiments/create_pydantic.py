import pyperclip

from typetemp.template.smart_template import SmartTemplate
from utils.complete import LLMConfig
from utils.file_tools import write


class Template(SmartTemplate):
    source = """
You are a pydantic assistant. You convert plaintext into pydantic models
```plaintext
{{ prompt }}
```

```python
"""


async def render(prompt: str, max_tokens=2000):
    """Generate a pydantic based on a prompt."""
    return await Template(
        prompt=prompt, config=LLMConfig(max_tokens=max_tokens, stop=["```"])
    ).render()


async def main():
    content = await render(pyperclip.paste())
    print(content)
    filename = await write(content, extension="py")
    print(f"Wrote {filename}")


if __name__ == "__main__":
    import anyio

    anyio.run(main)
