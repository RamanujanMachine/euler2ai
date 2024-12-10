# this file will contain helper functions for the gpt extraction mechanism

# one example is a function that got can decide to call that extracts sequences from the first terms of continued fractions
# parts of the function:
# 1. identify continued fraction and its recursive scheme
# 2. extract the first terms of a
# 3. extract the first terms of b
# 4. fit polynomials to each of these


from arxiv_dataset_filter_utils import cf_patterns
import json
from pydantic import BaseModel, Field
from enum import Enum
from typing import List
import sympy as sp
import copy
import re

import openai
import tiktoken


def openai_api_key():
    return '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'


OPENAI_API_KEY = openai_api_key()


def extract_content(gpt_response):
    return json.loads(gpt_response.model_dump_json())['choices'][0]['message']['content']


def system_message(message):
    return {"role": "system", "content": message}


def user_message(message):
    return {"role": "user", "content": message}


def assistant_message(message):
    return {"role": "assistant", "content": message}


def prompt_and_append_messages():
    pass


###########
# Currently being used:
class GPTIsFormula(BaseModel):
    boolean: bool
    # explanation: str = Field(description="Explanation why the formula can be used to calculate the constant.")


def classify_formula(latex_string, constant='pi', temperature=0, api_key=OPENAI_API_KEY, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=api_key)

    messages = [
        system_message(f"You are a model that classifies whether a latex string is a formula that can be rearranged to calculate the constant {constant}. " + \
                       "Specifically, we are interested in continued fractions, series or products. Keep all answers concise and accurate."),
        user_message(f"Is this a continued fraction, series or product that can be rearranged to calculate the constant {constant}? {latex_string}")
        ]
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, response_format=GPTIsFormula)
    messages.append(assistant_message(extract_content(response)))

    return json.loads(messages[-1]['content'])['boolean']
###########


# Count tokens and estimate cost
# tiktoken


def count_tokens(string):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(string))


def estimate_cost(messages):
    USER_COST = 2.5 / 10**6
    SYSTEM_COST = USER_COST
    ASSISTANT_COST = 10 / 10**6

    return sum([USER_COST * count_tokens(m['content']) if m['role'] == 'user' else \
                SYSTEM_COST * count_tokens(m['content']) if m['role'] == 'system' else \
                ASSISTANT_COST * count_tokens(m['content']) for m in messages])


# Structured response classes


class GPTFormulaBool(BaseModel):
    boolean: bool
    explanation: str = Field(description="Explanation why the formula is either a continued fraction or a series.")


class FormulaType(Enum):
    CONTINUED_FRACTION = 'cf'
    SERIES = 'series'
    NEITHER = 'neither'


class GPTFormulaClassification(BaseModel):
    formula_type: FormulaType
    explanation: str = Field(description="Explanation why the formula type is what it is.")


class GPTFormulaValue(BaseModel):
    value: str
    explanation: str = Field(description="Explanation why the formula value is what it is.")


class GPTCF(BaseModel):
    an: str
    bn: str
    unknowns: List[str]
    explanation: str = Field(description="Explanation why an is the partial denominator, why bn is the partial numerator, and why each unknown is an unknown.")


class GPTSeries(BaseModel):
    summand: str
    dummy_var: str
    start: str
    unknowns: List[str]
    explanation: str = Field(description="Explanation why summand is the summand of the series, why dummy_var is the dummy variable iterated over, " + \
                            "why start is the starting value for the dummy variable and why each unknown is an unknown.")
  

class GPTSympyExpression(BaseModel):
    expression: str
    explanation: str = Field(description="Explanation why the new string is the proper sympy expression for the original string.")


class GPTBool(BaseModel):
    boolean: bool
    explanation: str = Field(description="Explanation why the answer is either true or false.")


# GPT


def correct_to_sympy_expression(string, messages=[], max_iters=3, verbose=False, temperature=0, api_key=OPENAI_API_KEY, model="gpt-4o-mini", max_tokens=200):
    """
    Tries to correct a string to be a proper sympy expression.
    Args:
    max_iters: maximum number of iterations allowed for GPT to correct itself.
    """
    client = openai.OpenAI(api_key=api_key)

    i = 0
    expression_is_clean = False

    while not expression_is_clean and i <= max_iters:
        if verbose:
            print(f'Expression, attempt {i}: {string}')
        try:
            formula_sympy = sp.sympify(string)
            expression_is_clean = True
            if verbose:
                print('Expression is now clean.')
            break
        except Exception as e:
            i += 1
            if verbose:
                print(f'Error: {e}')
            messages.append(user_message(f"The last attempt was not proper sympy: {e}. Try again. Extract the expression in this string and write it in proper sympy format: {string}"))
            response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTSympyExpression)
            messages.append(assistant_message(extract_content(response)))
            string = json.loads(messages[-1]['content'])['expression']

    return string, messages, expression_is_clean


