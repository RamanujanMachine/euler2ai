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


# Count tokens and estimate cost
# tiktoken


def count_tokens(string):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(string))


def count_tokens_for_messages(messages):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return {'system': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'system']),
            'user': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'user']),
            'assistant': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'assistant'])}


def estimate_cost(messages=[], token_counts={}):
    SYSTEM_COST = 2.5 / 10**6
    USER_COST = 2.5 / 10**6
    ASSISTANT_COST = 10 / 10**6

    if not token_counts:
        token_counts = count_tokens_for_messages(messages)

    return SYSTEM_COST * token_counts['system'] + USER_COST * token_counts['user'] + ASSISTANT_COST * token_counts['assistant']


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


# Structured response classes


class GPTFormulaBool(BaseModel):
    boolean: bool
    explanation: str = Field(description="Explanation why the formula is a continued fraction or a series or an infinite product.")


class FormulaType(Enum):
    CONTINUED_FRACTION = 'cf'
    SERIES = 'series'
    PRODUCT = 'product'
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
    explanation: str = Field(description="Explanation why an is the partial denominator of the continued fraction, why bn is the partial numerator" + \
                              "and why each unknown is an unknown.")


class GPTSeries(BaseModel):
    summand: str
    dummy_var: str
    start: str
    unknowns: List[str]
    explanation: str = Field(description="Explanation why summand is the summand of the series, why dummy_var is the dummy variable iterated over, " + \
                            "why start is the starting value for the dummy variable and why each unknown is an unknown.")
  

class GPTProduct(BaseModel):
    factor: str
    dummy_var: str
    start: str
    unknowns: List[str]
    explanation: str = Field(description="Explanation why factor is the factor of the infinite product, why dummy_var is the dummy variable iterated over, " + \
                            "why start is the starting value for the dummy variable and why each unknown is an unknown.")


class GPTSympyExpression(BaseModel):
    expression: str
    explanation: str = Field(description="Explanation why the new string is the proper sympy expression for the original string.")


class GPTBool(BaseModel):
    boolean: bool
    explanation: str = Field(description="Explanation why the answer is either true or false.")


