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
        schema = target_schema.model_json_schema()
        
        messages = [
            {"role": "user", 
            "content": f"Use the supplied functions to parse the following text. Do not make up answers. If you can't find a value for a property, simply return None for that property: {data}"
            }
        ]
        functions = [
            {
                "name": schema_name,
                "description": target_schema.__doc__ or "Extracts data from unstructured text into a json schema that matches the output_cls. For missing values or data not found, do not hallucinate and only complete with 'None'",
                "parameters": schema,
            }
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call={"name": schema_name},
            )

            function_args = response["choices"][0]["message"]["function_call"]["arguments"]
            result = target_schema(**json.loads(function_args))
            return result
        except (KeyError, pydantic.ValidationError, json.JSONDecodeError):
            return {"error": "Failed to transform data"}