def extract_formula(latex_string, verbose=True, constant='pi', api_key=OPENAI_API_KEY,
                    temperature=0, max_iters=1, use_gpt_4o_for_all=False, max_tokens=200):
    """
    The model used for symbolic formula extraction is 'gpt-4o', compared with 'gpt-4o-mini'
    which is used otherwise throughout the pipeline. 'gpt-4o' is much better at generalizing
    patterns in the data to write the correct symbolic expressions.
    Args:
        max_iters: maximum number of iterations allowed for GPT to correct itself.
    """
    if use_gpt_4o_for_all:
        model = "gpt-4o"
    else:
        model = "gpt-4o-mini"

    client = openai.OpenAI(api_key=api_key)

    messages = [
        system_message(f"You are a model that classifies whether a latex string is a formula that can be rearranged to calculate the constant {constant}. " + \
                        "Specifically, we are interested in three types of formulas: continued fractions and series (infinite sums). Keep all answers concise and accurate."),
        user_message(f"Is this formula a continued fraction or a series that can be rearranged to calculate the constant {constant}? {latex_string}")
        ]

    # is a formula?
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaBool)
    messages.append(assistant_message(extract_content(response)))

    formula_bool = json.loads(messages[-1]['content'])['boolean']

    if not formula_bool:
        if verbose:
            print(f'Not a formula.')
        return {'type': ''}, messages
    

    # what type?
    messages.append(user_message(f"Is this formula a continued fraction or series? {latex_string}"))
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaClassification)
    messages.append(assistant_message(extract_content(response)))

    formula_type = json.loads(messages[-1]['content'])['formula_type']

    # expected type
    expected_formula_type = ''
    # cf_regular_expressions = '(' + r'\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})*\s*}' + '|' + \
                                    # r'\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})*\s*}' + ')'
    # if 'sum' in latex_string:
    #     expected_formula_type = 'series'
    # elif re.findall(cf_patterns(), latex_string) or 'cf' in latex_string:
    #     expected_formula_type = 'cf'
    # if expected_formula_type:
    #     assert formula_type == expected_formula_type, f'Expected {expected_formula_type}, got {formula_type}'

    # identify the value
    messages.append(user_message(r"What is the value of this formula? It should be explicit (a closed form) and on one side of the equation. " + \
                                    r"Example: the string '$$\forall z \in \mathbb{C}: \quad  1+\frac{1\cdot(2\cdot z-1)}{4+\frac{2\cdot(2\cdot z-3)}" + \
                                    r"{7+\frac{3\cdot(2\cdot z-5)}{10+\frac{4\cdot(2\cdot z-7)}{13+..}}}} = \frac{2^{2\cdot z +1}}{\pi\binom{2\cdot z}{z}}$$' " + \
                                    r"has value: '2**(2*z + 1)/(pi*binomial(2*z, z))'. " + \
                                r"Another example: the string '\pi=\frac{22}{7} -24\sum_{n=2}^\infty \frac{(-1)^{n}}{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}' " + \
                                r"has value: 'pi'. "  + \
                                f"Extract the value and write it in sympy format: {latex_string}"))
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaValue)
    messages.append(assistant_message(extract_content(response)))

    formula_value = json.loads(messages[-1]['content'])['value']

    # clean the value (iteratively)
    formula_value, messages, value_is_proper_sympy = correct_to_sympy_expression(formula_value, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model=model)

    # identify formula components + unknowns
    if formula_type == 'cf':
        messages.append(user_message(f"Identify the partial denominator an, partial numerator bn, and any unknown variables (other than the depth n) " + \
                                    f"that appear in the the continued fraction. " + \
                                    "Extract each of them and write them as proper sympy expressions as a function of depth n. " + \
                                    "Example: the string '$$\forall z \in \mathbb{C}: \quad  1+\frac{1\cdot(2\cdot z-1)}{4+\frac{2\cdot(2\cdot z-3)}" + \
                                    "{7+\frac{3\cdot(2\cdot z-5)}{10+\frac{4\cdot(2\cdot z-7)}{13+..}}}} = \frac{2^{2\cdot z +1}}{\pi\binom{2\cdot z}{z}}$$' " + \
                                    "has an: '3*n + 1', bn: 'n*(2*z - (2*n - 1))', unknowns: ['z']" + \
                                    f"The continued fraction: {latex_string}"))
        response = client.beta.chat.completions.parse(model="gpt-4o", messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTCF)
        messages.append(assistant_message(extract_content(response)))

    elif formula_type == 'series':
        messages.append(user_message(f"Identify the summand, dummy variable, start value for the dummy variable and any unknown variables (other than the dummy variable) " + \
                                    f"that appear in the series: {latex_string}. Extract each of them and write them as proper sympy expressions. " + \
                                    "Example: the string '\pi=\frac{22}{7} -24\sum_{n=2}^\infty \frac{(-1)^{n}}{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}' " + \
                                    "has summand: '(-1)**n / ((2n + 1)*(2*n + 2)*(2*n + 3)*(2*n + 4)*(2*n + 5))', dummy variable: 'n', start: '2', unknowns: [] " + \
                                    f"The series: {latex_string}"))
        response = client.beta.chat.completions.parse(model="gpt-4o", messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTSeries)
        messages.append(assistant_message(extract_content(response)))

    formula_info = json.loads(messages[-1]['content'])

    # clean the formula components + unknowns
    info_is_proper_sympy = copy.deepcopy(formula_info)
    del info_is_proper_sympy['explanation']
    for key, val in formula_info.items():
        if key == 'explanation':
            continue
        if key == 'unknowns':
            proper_sympy_val = copy.deepcopy(val)
            for i, string in enumerate(val):
                string, messages, sympy_boolean = correct_to_sympy_expression(string, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model=model)
                val[i] = string
                proper_sympy_val[i] = sympy_boolean
        else:
            val, messages, proper_sympy_val = correct_to_sympy_expression(val, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model=model)
        
        formula_info[key] = val
        info_is_proper_sympy[key] = proper_sympy_val

    if verbose:
        print(f'{formula_bool}')
        print(f'{formula_type}')
        print(f'{formula_value}')

    # join dictionaries
    formula_info['value'] = formula_value
    is_proper_sympy = {}
    for item in info_is_proper_sympy.items():
        is_proper_sympy[item[0]] = item[1]
    is_proper_sympy['value'] = value_is_proper_sympy

    return {'type': formula_type, 'info': formula_info, 'is_proper_sympy': is_proper_sympy}, messages