# Extract formula


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
            messages.append(user_message(f"The last attempt was not proper sympy: {str(e)[:50]}. Try again. Extract the expression in this string and write it in proper sympy format: {string}"))
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
                        "Specifically, we are interested in three types of formulas: continued fractions, series (infinite sums) and infinite products." + \
                        "Keep all answers concise and accurate."),
        user_message(f"Is this formula a continued fraction or a series or a product that can be rearranged to calculate the constant {constant}? {latex_string}")
        ]

    # is a formula?
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaBool)
    messages.append(assistant_message(extract_content(response)))

    formula_bool = json.loads(messages[-1]['content'])['boolean']

    if not formula_bool:
        if verbose:
            print(f'Not a formula.')
        return {'type': ''}, messages
    
    if verbose:
        print(f'Is a formula.')
        token_counts = count_tokens_for_messages(messages)
        print('Token counts:', token_counts)
        print('Cost estimate:', estimate_cost(token_counts=token_counts))

    # what type?
    messages.append(user_message(f"Is this formula a continued fraction, a series or a product? {latex_string}"))
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaClassification)
    messages.append(assistant_message(extract_content(response)))

    formula_type = json.loads(messages[-1]['content'])['formula_type']

    if verbose:
        print(f'Formula of type: {formula_type}')
        token_counts = count_tokens_for_messages(messages)
        print('Token counts:', token_counts)
        print('Cost estimate:', estimate_cost(token_counts=token_counts))

    # identify the value
    messages.append(user_message(r"What is the value of this formula? It should be explicit and on one side of the equation. " + \
                                    r"Example: the string '$$\forall z \in \mathbb{C}: \quad  1+\frac{1\cdot(2\cdot z-1)}{4+\frac{2\cdot(2\cdot z-3)}" + \
                                    r"{7+\frac{3\cdot(2\cdot z-5)}{10+\frac{4\cdot(2\cdot z-7)}{13+..}}}} = \frac{2^{2\cdot z +1}}{\pi\binom{2\cdot z}{z}}$$' " + \
                                    r"has value: '2**(2*z + 1)/(pi*binomial(2*z, z))'. " + \
                                r"Another example: the string '\pi=\frac{22}{7} -24\sum_{n=2}^\infty \frac{(-1)^{n}}{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}' " + \
                                r"has value: 'pi'. "  + \
                                f"Extract the value and write it in sympy format: {latex_string}"))
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTFormulaValue)
    messages.append(assistant_message(extract_content(response)))

    formula_value = json.loads(messages[-1]['content'])['value']

    if verbose:
        print(f'Formula value: {formula_value}')
        token_counts = count_tokens_for_messages(messages)
        print('Token counts:', token_counts)
        print('Cost estimate:', estimate_cost(token_counts=token_counts))

    # clean the value (iteratively)
    formula_value, messages, value_is_proper_sympy = correct_to_sympy_expression(formula_value, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model="gpt-4o", max_tokens=max_tokens)

    # identify formula components + unknowns
    if formula_type == 'cf':
        messages.append(user_message(f"Identify the partial denominator an, partial numerator bn, and any unknown variables (other than the depth n) " + \
                                    f"that appear in the the continued fraction. " + \
                                    r"Extract each of them and write them as proper sympy expressions as a function of depth n. " + \
                                    r"Example: the string '$$\forall z \in \mathbb{C}: \quad  1+\frac{1\cdot(2\cdot z-1)}{4+\frac{2\cdot(2\cdot z-3)}" + \
                                    r"{7+\frac{3\cdot(2\cdot z-5)}{10+\frac{4\cdot(2\cdot z-7)}{13+..}}}} = \frac{2^{2\cdot z +1}}{\pi\binom{2\cdot z}{z}}$$' " + \
                                    r"has an: '3*n + 1', bn: 'n*(2*z - (2*n - 1))', unknowns: ['z']" + \
                                    f"The continued fraction: {latex_string}"))
        response = client.beta.chat.completions.parse(model="gpt-4o", messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTCF)
        messages.append(assistant_message(extract_content(response)))

    elif formula_type == 'series':
        messages.append(user_message(f"Identify the summand, dummy variable, start value for the dummy variable and any unknown variables (other than the dummy variable) " + \
                                    f"that appear in the series: {latex_string}. Extract each of them and write them as proper sympy expressions. " + \
                                    r"Example: the string '\pi=\frac{22}{7} -24\sum_{n=2}^\infty \frac{(-1)^{n}}{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}' " + \
                                    "has summand: '(-1)**n / ((2n + 1)*(2*n + 2)*(2*n + 3)*(2*n + 4)*(2*n + 5))', dummy variable: 'n', start: '2', unknowns: [] " + \
                                    f"The series: {latex_string}"))
        response = client.beta.chat.completions.parse(model="gpt-4o", messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTSeries)
        messages.append(assistant_message(extract_content(response)))

    elif formula_type == 'product':
        messages.append(user_message(f"Identify the factor, dummy variable, start value for the dummy variable and any unknown variables (other than the dummy variable) " + \
                                    f"that appear in the infinite product: {latex_string}. Extract each of them and write them as proper sympy expressions. " + \
                                    r"Example: the string '\prod_{n=1}^\infty \frac{4n^2}{4n^2 - 1} = \frac{\pi}{2}' " + \
                                    r"has factor: '\frac{4n^2}{4n^2 - 1}', dummy variable: 'n', start: '1', unknowns: [] " + \
                                    f"The infinite product: {latex_string}"))
        response = client.beta.chat.completions.parse(model="gpt-4o", messages=messages, temperature=temperature, max_tokens=max_tokens, response_format=GPTProduct)
        messages.append(assistant_message(extract_content(response)))

    formula_info = json.loads(messages[-1]['content'])

    if verbose:
        print('Extracted formula info')
        token_counts = count_tokens_for_messages(messages)
        print('Token counts:', token_counts)
        print('Cost estimate:', estimate_cost(token_counts=token_counts))

    # clean the formula components + unknowns
    info_is_proper_sympy = copy.deepcopy(formula_info)
    del info_is_proper_sympy['explanation']
    for key, val in formula_info.items():
        if key == 'explanation':
            continue
        if key == 'unknowns':
            proper_sympy_val = copy.deepcopy(val)
            for i, string in enumerate(val):
                string, messages, sympy_boolean = correct_to_sympy_expression(string, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model=model, max_tokens=max_tokens)
                val[i] = string
                proper_sympy_val[i] = sympy_boolean
        else:
            val, messages, proper_sympy_val = correct_to_sympy_expression(val, messages=messages, max_iters=max_iters, verbose=verbose, temperature=temperature, model=model, max_tokens=max_tokens)
        
        formula_info[key] = val
        info_is_proper_sympy[key] = proper_sympy_val

    if verbose:
        print('Cleaned formula info')
        token_counts = count_tokens_for_messages(messages)
        print('Token counts:', token_counts)
        print('Cost estimate:', estimate_cost(token_counts=token_counts))

    # join dictionaries
    formula_info['value'] = formula_value
    is_proper_sympy = {}
    for item in info_is_proper_sympy.items():
        is_proper_sympy[item[0]] = item[1]
    is_proper_sympy['value'] = value_is_proper_sympy

    return {'type': formula_type, 'info': formula_info, 'is_proper_sympy': is_proper_sympy}, messages


