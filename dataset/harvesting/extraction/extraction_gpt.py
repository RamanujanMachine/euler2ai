from dataset_utils.gpt_utils import (
    system_message,
    user_message,
    assistant_message,
    extract_content,
    count_tokens_for_messages,
    estimate_cost
    )
import json
import openai
import copy
from enum import Enum
import sympy as sp
from typing import List
from pydantic import BaseModel


class SympyExpression(BaseModel):
    expression: str


def correct_to_sympy_expression(string, api_key, messages=[],
                                max_iters=3, temperature=0,
                                max_tokens=None, verbose=False):
    """
    Tries to correct a string to be a proper sympy expression.

    Args:
        max_iters: maximum number of iterations allowed for GPT to correct itself.
    """
    client = openai.OpenAI(api_key=api_key)

    working_messages = copy.deepcopy(messages)
    original_string = string
    new_messages = []

    working_messages.append(
        system_message(
            "You are a helpful assistant tasked with extracting mathematical expressions " + \
            "from strings and rewriting them in proper SymPy format.\nYour output must be " + \
            "valid Python code that can be executed without errors.\nAlways focus on processing " + \
            "the original string provided and ensure the response contains only the corrected SymPy expression, " + \
            "formatted as executable Python code."
            )
        )

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
            if i <= max_iters:
                if verbose:
                    print(f'Error: {e}')
                working_messages.append(
                    user_message(
                        f"The last attempt was invalid SymPy code: {str(e)[:50]}.\n\n"
                        f"Last attempt:\n{string}\n\n"
                        "Task:\n"
                        "1. Extract the expression from the **original string** below.\n"
                        "2. Rewrite it in proper SymPy format as valid, executable Python code.\n"
                        "3. Only return the corrected SymPy expression, formatted as valid Python code.\n\n"
                        f"Original string:\n{original_string}\n\n"
                        "Process the **original string** and provide the corrected SymPy expression."
                        )
                    )
                response = client.beta.chat.completions.parse(
                    model="gpt-4o", messages=working_messages, temperature=temperature,
                    max_tokens=max_tokens, response_format=SympyExpression)
                working_messages.append(assistant_message(extract_content(response)))
                new_messages.append(working_messages[-1])
                string = json.loads(working_messages[-1]['content'])['expression']
            else:
                break
  
    correction_cost = estimate_cost(messages=new_messages)
    return string, messages, expression_is_clean, correction_cost, i, new_messages


class FormulaBool(BaseModel):
    boolean: bool


class FormulaType(Enum):
    CONTINUED_FRACTION = 'cf'
    SERIES = 'series'
    NEITHER = 'neither'


class FormulaClassification(BaseModel):
    formula_type: FormulaType


class Series(BaseModel):
    term: str
    dummy_var: str
    start: str
    unknowns: List[str]


class CF(BaseModel):
    an: str
    bn: str
    unknowns: List[str]


class Variable(BaseModel):
    variable: str


