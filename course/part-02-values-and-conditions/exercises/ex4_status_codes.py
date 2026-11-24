"""Exercise 4 (checkpoint): classify HTTP status codes.

Fill in the functions. Each one must `return` its answer.

classify(status_code)
    Returns the category of a status code as text.

    100 to 199  ->  "informational"
    200 to 299  ->  "success"
    300 to 399  ->  "redirect"
    400 to 499  ->  "client error"
    500 to 599  ->  "server error"
    anything else  ->  "unknown"

    classify(201)  ->  "success"
    classify(404)  ->  "client error"
    classify(700)  ->  "unknown"

describe(status_code)
    Returns the code and its category in one string. Use classify() inside it.
    describe(404)  ->  "404: client error"

should_retry(status_code)
    True when sending the request again might help: the code is 429
    (too many requests) or any server error. Otherwise False.
    should_retry(503)  ->  True
    should_retry(429)  ->  True
    should_retry(404)  ->  False
"""
def classify(status_code):
    
    if status_code >= 100 and status_code <= 199:
        return "informational"
    elif status_code >= 200 and status_code <= 299:
        return "success"
    elif status_code >= 300 and status_code <= 399:
        return "redirect"
    elif status_code >= 400 and status_code <= 499:
        return "client error"
    elif status_code >= 500 and status_code <= 599:
        return "server error"
    else:
        return "unknown"

def describe(status_code):
    
    return f"{status_code}: {classify(status_code)}"


def should_retry(status_code):
    # TODO: replace the line below
    return status_code >= 500 and status_code <= 599 or status_code == 429
    


# Try your functions.
print(describe(200))
print(describe(404))
print(describe(503))
print(should_retry(503))
