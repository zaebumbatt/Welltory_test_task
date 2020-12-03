import json
import logging
import os

from jsonschema import exceptions, validate

logging.basicConfig(filename='result.log', level=logging.DEBUG)

schemas_files = os.listdir('task_folder/schema')
events_files = os.listdir('task_folder/event')

schemas = set()
for schema in schemas_files:
    schemas.add(schema.rstrip('.schema'))

for event in events_files:
    with open(f'task_folder/event/{event}') as file1:
        event_data = json.load(file1)
        if not event_data:
            logging.debug(f'File "{event}" is empty.')
        else:
            schema = event_data.get('event')
            if schema not in schemas:
                logging.debug(
                    (f'File "{event}". '
                     f'Schema "{event_data["event"]}" is not available.')
                )
            else:
                with open(f'task_folder/schema/{schema}.schema') as file2:
                    schema_data = json.load(file2)
                    try:
                        validate(instance=event_data, schema=schema_data)
                    except exceptions.ValidationError as exception:
                        logging.debug(
                            (f'File "{event}". '
                             f'{exception.message} in "{schema}" schema.')
                        )
