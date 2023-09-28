from docstring_parser import parse
import json
import openai
import pydantic

class DataTools:
    @staticmethod
    def update_descriptions_from_docstring(doc_info, fields):
        for p in doc_info.params:
            field_name = p.arg_name
            desc = p.description
            if field_name in fields["properties"]:
                fields["properties"][field_name].setdefault("description", desc)

    @staticmethod
    def find_required_fields(fields):
        return sorted(field for field, props in fields["properties"].items() if "default" not in props)

    @staticmethod
    def create_openai_properties(cls):
        base_schema = cls.model_json_schema()
        doc_info = parse(cls.__doc__ or "")
        fields = {key: val for key, val in base_schema.items() if key not in ['title', 'description']}
        
        DataTools.update_descriptions_from_docstring(doc_info, fields)
        
        fields["required"] = DataTools.find_required_fields(fields)
        
        return fields

    def transform(data, target_schema, model="gpt-3.5-turbo"):
        if not isinstance(data, str):
            raise TypeError("data must be a text string")
        if not issubclass(target_schema, pydantic.BaseModel):
            raise TypeError("target_schema must be a subclass of pydantic.BaseModel")
        schema_name = target_schema.__name__
        schema = DataTools.create_openai_properties(target_schema)
        messages = [{"role": "user", "content": f"Use the supplied functions to parse the following text. Do not make up answers. If you can't find a value for a property, simply return None for that property: {data}"}]
            
        functions = [
            {
                "name": schema_name,
                "description": target_schema.__doc__ or "Extracts data from unstructured text into a json schema that matches the output_cls. For missing values or data not found, do not hallucinate and only complete with 'None'",
                "parameters": {
                    "type": "object",
                    "properties": schema.get('properties'),
                    "required": schema.get('required')
                },
            }
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call={"name": schema_name},
        )
        
        if not response.get("choices"):
            raise ValueError("OpenAI's response does not contain the expected 'choices' field.")
        
        response_message = response["choices"][0]["message"]
        
        if not isinstance(response_message, dict):
            raise TypeError(f"Expected 'response_message' to be a dictionary, but got {type(response_message)}")
            
        if "function_call" not in response_message:
            raise KeyError("The response_message does not contain a 'function_call'.")

        if "function_call" not in response_message:
            raise KeyError("The response_message does not contain a 'function_call'.")

        if response_message["function_call"]["name"] != schema_name:
            raise ValueError(f"Function '{response_message['function_call']['name']}' is not recognized or supported.")
        
        try:
            function_args = json.loads(response_message["function_call"]["arguments"])
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding the JSON arguments: {e}")
        
        try:
            result = target_schema(**function_args)
        except Exception as e:
            raise ValueError(f"Error creating output class: {e}")
        
        function_response = result.model_dump()
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": schema_name,
                "content": json.dumps(function_response),
            }
        )
        return messages[2]["content"]