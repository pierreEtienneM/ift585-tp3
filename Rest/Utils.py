def Error(message):
    return {
        "success": False,
        "message": message
    }

def Success(message):
    return {
        "success": True,
        "message": message
    }