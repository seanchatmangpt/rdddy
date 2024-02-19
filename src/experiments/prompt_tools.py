import functools
import itertools
import time
from collections.abc import Iterable
from typing import Optional

# import anyio
from icontract import ensure, require

from utils.complete import acreate
from utils.models import instruct_models, ok_models


def timer(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds to run.")
        return result

    return wrapper


# 1. Model Selection
def model_generator(models: list[str]):
    """A generator that yields models in a round-robin fashion using itertools.cycle."""
    return itertools.cycle(models)


# 3. OpenAI Call
async def call_openai(
    prompt: str, model_name: str, max_tokens: int = 50, temperature: float = 0.7
) -> str:
    return await acreate(
        prompt=prompt, model=model_name, max_tokens=max_tokens, temperature=temperature
    )


# 4. Timing and Logging
async def timed_openai_call(
    prompt: str,
    item: str,
    model_name: str,
    max_tokens: int = 50,
    temperature: float = 0.7,
) -> str:
    start_time = time.time()
    response = await call_openai(prompt, model_name, max_tokens, temperature)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f'Generated response for "{item[:30]}..." using {model_name} in {elapsed_time:.2f} seconds.'
    )
    return response


# 5. Concurrent Execution
async def prompt_map(
    prompts_iterable: Iterable[str],
    base_prompt: str = "",
    max_tokens: int = 50,
    model_list: Optional[list[str]] = None,
    prefix: str = "",
    suffix: str = "",
    stop: Optional[list[str]] = None,
    temperature: float = 0.0,
) -> list[str]:
    model_gen = model_generator(model_list or instruct_models)
    responses = []

    async def generate_response(index: int, item: str) -> None:
        model_name = next(model_gen)
        prompt = f"{base_prompt} {prefix} {item} {suffix}"
        print(f"Prompt: {prompt}")
        response = await acreate(
            prompt=prompt,
            model=model_name,
            max_tokens=max_tokens,
            stop=stop,
            temperature=temperature,
        )
        print(f"Response: {response}")
        responses.append((index, response))

    async with anyio.create_task_group() as tg:
        for index, item in enumerate(prompts_iterable):
            tg.start_soon(generate_response, index, item)

    # Sort the responses by index
    sorted_responses = [resp for _, resp in sorted(responses)]

    return sorted_responses


async def batched_prompt_map(
    prompts_iterable: Iterable[str],
    base_prompt: str = "",
    max_tokens: int = 50,
    model_list: Optional[list[str]] = None,
    prefix: str = "",
    suffix: str = "",
    stop: Optional[list[str]] = None,
    temperature: float = 0.0,
    batch_size: int = 5,
):
    """This function takes a batch size and kwargs and returns a list of responses."""
    responses = []
    for i in range(0, len(prompts_iterable), batch_size):
        batch = prompts_iterable[i : i + batch_size]
        batch_responses = await prompt_map(
            prompts_iterable=batch,
            base_prompt=base_prompt,
            max_tokens=max_tokens,
            model_list=model_list,
            prefix=prefix,
            suffix=suffix,
            stop=stop,
            temperature=temperature,
        )
        responses.extend(batch_responses)
    return responses


async def prompt_dict(
    prompts_dict: dict[str, str],
    base_prompt: str = "",
    max_tokens: int = 50,
    model_list: Optional[list[str]] = None,
    prefix: str = "",
    suffix: str = "",
    stop: Optional[list[str]] = None,
    temperature: float = 0.0,
) -> dict[str, str]:
    model_gen = model_generator(model_list or instruct_models)
    responses = {}

    async def generate_response(key: str, item: str) -> None:
        model_name = next(model_gen)
        prompt = f"{base_prompt} {prefix} {item} {suffix}"
        response = await acreate(
            prompt=prompt,
            model=model_name,
            max_tokens=max_tokens,
            stop=stop,
            temperature=temperature,
        )
        responses[key] = response

    async with anyio.create_task_group() as tg:
        for key, item in prompts_dict.items():
            tg.start_soon(generate_response, key, item)

    return responses


