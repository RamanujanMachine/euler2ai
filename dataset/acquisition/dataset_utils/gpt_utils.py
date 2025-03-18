import tiktoken
import json


def extract_content(gpt_response):
    return json.loads(gpt_response.model_dump_json())['choices'][0]['message']['content']


def system_message(message):
    return {"role": "system", "content": message}


def user_message(message):
    return {"role": "user", "content": message}


def assistant_message(message):
    return {"role": "assistant", "content": message}


def count_tokens(string):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(string))


def count_tokens_for_messages(messages):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return {'system': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'system']),
            'user': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'user']),
            'assistant': sum([len(enc.encode(m['content'])) for m in messages if m['role'] == 'assistant'])}


def estimate_cost(messages=[], token_counts={}, model="gpt-4o"):
    # in $ US dollars
    if model == "gpt-4o":
        SYSTEM_COST = 2.5 / 10**6
        USER_COST = 2.5 / 10**6
        ASSISTANT_COST = 10 / 10**6
    elif model == "gpt-4o-mini":
        SYSTEM_COST = 0.15 / 10**6
        USER_COST = 0.15 / 10**6
        ASSISTANT_COST = 0.6 / 10**6

    if not token_counts:
        token_counts = count_tokens_for_messages(messages)

    return SYSTEM_COST * token_counts['system'] + USER_COST * token_counts['user'] + ASSISTANT_COST * token_counts['assistant']
