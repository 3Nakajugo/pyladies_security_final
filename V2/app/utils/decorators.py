from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required
from flask import jsonify


def role_required(*roles):
    def wrapper(fn): #This is the actual decorator that will wrap the function.
        @wraps(fn) #This keeps the original function’s name and metadata.
        @jwt_required() #This ensures that the user is authenticated before accessing the function.
        def decorated(*args, **kwargs): #Allowable arguments for the decorated function.
            claims = get_jwt() #Get the JWT claims, which contain user information like role.
            if claims.get("role") not in roles: #Check if the user's role is in the allowed roles.
                return {"message": "Forbidden"}, 403 #If not, return a 403 Forbidden response.
            return fn(*args, **kwargs) #If the role is valid, call the original function with its arguments.
        return decorated
    return wrapper
