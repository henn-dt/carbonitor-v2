# app/presentation/decorators/response_handling.py
from functools import wraps
from flask import jsonify
from typing import Type
from pydantic import BaseModel, ValidationError

def handle_response(view_model_class: Type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                if result is None:
                    return jsonify({'error': 'Not found'}), 404
                
                if isinstance(result, list):
                    response = [view_model_class.model_validate(item) for item in result]
                    return jsonify([item.model_dump() for item in response])
                
                response = view_model_class.model_validate(result)
                return jsonify(response.model_dump())
            except ValidationError as e:
                return jsonify({"errors": e.errors()}), 422
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return jsonify({'error': 'Internal server error'}), 500
        return decorated_function
    return decorator