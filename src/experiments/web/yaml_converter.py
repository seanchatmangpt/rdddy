import asyncio

import streamlit as st

from experiments import create_yaml


# Define the Streamlit component function
def yaml_converter(yaml_prompt):
    # Add a button to trigger the conversion
    if st.button("Convert to YAML"):
        st.write("Converting...")

        # Run the conversion asynchronously
        async def async_conversion():
            yaml_data = await create_yaml.render(yaml_prompt)
            st.code(yaml_data, language="yaml")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_conversion())
        st.write("Conversion complete!")


# Create a Streamlit component instance
# def yaml_converter_component_func(yaml_prompt):
#     with st.container():
#         yaml_converter(yaml_prompt)

# Create a Streamlit app to demonstrate the component
if __name__ == "__main__":
    st.title("YAML Converter Streamlit Component")
    yaml_prompt = st.text_area("YAML Prompt", "")
    yaml_converter(yaml_prompt)
