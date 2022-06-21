
def success(data, code=200, message="Successful!"):
    return {
        "success":True,
        "code":code,
        "message":message,
        "data": data
    }

def error(code=400, message="Error!"):
    return {
        "success": False,
        "code": 400,
        "message": message
    }