from harvesting_utils.gpt_utils import extract_content, system_message, user_message, assistant_message
import openai
import json
from pydantic import BaseModel


class ComputesConstant(BaseModel):
    boolean: bool


def classify_formula(latex_string, api_key, constant='pi', temperature=0, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=api_key)

    messages = [
        system_message(f"You are a model that classifies whether a latex string is a formula that can be rearranged to calculate the constant {constant}. " + \
                       "Specifically, we are interested in continued fractions and series."),
        user_message(f"Is this a continued fraction or a series that can be rearranged to calculate the constant {constant}?\n\n{latex_string}")
        ]
    response = client.beta.chat.completions.parse(model=model,
                                                  messages=messages,
                                                  temperature=temperature,
                                                  response_format=ComputesConstant)
    messages.append(assistant_message(extract_content(response)))

    return json.loads(messages[-1]['content'])['boolean']
