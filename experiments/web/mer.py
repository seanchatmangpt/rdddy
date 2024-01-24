import asyncio

import streamlit as st
from streamlit_mermaid import st_mermaid

from typetemp.template.typed_template import TypedTemplate
from utils.complete import acreate
from utils.file_tools import write
from utils.models import get_model

create_mermaid_template = """
Objective:
Transform the given input (Mermaid diagram code) into a rendered Mermaid diagram image.
Make sure to capture the nuances of the input in the output. The most elegant solution is the one that is the most generalizable.

```prompt
{{prompt}}
```

"""


async def create_mermaid(prompt, md_type="mermaid", model=None, filepath=None):
    """
    Generate a Mermaid diagram image based on the given Mermaid diagram code.
    """
    create_prompt = TypedTemplate(source=create_mermaid_template, prompt=prompt)()

    return await __create(
        prompt=create_prompt,
        filepath=filepath,
        md_type=md_type,
        model=model,
    )


async def __create(
    prompt,
    md_type="text",
    max_tokens=2500,
    model=None,
    filepath=None,
    temperature=0.0,
    stop=None,
    suffix="",
):
    model = get_model(model)

    create_prompt = TypedTemplate(
        source=__create_template, prompt=prompt, md_type=md_type, suffix=suffix
    )()

    # # print(create_prompt)

    result = await acreate(
        prompt=create_prompt,
        model=model,
        stop=["```"] + (stop or []),
        max_tokens=max_tokens,
        temperature=temperature,
    )
    # # print(f"Prompt: {result}")
    # # print(f"Result: {result}")

    if filepath:
        await write(contents=result, filename=filepath)

    return result


__create_template = """
{{prompt}}
```{{md_type}}
{{suffix}}
"""

st.set_page_config(
    page_title="Streamlit Mermaid Example",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Streamlit Mermaid Example")

st.markdown(
    """
    ## Mermaid
    [Mermaid](https://mermaid-js.github.io/mermaid/#/) is a diagramming and charting tool that uses text-based descriptions to render diagrams.
    """
)

st.markdown(
    """
    ### Flowchart
    """
)

# mermaid_code = """graph TD;
#     A-->B;
#     A-->C;
#     B-->D;
#     C-->D;
# """
#
# mermaid_code = st.text_area("Mermaid Code", mermaid_code)
#
# st_mermaid(mermaid_code, height="500px")

# Add a text input for the prompt
mermaid_prompt = st.text_area("Mermaid Prompt", "")

# Add a button to trigger the conversion
if st.button("Convert to Mermaid"):
    st.write("Converting...")

    # Run the conversion asynchronously
    async def async_conversion():
        mermaid_code = await create_mermaid(mermaid_prompt)
        print(mermaid_code)
        st_mermaid(mermaid_code, height="500px")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_conversion())
    st.write("Conversion complete!")
