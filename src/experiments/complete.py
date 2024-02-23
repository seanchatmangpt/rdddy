from dataclasses import dataclass, field
from typing import Optional

import openai
import pyperclip
from openai import AsyncOpenAI
from openai.resources.chat import AsyncCompletions
from playwright.async_api import async_playwright

from utils.models import get_model


@dataclass
class LLMConfig:
    prompt: str = ""
    model: str = "3i"
    temperature: float = 0.0
    max_tokens: int = 250
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[list[str]] = field(default=None)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid config key: {key}")


def create(config: Optional[LLMConfig] = None, **kwargs):
    if config:
        config.update(**kwargs)
        prompt = config.prompt
        model = config.model
        temperature = config.temperature
        max_tokens = config.max_tokens
        top_p = config.top_p
        frequency_penalty = config.frequency_penalty
        presence_penalty = config.presence_penalty
        stop = config.stop
    else:
        prompt = kwargs.get("prompt", "")
        model = kwargs.get("model", "3i")
        temperature = kwargs.get("temperature", 0)
        max_tokens = kwargs.get("max_tokens", 250)
        top_p = kwargs.get("top_p", 1)
        frequency_penalty = kwargs.get("frequency_penalty", 0)
        presence_penalty = kwargs.get("presence_penalty", 0)
        stop = kwargs.get("stop", None)

    response = openai.completions.create(
        model=get_model(model),
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    return response.choices[0].text.strip()


async def count_response_buttons(page):
    # Count the number of specific buttons indicating response completion
    buttons = await page.query_selector_all('button[class*="group-hover:visible"]')
    return len(buttons)


async def extract_new_messages(page, last_count):
    # Get all messages by the assistant
    elements = await page.query_selector_all(
        'div[data-message-author-role="assistant"]'
    )
    new_messages = []

    for element in elements[-last_count:]:  # Process only the last few messages
        text_content = await page.evaluate("(element) => element.textContent", element)
        new_messages.append(text_content)

    return new_messages


async def process_new_responses(page, copy_code=False):
    last_button_count = await count_response_buttons(page)

    while True:
        current_button_count = await count_response_buttons(page)
        if current_button_count > last_button_count:
            new_message_count = current_button_count - last_button_count
            new_messages = await extract_new_messages(page, new_message_count)
            if copy_code:
                buttons = await page.query_selector_all("button:has-text('Copy code')")

                # Select the last button
                last_button = buttons[-1]

                # Perform actions with the last button (like clicking)
                await last_button.click()

                await asyncio.sleep(0.1)
                print(f"Copied code: {pyperclip.paste()}")
                return pyperclip.paste()

            return "\n".join(new_messages)
        await asyncio.sleep(1)


async def goto_chatgpt(prompt, copy_code=False, route=""):
    async with async_playwright() as p:
        # Connect to an existing instance of Chrome using the connect_over_cdp method.
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")

        # Retrieve the first context of the browser.
        default_context = browser.contexts[0]

        # Retrieve the first component in the context.
        page = default_context.pages[0]

        chat_gpt_url = f"https://chat.openai.com/{route}"

        await page.goto(chat_gpt_url)

        textarea = await page.query_selector("#prompt-textarea")
        await textarea.fill(prompt)

        await asyncio.sleep(1)

        # await component.click("#prompt-textarea")
        # await component.type("#prompt-textarea", prompt)
        await page.click('[data-testid="send-button"]')

        response = await process_new_responses(page, copy_code=copy_code)
        return response


async def acreate(*, config: Optional[LLMConfig] = None, **kwargs):
    if config:
        config.update(**kwargs)
        prompt = config.prompt
        model = config.model
        temperature = config.temperature
        max_tokens = config.max_tokens
        top_p = config.top_p
        frequency_penalty = config.frequency_penalty
        presence_penalty = config.presence_penalty
        stop = config.stop
    else:
        prompt = kwargs.get("prompt", "")
        model = kwargs.get("model", "3i")
        temperature = kwargs.get("temperature", 0)
        max_tokens = kwargs.get("max_tokens", 250)
        top_p = kwargs.get("top_p", 1)
        frequency_penalty = kwargs.get("frequency_penalty", 0)
        presence_penalty = kwargs.get("presence_penalty", 0)
        stop = kwargs.get("stop", None)

    model = get_model(model)

    # if model == "llama":
    #     from llama_cpp import Llama
    #
    #     llm = Llama(
    #         model_path="/Users/candacechatman/dev/models/codellama-7b.Q4_0.gguf"
    #     )
    #
    #     response = llm(
    #         model=model,
    #         prompt=prompt,
    #         temperature=temperature,
    #         max_tokens=max_tokens,
    #         top_p=top_p,
    #         frequency_penalty=frequency_penalty,
    #         presence_penalty=presence_penalty,
    #         stop=stop,
    #     )
    #     print(response)
    #     choice = response["choices"][0]
    #     return choice["text"]

    if model == "chatgpt":
        return await goto_chatgpt(
            prompt,
            copy_code=kwargs.get("copy_code", False),
            route=kwargs.get("route", "/"),
        )

    else:
        client = AsyncOpenAI()

        response = await client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
        )

        return response.choices[0].text.strip()


