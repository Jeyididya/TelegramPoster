import openai

from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv('.env'))
api_key = config('CHA_API')
# Set your OpenAI API key
openai.api_key = api_key


def generate_image_prompt(quote):
    prompt = f"Generate an image that depicts the following quote: '{quote}'"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()


# Example quote
quote = "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment."

# Generate image prompt based on the quote
image_prompt = generate_image_prompt(quote)
print(image_prompt)