# [Rest of your functions and example usage]

# Example models and usage:

# example_prompt = "Translate the following text into French"
# text_list = ["Hello, how are you?", "I love programming", "Thank you very much", "I am doing well", "I am doing poorly"]
# start_time = time.time()
# responses_best_models = await prompt_map(example_prompt, text_list, 50)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Responses: in {elapsed_time:.2f} seconds.", responses_best_models)


async def prompt_filter(
    base_prompt: str,
    prompts_iterable: Iterable[str],
    model_list: Optional[list[str]] = None,
    max_tokens: int = 50,
) -> list[str]:
    """This function takes a base prompt and filters an iterable based on responses from OpenAI.

    Args:
        base_prompt (str): The base prompt for generating boolean responses.
        prompts_iterable (iterable): An iterable (e.g., list, tuple) of strings to be filtered.
        model_list (List[str]): List of models to be used in round-robin fashion. If None, defaults to instruct_models.
        max_tokens (int): The maximum number of tokens in each response.

    Returns:
        list: A list of items from the iterable that pass the condition specified by the prompt.
    """
    filterable = [
        f"Create a Python bool based on the prompt: '{prompt}'."
        f"\nPlease complete the following code block:\n"
        f"```python\n"
        f"from typing import bool\n"
        f"# {prompt} \n"
        f"perfect_bool: bool = "
        for prompt in prompts_iterable
    ]

    responses = await prompt_map(filterable, base_prompt, max_tokens, model_list)
    results = [
        item
        for item, resp in zip(prompts_iterable, responses, strict=False)
        if "true" in resp.lower()
    ]

    return results


filter_prompt = "Is the statement in quotes positive?"

statements = [
    "'The sun is not shining today.'",
    "'I failed the test.'",
    "'The flowers are blooming.'",
    "'The weather is gloomy.'",
    "'I aced the exam!'",
]

# filtered_statements = anyio.run(prompt_filter, filter_prompt, statements)
# print("Positive statements:", filtered_statements)

from collections.abc import Callable, Iterable

import anyio


async def prompt_reduce(
    base_prompt: str,
    prompts_iterable: Iterable[str],
    reducer: Callable[[list[str]], list[str]],
    model_list: Optional[list[str]] = None,
    max_tokens: int = 50,
) -> list[str]:
    """Uses the prompt_map function to collect responses and then reduces the responses based on a given reducer function.

    Args:
        base_prompt (str): The base prompt for generating responses.
        prompts_iterable (Iterable[str]): An iterable of strings to generate responses for.
        reducer (Callable[[List[str]], List[str]]): A function to reduce the list of generated responses.
        model_list (List[str]): Optional; list of models to use. If None, uses a default.
        max_tokens (int): Optional; max tokens for each response.

    Returns:
        A reduced list of responses based on the reducer function.
    """
    # First, we generate the responses based on the iterable and the base prompt
    responses = await prompt_map(prompts_iterable, base_prompt, max_tokens, model_list)

    # Then, we reduce the list of responses using the reducer function
    return reducer(responses)


async def create_python_class_from_function_names(
    class_name: str, function_names: list[str]
) -> str:
    """Creates a Python class string from a list of function names using OpenAI for method content."""
    function_strs = []
    for fname in function_names:
        prompt = f"Generate Python code for a class method named {fname}."
        implementation_details = await call_openai(
            prompt, "text-davinci-002", max_tokens=50
        )  # You can use your preferred model
        function_strs.append(
            f"    def {fname}(self, *args, **kwargs):\n        {implementation_details.strip()}"
        )

    functions_str = "\n".join(function_strs)
    return f"class {class_name}:\n{functions_str}"


