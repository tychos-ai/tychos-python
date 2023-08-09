import re

def validate_query_filter(query_filter):
    valid_operators = ['$eq', '$ne', '$gt', '$gte', '$lt', '$lte', '$in', '$nin']
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')  # Pattern for ISO 8601 dates
    
    if not isinstance(query_filter, dict):
        raise ValueError("query_filter must be a dictionary.")
    
    for key, value in query_filter.items():
        # Validate that value is a dictionary with a valid operator
        if not isinstance(value, dict):
            raise ValueError("The value in query_filter must be a dictionary.")
        if len(value) != 1:
            raise ValueError("The value in query_filter must contain exactly one operator.")
        
        operator, operand = list(value.items())[0]
        if operator not in valid_operators:
            raise ValueError(f"Invalid operator '{operator}' in query filter. Use one of the following operators: {', '.join(valid_operators)}")
        
        # Validate the operand based on the operator
        if operator in ['$eq', '$ne']:
            if not isinstance(operand, (int, str, bool)):
                raise ValueError(f"The operand of '{operator}' must be an integer, string, or boolean.")
        elif operator in ['$gt', '$gte', '$lt', '$lte']:
            if isinstance(operand, int):
                continue
            elif isinstance(operand, str):
                if not date_pattern.fullmatch(operand):
                    raise ValueError(f"The operand of '{operator}' must be an integer or date string in ISO 8601 format.")
            else:
                raise ValueError(f"The operand of '{operator}' must be an integer or date string.")
        elif operator in ['$in', '$nin']:
            if not isinstance(operand, list) or not all(isinstance(i, (int, str)) for i in operand):
                raise ValueError(f"The operand of '{operator}' must be a list of integers or strings.")
    return True