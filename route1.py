import logger


folder_path = "logs"

foo = logger.Logger("foo", folder_path)

def divide(x,y):
    try:
        result = x / y
    except ZeroDivisionError:
        foo.error("Can divided by zero")
    else:
        return result

res = divide(10, 0)
print(res)