def extract_formula(latex_string, api_key, constant='pi',
                    temperature=0, max_iters=3, max_tokens=None,
                    save_messages=False, verbose=True) -> dict:
    """
    The model used for symbolic formula extraction is 'gpt-4o', compared with 'gpt-4o-mini'
    which is used otherwise throughout the pipeline. 'gpt-4o' is seemingly better at generalizing
    patterns in the data to write the correct symbolic expressions.

    Args:
        max_iters: maximum number of iterations allowed for GPT to correct itself.
        save_messages: whether to save the messages exchanged with the model in the output dict.
    """
    client = openai.OpenAI(api_key=api_key)

    if verbose:
        print(f'Extracting formula from: {latex_string}')

    messages = [
        system_message(
            f"You are a model that extracts formula information from a LaTeX string.\n" + \
            "Your task is to:\n" + \
            "a. Classify the type of formula: series, continued fraction, or neither.\n" + \
            "b. Extract its components and identify the variable.\n" + \
            "This information will be used to compute the formula later, " + \
                "so it is critical that the components are accurate to ensure correctness.\n\n" + \
            "You will be asked separately about each of the following steps:\n" + \
            "Step 1. Classify the formula: Determine whether the LaTeX string represents " + \
                f"a series or a continued fraction that can be rearranged to calculate the constant {constant}.\n" + \
            "Step 2. Identify the formula type: Specify whether it is a series or a continued fraction.\n" + \
            "Step 3. Extract the formula components:\n" + \
            "   - For series: Identify the term and the start value.\n" + \
            "   - For continued fractions: Identify the partial numerator and partial denominator.\n" + \
            "Step 4. Identify the variable of the formula: Clearly state the variable used in the formula.\n"
        ),
        user_message(
            "Step 1:\n" + \
            "Is this formula a series or a continued fraction that can be rearranged " + \
            f"to calculate the constant {constant}?\n\n{latex_string}"
        )
        ]


    # is a formula?
    response = client.beta.chat.completions.parse(
        model="gpt-4o", messages=messages, temperature=temperature,
        max_tokens=max_tokens, response_format=FormulaBool
        )
    messages.append(assistant_message(extract_content(response)))

    formula_bool = json.loads(messages[-1]['content'])['boolean']

    if not formula_bool:
        token_counts = count_tokens_for_messages(messages)
        total_cost = estimate_cost(token_counts=token_counts)
        if verbose:
            print(f'Not a formula.')
        return {
            'type': '',
            'cost': total_cost,
            'messages': messages
            }
    if verbose:
        token_counts = count_tokens_for_messages(messages)
        total_cost = estimate_cost(token_counts=token_counts)
        print(f'Is a formula.')
        print('Total token counts:', token_counts)
        print('Total cost estimate:', total_cost)


    # what type?
    messages.append(
        user_message(
            "Step 2:\n" + \
            "Determine the type of formula. " + \
            f"Is this formula a continued fraction or a series?\n\n{latex_string}"
            )
        )
    response = client.beta.chat.completions.parse(
        model="gpt-4o", messages=messages, temperature=temperature,
        max_tokens=max_tokens, response_format=FormulaClassification
        )
    messages.append(assistant_message(extract_content(response)))

    formula_type = json.loads(messages[-1]['content'])['formula_type']

    if verbose:
        token_counts = count_tokens_for_messages(messages)
        total_cost = estimate_cost(token_counts=token_counts, model="gpt-4o")
        print(f'Formula of type: {formula_type}')
        print('Total token counts:', token_counts)
        print('Total cost estimate:', total_cost)


    # identify formula components + unknowns
    if formula_type == 'cf':
        messages.append(
            user_message(
                "Step 3:\n" + \
                "The formula is a continued fraction. Identify the following components:\n" + \
                "1. The partial denominator (an) as a function of depth (n).\n" + \
                "2. The partial numerator (bn) as a function of depth (n).\n" + \
                "3. Any unknown variables (other than the depth n).\n\n" + \
                "Write each component as a proper SymPy expression. For example:\n" + \
                "The string '$$\\forall z \\in \\mathbb{C}: \\quad  1+\\frac{1\\cdot(2\\cdot" + \
                    "z-1)}{4+\\frac{2\\cdot(2\\cdot z-3)}" + \
                "{7+\\frac{3\\cdot(2\\cdot z-5)}{10+\\frac{4\\cdot(2\\cdot z-7)}{13+..}}}} = " + \
                    "\\frac{2^{2\\cdot z +1}}{\\pi\\binom{2\\cdot z}{z}}$$' " + \
                "has the following:\n" + \
                "  - an: '3*n + 1'\n" + \
                "  - bn: 'n*(2*z - (2*n - 1))'\n" + \
                "  - unknowns: ['z']\n\n" + \
                f"The continued fraction is:\n{latex_string}\n\n"
                )
            )
        response = client.beta.chat.completions.parse(
            model="gpt-4o", messages=messages, temperature=temperature,
            max_tokens=max_tokens, response_format=CF)
        messages.append(assistant_message(extract_content(response)))

    elif formula_type == 'series':
        messages.append(
            user_message(
                "Step 3:\n" + \
                "The formula is a series. Identify the following components:\n" + \
                "1. The term (summand) as a SymPy expression.\n" + \
                "2. The dummy variable.\n" + \
                "3. The start value of the dummy variable.\n" + \
                "4. Any unknown variables (other than the dummy variable).\n\n" + \
                "For example:\n" + \
                "The string '\\pi=\\frac{22}{7} -24\\sum_{n=2}^\\infty \\frac{(-1)^{n}}{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}' " + \
                "has the following:\n" + \
                "  - Term: '(-1)**n / ((2*n + 1)*(2*n + 2)*(2*n + 3)*(2*n + 4)*(2*n + 5))'\n" + \
                "  - Dummy variable: 'n'\n" + \
                "  - Start: '2'\n" + \
                "  - Unknowns: []\n\n" + \
                "Pay attention to special symbols like _<symbol> (e.g., '(\\frac{1}{2})_n')," + \
                    "which often indicate a RisingFactorial. Another symbol to look out for is" + \
                        "'H_' which often means harmonic.\n\n" + \
                f"The series is:\n{latex_string}"
                )
            )
        response = client.beta.chat.completions.parse(
            model="gpt-4o", messages=messages, temperature=temperature,
            max_tokens=max_tokens, response_format=Series)
        messages.append(assistant_message(extract_content(response)))

    formula_info = json.loads(messages[-1]['content'])

    if verbose:
        token_counts = count_tokens_for_messages(messages)
        total_cost = estimate_cost(token_counts=token_counts, model="gpt-4o")
        print('Extracted formula info')
        print('Total token counts:', token_counts)
        print('Total cost estimate:', total_cost)


    # identify the variable
    messages.append(
        user_message(
            "Step 4:\n" + \
            "Identify the variable used in the formula. " + \
            "If the formula is a series, focus on the variable used in the outermost summation. " + \
            "If the formula contains nested summations or other variables, " + \
            "ensure you extract only the variable from the outermost summation and exclude all others.\n\n" + \
            f"For example:\n" + \
            "The string '$$\\pi = \\frac{{22}}{{7}} - 24\\sum_{{n=2}}^\\infty" + \
                " \\frac{{(-1)^n}}{{(2n+1)(2n+2)(2n+3)(2n+4)(2n+5)}}$$' " + \
            "has the outermost summation variable: 'n'.\n\n" + \
            f"Extract the variable from the formula:\n{latex_string}."
            )
        )
    response = client.beta.chat.completions.parse(
        model="gpt-4o", messages=messages, temperature=temperature,
        max_tokens=max_tokens, response_format=Variable)
    messages.append(assistant_message(extract_content(response)))

    formula_variable = json.loads(messages[-1]['content'])['variable']

    if verbose:
        token_counts = count_tokens_for_messages(messages)
        total_cost = estimate_cost(token_counts=token_counts)
        print(f'Formula variable: {formula_variable}')
        print('Total token counts:', token_counts)
        print('Total cost estimate:', total_cost)

    
    # clean the formula components + unknowns iteratively
    info_is_proper_sympy = {}
    info_correction_cost = {}
    info_correction_iters = {}
    info_correction_messages = []

    for key, val in formula_info.items():
        if key == 'unknowns':
            proper_sympy_vals = []
            correction_costs = []
            correction_iters = []
            
            for i, string in enumerate(val):
                corrected_string, _, sympy_boolean, cost, iters, new_messages = correct_to_sympy_expression(
                    string, api_key, messages=messages, max_iters=max_iters,
                    temperature=temperature, max_tokens=max_tokens, verbose=verbose)
                
                val[i] = corrected_string
                proper_sympy_vals.append(sympy_boolean)
                correction_costs.append(cost)
                correction_iters.append(iters)
                info_correction_messages.extend(new_messages)
            
            info_is_proper_sympy[key] = proper_sympy_vals
            info_correction_cost[key] = correction_costs
            info_correction_iters[key] = correction_iters
        else:
            corrected_val, _, proper_sympy_val, correction_cost, correction_iters, new_messages = correct_to_sympy_expression(
                val, api_key, messages=messages, max_iters=max_iters,
                temperature=temperature, max_tokens=max_tokens, verbose=verbose)
            
            formula_info[key] = corrected_val
            info_is_proper_sympy[key] = proper_sympy_val
            info_correction_cost[key] = correction_cost
            info_correction_iters[key] = correction_iters
            info_correction_messages.extend(new_messages)

    if verbose:
        print("Cleaned formula info.")


    # package up the results
    formula_info = {**formula_info, 'variable': formula_variable}
    messages.extend(info_correction_messages)
    token_counts = count_tokens_for_messages(messages)
    total_cost = estimate_cost(token_counts=token_counts)

    output= {
        'cost': total_cost,
        'type': formula_type,
        'info': formula_info,
        'is_proper_sympy': info_is_proper_sympy,
        'correction_cost': info_correction_cost,
        'correction_iters': info_correction_iters
        }
    
    if save_messages:
        output['messages'] = messages

    return output
