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

    def transform(data, target_schema, model="gpt-3.5-turbo", ai_infer=True):
        if not isinstance(data, str):
            raise TypeError("data must be a string")

        if not issubclass(target_schema, pydantic.BaseModel):
            raise TypeError("target_schema must be a Pydantic Model")

        allowed_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"]
        if model not in allowed_models:
            raise ValueError(f"model must be one of the following OpenAI models: {allowed_models}")
        
        if not isinstance(ai_infer, bool):
            raise TypeError("ai_infer must be a boolean")

        schema_name = target_schema.__name__
        schema = target_schema.model_json_schema()

        if ai_infer:
            messages = [
                {"role": "system",
                "content": "Infer data where it isn't explicitly stated for a property and make assumptions."
                },
                {"role": "user", 
                "content": data
                }
            ]
            functions = [
                {
                    "name": schema_name,
                    "description": target_schema.__doc__ or "Extracts data from unstructured text into a json schema that matches the output_cls.",
                    "parameters": schema,
                }
            ]
        else:
            messages = [
                {"role": "system",
                "content": "Do not make up answers or make assumptions. Return None (or the equivalent specified datatype) for properties that aren't found."
                },
                {"role": "user", 
                "content": f"Do not make up answers or make assumptions. Return None for properties that aren't found: {data}"
                }
            ]
            functions = [
                {
                    "name": schema_name,
                    "description": target_schema.__doc__ or "Extracts data from unstructured text into a json schema that matches the output_cls.",
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
            
            function_args = json.loads(response["choices"][0]["message"]["function_call"]["arguments"], strict=False)

            return target_schema(**function_args)

        except (KeyError, pydantic.ValidationError, json.JSONDecodeError) as e:
            return {"error": f"Failed to transform data due to {str(e)}"}