import asyncio
import json
import os
from dataclasses import dataclass
from time import sleep

from loguru import logger

# from fgn.completion.prompt_schemas import *
# from fgn.utils.llama_llm import LocalLlamaClient
# from fgn.utils.llm_operations import generate_filename
DEFAULT_PROMPT = ""
DEFAULT_SYS_MSG = "AI chatbot that converses like a LLM 7 AGI Hive-Mind simulator"
DEFAULT_MODEL = "4"
DEFAULT_MAX_RETRY = 5
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_INITIAL_WAIT = 1


def chat(
    prompt=DEFAULT_PROMPT,
    sys_msg=DEFAULT_SYS_MSG,
    msgs=None,
    funcs=None,
    model=DEFAULT_MODEL,
    max_retry=DEFAULT_MAX_RETRY,
    backoff_factor=DEFAULT_BACKOFF_FACTOR,
    initial_wait=DEFAULT_INITIAL_WAIT,
    raw_msg=False,
    write_path=None,
    mode="a+",
):
    """Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.

    Parameters:
        prompt (str, optional): The initial prompt for the chat conversation.
        sys_msg (str, optional): System message to guide the model's behavior.
        msgs (List[dict], optional): Previous messages in the conversation.
        funcs (List[Callable], optional): Custom functions to be applied on the response.
        model (str, optional): The OpenAI model to be used for completion.
        max_retry (int, optional): Maximum number of retries in case of an error.
        backoff_factor (float, optional): Multiplicative factor for exponential backoff between retries.
        initial_wait (float, optional): Initial wait time for the exponential backoff.
        raw_msg (bool, optional): Whether to include raw message in the response.
        write_path (str, optional): Directory or file path to write the response.
        mode (str, optional): File opening mode if writing response to file.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    retry = 0

    model = get_model(model)

    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)
            res = None

            if str(model) == "2":
                ...
                # llama = LocalLlamaClient()
                # res = llama.complete(prompt=prompt)
            elif funcs:
                res = get_response(
                    openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )
            else:
                res = get_response(
                    openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )

            write_response(mode, prompt, res, write_path)

            return res
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            # Increment the retry attempts
            retry += 1

            # If reached the maximum retry attempts, return the error message
            if retry > max_retry:
                raise ValueError(
                    f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
                )

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            logger.warning(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)


# Callable class version of chat using dataclass
@dataclass
class Chat:
    prompt = DEFAULT_PROMPT
    sys_msg = DEFAULT_SYS_MSG
    msgs = None
    funcs = None
    model = DEFAULT_MODEL
    max_retry = DEFAULT_MAX_RETRY
    backoff_factor = DEFAULT_BACKOFF_FACTOR
    initial_wait = DEFAULT_INITIAL_WAIT
    raw_msg = False

    def __call__(self, **kwargs):
        return chat(**kwargs)


async def achat(
    prompt=DEFAULT_PROMPT,
    sys_msg=DEFAULT_SYS_MSG,
    msgs=None,
    funcs=None,
    model=DEFAULT_MODEL,
    max_retry=DEFAULT_MAX_RETRY,
    backoff_factor=DEFAULT_BACKOFF_FACTOR,
    initial_wait=DEFAULT_INITIAL_WAIT,
    raw_msg=False,
    write_path=None,
    mode="a+",
):
    """Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    if funcs is None:
        funcs = []

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)
            res = None

            if funcs:
                res = get_response(
                    await AsyncCompletions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )
            else:
                res = get_response(
                    await openai.chat.completions.create(**params),
                    raw_msg=raw_msg,
                    funcs=funcs,
                )

            await awrite_response(mode, prompt, res, write_path)

            return res
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            retry += 1

            if retry > max_retry:
                raise ValueError(
                    f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
                )

            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            print(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            await asyncio.sleep(wait_time)


def write_response(mode, prompt, res, write_path):
    if write_path and os.path.isdir(write_path):
        # name = generate_filename(prompt)
        # logger.info(f"Creating file {name} in {write_path}")
        # write_path = os.path.join(write_path, generate_filename(prompt))
        pass
    if write_path:
        with open(write_path, mode) as f:
            f.write(f"{res}\n")


async def awrite_response(mode, prompt, res, write_path):
    if write_path and os.path.isdir(write_path):
        # name = generate_filename(prompt)
        # logger.info(f"Creating file {name} in {write_path}")
        # write_path = os.path.join(write_path, generate_filename(prompt))
        pass
    if write_path:
        with open(write_path, mode) as f:
            f.write(f"{res}\n")


def get_response(res, raw_msg, funcs):
    msg = res.get("choices")[0].get("message")

    if raw_msg:
        return msg

    func = msg.get("function_call")

    if func:
        try:
            func["arguments"] = json.loads(func.get("arguments", ""))
        except json.decoder.JSONDecodeError:
            pass
        # if it is not a valid json, {"name": "func_name", "arguments": {}}, throw a error
        if not isinstance(func, dict) or not isinstance(func.get("arguments"), dict):
            error_msg = f"Invalid function response from OpenAI API {msg}"
            logger.exception(error_msg)
            raise ValueError(error_msg)
        else:
            return func
    elif funcs and len(funcs) > 0:
        error_msg = f"Invalid function response from OpenAI API {msg}"
        logger.exception(error_msg)
        raise ValueError(error_msg)
    else:
        return msg.get("content", "").strip()


def _create_params(model, messages, funcs=None):
    parameters = {
        "model": get_model(model),
        "messages": messages,
    }
    if funcs:
        parameters["functions"] = funcs
        parameters["function_call"] = "auto"

    return parameters


def _create_messages(sys_msg, prompt, msgs):
    messages = []

    if msgs is None:
        messages = [
            {"role": "system", "content": sys_msg},
        ]

    if prompt:
        messages.append({"role": "user", "content": prompt})

    # Extend the messages list with the provided prompt, system message, and previous messages
    if msgs:
        messages.extend(msgs)

    return messages


import asyncio

prompt = """Certainly, let's break down the process of designing the command-line interface (CLI) with seven subcommands for creating ontologies, synthetic Voice of the Customer (VOC), and related tasks. We'll think step by step, considering the user's needs and the structure of the commands:

Command Structure: We start by defining the top-level command and its structure. In this case, the top-level command could be named "ontogen" (ontology generation). This command will have various subcommands for different ontology-related tasks.

Subcommands:

create-ontology: This subcommand will allow users to create a new ontology. Users can specify the ontology name, description, and other relevant details. This will involve defining the structure of the ontology.
add-concept: Users can use this subcommand to add concepts to an existing ontology. They will provide the concept name, description, and potentially relationships with other concepts.
define-voc: This subcommand is for defining the Voice of the Customer (VOC). Users can specify customer feedback, expectations, and requirements. This may involve categorizing VOC into different segments.
analyze-voc: Users can analyze the VOC data gathered using the previous subcommand. This may involve sentiment analysis, keyword extraction, and summarization.
generate-synthetic-voc: This subcommand can create synthetic VOC data for testing or training purposes. Users specify parameters such as the number of feedback entries, sentiment distribution, and topics.
link-voc-to-ontology: This command links the VOC data to concepts in the ontology. Users can specify which concepts in the ontology are related to specific VOC entries.
export-ontology: Allows users to export the ontology in a specific format (e.g., OWL, RDF) for use in other applications.
Options and Arguments:

For each subcommand, define the specific options and arguments required. For example, the "create-ontology" subcommand may require options like "--ontology-name" and "--description."
Help Messages:

Create synthetic help messages for each subcommand to guide users on how to use them effectively. Mention the available options and their descriptions.
Validation:

Implement validation checks to ensure that user-provided data adheres to the required format and constraints. For example, ontology names should be unique, and VOC data should be properly formatted.
Error Handling:

Define how errors and exceptions will be handled and communicated to the user. Ensure that error messages are informative and help users troubleshoot issues.
Testing:

Develop a testing strategy to validate that each subcommand works as intended. This may involve creating test cases for various scenarios.
Documentation:

Document the usage of each subcommand, along with examples, in a user-friendly guide or manual.
User Experience:

Consider the overall user experience, making the CLI as intuitive as possible. Provide feedback and prompts to guide users through the process.
Usability Testing:

Conduct usability testing with potential users to gather feedback and make improvements based on their input.
Extensibility:

Think about how the CLI can be extended in the future. Can additional subcommands or features be easily added to accommodate evolving requirements?
Performance:

Optimize the CLI's performance, especially for tasks that involve processing large amounts of data or complex ontologies.
By carefully planning and designing each subcommand and considering user needs, you can create a powerful and user-friendly CLI for ontology generation, VOC management, and related tasks."""


async def main():
    client = AsyncOpenAI()

    await acreate(
        prompt="Convert the CLI to Typer and use jinja withing the echo",
        model="chatgpt",
    )


if __name__ == "__main__":
    asyncio.run(main())