@require(lambda x_prompts_iterable: all(isinstance(x, str) for x in x_prompts_iterable))
@require(lambda y_prompts_iterable: all(isinstance(y, str) for y in y_prompts_iterable))
@require(lambda max_tokens: isinstance(max_tokens, int) and max_tokens > 0)
@ensure(lambda result: isinstance(result, list))
@timer
async def prompt_matrix(
    x_prompts_iterable: Iterable[str],
    y_prompts_iterable: Iterable[str],
    base_prompt: str = "",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 50,
) -> list[str]:
    responses = []

    async def generate_response(index, prompt) -> None:
        response = await acreate(
            prompt=prompt, model=model, max_tokens=max_tokens, temperature=temperature
        )
        responses.append((index, response))

    prompts = [
        f"{base_prompt} {x_prompt} {y_prompt}"
        for x_prompt in x_prompts_iterable
        for y_prompt in y_prompts_iterable
    ]

    async with anyio.create_task_group() as tg:
        for index, item in enumerate(prompts):
            tg.start_soon(generate_response, index, item)

    sorted_responses = [resp for _, resp in sorted(responses)]

    return sorted_responses


# Example usage
async def main():
    x_prompts = ["Create a python function for", "Create a python class for"]
    y_prompts = ["sorting an array", "finding the maximum element"]
    result = await prompt_matrix(x_prompts, y_prompts, "You are an agent", max_tokens=50)
    print(result)


# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.


class Verifiers:
    """A class designed to judge the validity of thoughts and answers produced by language models. This verifier can assess if a thought is a valid form of reasoning for deriving an answer from a question and if the answer is correct."""

    def __init__(self):
        pass

    async def generate_solutions(self, problem: str) -> list[str]:
        """Generates solutions for a given problem leveraging OpenAI prompts, inspired by the idea of adding explicit "thought" variables to improve model performance."""
        base_prompt = f"Given the concept of 'Self-Taught Reasoner' and 'rationale generation with rationalization', propose solutions for: {problem}"
        solutions = await prompt_map(
            [problem for _ in range(5)],
            base_prompt,
            model_list=ok_models,
            max_tokens=300,
        )  # Simulating 5 potential solutions
        print("Generated solutions:", solutions)
        return solutions

    async def verify_solutions(self, solutions: list[str]) -> list[str]:
        """Validates the provided solutions based on the concept of "verification" labels, which determine if a solution is derived through valid reasoning."""
        base_prompt = "Is this useful to an expert?"
        verified_solutions = await prompt_filter(base_prompt, solutions)
        return verified_solutions

    async def pick_best_solution(self, verified_solutions: list[str]) -> str:
        """Chooses the best solution among the verified ones, leveraging the notion of ranking solutions by their validity."""
        base_prompt = "Using the idea of 'N-step reasoning' and 'verification model', identify the best solution among the following verified solutions:"
        combined_solutions = "\n".join(verified_solutions)
        best_solution = await prompt_map([combined_solutions], base_prompt)
        return best_solution[0]  # Return the first item as it should contain the best solution


# async def main():
#     verifier = Verifiers()
#     solutions = await verifier.generate_solutions(
#         "How to improve code readability in a DDD abstraction framework? Expert level Opinions only with Python examples. Out of the box ideas\n```python\n# Code examples\n```"
#     )
#     verified_solutions = await verifier.verify_solutions(solutions)
#     best_solution = await verifier.pick_best_solution(verified_solutions)
#     print("Best Solution:", best_solution)


if __name__ == "__main__":
    anyio.run(main)
    # Example usage
    # domain_statements = [
    #     "The user should be able to deposit money into their account.",
    #     "The user must be able to withdraw funds.",
    #     "The account should display the current balance.",
    #     "The account should allow setting a preferred currency.",
    #     "The account should allow setting a preferred language.",
    #     "Loans should be approved within 24 hours.",
    # ]

    # function_names_base_prompt = (
    #     "Based on the following statement by a domain expert, "
    #     "suggest a suitable pythonic function name. Avoid the words get or set:"
    # )

    # Here you'll call the prompt_reduce function with the necessary parameters. For demonstration, we simulate it.
    # function_names = anyio.run(prompt_reduce, function_names_base_prompt, domain_statements, extract_function_names)
    #
    # print("Extracted function names:", function_names)
