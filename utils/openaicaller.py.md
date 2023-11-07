# OpenAI Caller Script Reference

The provided script defines a class `openai_caller` that encapsulates methods to interact with OpenAI models using the official OpenAI module. It includes error handling and retry mechanisms. Below is the detailed explanation of the code along with its features and examples.

## Features

### 1. Chat Models & Text Models

The script supports the usage of various chat models and text models. The available models are defined in the `chat_models` and `text_models` lists. Currently, the text models are not supported and will raise a `NotImplementedError`.

### 2. Retry Mechanism

The script includes a retry mechanism to handle common API errors, timeouts, and rate limit issues. It will attempt to retry a call up to 10 times before failing.

### 3. Error Callback Function

An optional retry callback function (`recall_func`) can be provided to handle errors. This function should take a string argument representing the error message. If you do not care about the error message, you should  still define a dummy parameter for the function. This function will be called each time an error occurs. The error will always be printed to the terminal, regardless of whether a callback function is provided or not.

### 4. Colored Warnings & Errors

The script uses ANSI escape codes to colorize warning and error messages in the terminal, making them more visible.

### 5. Mandatory API Key

The `api_key` parameter is mandatory in each call to the OpenAI models.

### 6. Handling Too Many Tokens

The script ensures that the number of tokens in a request does not exceed the maximum allowed tokens for the specified model. If the number of tokens in the `messages` parameter exceeds the model's maximum token limit, the script will iteratively remove the first message from the `messages` array until the total token count is within the limit. This is done using the following logic:

```python
tokens = await num_tokens_from_messages(kwargs["messages"], kwargs["model"])
model_max_tokens = models_max_tokens[kwargs["model"]]
while tokens > model_max_tokens:
    kwargs["messages"] = kwargs["messages"][1:]
    print(f"{bcolors.BOLD}{bcolors.WARNING}Warning: Too many tokens. Removing first message.{bcolors.ENDC}")
    tokens = await num_tokens_from_messages(kwargs["messages"], kwargs["model"])
```

This feature ensures that the request complies with the token constraints of the chosen model and automatically adapts the input by removing the earliest messages if necessary.

## Methods

### `generate_response(error_call=None, **kwargs)`

This method is used to generate a response from the OpenAI models based on the provided parameters. It will figure out whether the model is a chat model or a text model and call the appropriate method. The parameters are as follows:

- `error_call`: An optional **FIRST POSITIONAL** argument **async** function that will be called if an error occurs. That function should take a string as an argument, representing the error message.
- The parameters passed to the OpenAI model. They must include the mandatory `api_key` parameter. Theese are the same parameters as defined in the standard OpenAI module, except for the addition of the `api_key` parameter. Any parameer here will be passed transparently to the OpenAI module.

### `chat_generate(recall_func, **kwargs)`

An internal method used to generate chat-based responses.

### `moderation(recall_func=None, **kwargs)`

This method is used for moderation purposes with the OpenAI models.

### `retryal_call(recall_func, callable)`

An internal method that implements the retry mechanism.

## Error Handling

Errors are handled through retries and callback functions:

- `APIError`: Not the user's fault. It will be retried.
- `Timeout`: Request timed out. It will be retried.
- `RateLimitError`: User is being rate-limited. It will be retried.
- `APIConnectionError`: Issue with the internet connection. It will be raised.
- `InvalidRequestError`: Issue with the request. It will be raised.
- `AuthenticationError`: Issue with the API key. It will be raised.
- `ServiceUnavailableError`: OpenAI API is not responding. It will be retried.

## Important Note

**Unlike the OpenAI module, in this script, the `api_key` parameter is NOT passed during the initialization of the `caller` class. Instead, it MUST be passed with each individual request.**

## Examples

### Example 1: Basic Chat Generation

This example demonstrates a simple chat generation without a retry callback function.

```python
from openaicaller import caller as openai
async def main():
    response = await openai.generate_response(
        api_key="sk-your-api-key",
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "ping"}]
    )
    print(response)

asyncio.run(main())
```

### Example 2: Using a Retry Callback Function

This example shows how to define and use a custom retry callback function with the chat generation.

```python
from openaicaller import caller as openai
def my_retry_function(error_message): #this function will be automatically called when ar error is gotten. You can define it and pass it as an argument. It is important to note that, if your function does not care of the error message, it should still take a dummy parameter as input
    print(f"An error occurred: {error_message}. Retrying...")

async def main():
    response = await openai.generate_response(
        error_call=my_retry_function,
        api_key="sk-your-api-key",
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "ping"}]
    )
    print(response)

asyncio.run(main())
```

### Example 3: Handling Moderation

This example demonstrates how to call the moderation method with the OpenAI caller class.

```python
from openaicaller import caller as openai
async def main():
    response = await openai.moderation(
        api_key="sk-your-api-key",
        # Additional parameters as needed
    )
    print(response)

asyncio.run(main())
```

## Conclusion

The `openai_caller` class provided in this script offers a robust way to interact with OpenAI models. By including the `api_key` parameter in each request and optionally providing a custom retry callback function, users can have granular control over the API interaction, including error handling and retry mechanisms. Make sure to follow the correct usage pattern, as it differs from the standard OpenAI module.