# sympy to mathematica conversion


class GPTMathematica(BaseModel):
    mathematica: str


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


def convert_to_mathematica(sympy_string, temperature=0, api_key=OPENAI_API_KEY, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=api_key)

    # The expression should be a function of `k` so change the dummy variable.
    
    init_prompt = r"""Convert the following SymPy function, given as a Python string, into a valid Mathematica expression. Ensure it is fully compatible with Mathematica syntax.

        For example:
        - Input: `"1/(k + 1) * (factorial(k)) / (factorial(k - 2))"`
        - Output: `"1/(k + 1) * Factorial[k] / Factorial[k - 2]"`

        Another example:
        - Input: `"Rational(12, 34) * n**2 + n / 5"`
        - Output: `"12/34 k^2 + k / 5"`

        The output must:
        1. Replace Python/SymPy-specific syntax with Mathematica equivalents.
        2. Use `[]` for functions in Mathematica instead of `()`.
        3. Be a function of variable `k`.
        """

    messages = [
        system_message(f"You are a model that converts Python/Sympy expressions to equivalent Mathematica expressions."),
        user_message(f"{init_prompt}. The SymPy expression to convert is: {sympy_string}")
        ]
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, response_format=GPTMathematica)
    messages.append(assistant_message(extract_content(response)))

    return json.loads(messages[-1]['content'])['mathematica'], messages


# The following function was generated by Copilot from the code above.
# Examples were then edited.
def convert_to_sympy(mathematica_string, temperature=0, api_key=OPENAI_API_KEY, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=api_key)

    init_prompt = r"""Convert the following Mathematica function, given as a Python string, into a valid SymPy expression. Ensure it is fully compatible with SymPy syntax so it can be used as input to the `sympy` function.

        For example:
        - Input: `"1/(k + 1) * Factorial[k] / Factorial[k - 2]"`
        - Output: `"1/(k + 1) * factorial(k) / factorial(k - 2) + Rational(12, 34) * n**2 + Rational(1, 5) * n"`

        - Input: `"12/34 n^2 + n / 5"`
        - Output: `"Rational(12, 34) * n**2 + Rational(1, 5) * n"`

        - Input: `"(3369 + 39674 n - 418216 n^2) / 34"`
        - Output: `"Rational(3369, 34) + Rational(39674, 34) * n - Rational(418216, 34) * n**2"`

        The output must:
        1. Replace Mathematica-specific syntax with SymPy equivalents.
        2. Replace fractions with sympy `Rational` objects (do not include the sympy. prefix).
        3. Place integers exclusively inside `Rational` objects, no expressions that depend on `n`.
        """
    
    messages = [
        system_message(f"You are a model that converts Mathematica expressions to equivalent Python/SymPy expressions."),
        user_message(f"{init_prompt}. The Mathematica expression to convert is: {mathematica_string}")
        ]
    
    response = client.beta.chat.completions.parse(model=model, messages=messages, temperature=temperature, response_format=GPTSympyExpression)
    messages.append(assistant_message(extract_content(response)))

    return json.loads(messages[-1]['content'])['expression'], messages

