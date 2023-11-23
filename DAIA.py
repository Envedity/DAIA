from DAIA_GPT4V.run import run
from config import openai_api_key


def main(key: str = None) -> None:
    # Checking API Key
    if not key or len(key) <= 0 or key == "":
        input_api_key = ""

        while input_api_key == "":
            input_api_key = input("Enter Your API Key: ")

        # Saving API Key
        with open(".env", "a") as env_file:
            env_file.write(f"\nOPENAI_KEY={input_api_key}")
            env_file.close()

        key = input_api_key

    # User Interaction
    try:
        option = int(
            input(
                "\nOptions\n[1] DAIA_GPT-4-with-Vision\n[2] DAIA_Continues\n\nSelect Option: "
            )
        )

    except ValueError:
        print("Please enter a number.")
        exit()

    match option:
        case 1:
            return run(api_key=key)

        case 2:
            return print("Currently Unavaiable.")

        case _:
            return print("Invalid Option.")


if __name__ == "__main__":
    main(openai_api_key)
