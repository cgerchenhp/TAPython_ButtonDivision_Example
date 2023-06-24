# -*- coding: utf-8 -*-
import random
import json

import unreal
from Utilities.Utils import Singleton


class DynamicSlateExamples(metaclass=Singleton):
    def __init__(self, json_path:str):
        self.json_path = json_path
        self.data : unreal.ChameleonData = unreal.PythonBPLib.get_chameleon_data(self.json_path)
        self.slots_added_count = 0
        self.ui_border = "a_named_sborder"
        self.ui_verticalbox = "a_named_sverticalbox"
        self.ui_index_input = "index_input"

        self.template_json = """{
            "Padding": 4,
            "SHorizontalBox":
            {
                "Slots": [
                    {
                        "STextBlock":
                        {
                            "Text": "Text Content"
                        }
                    },
                    {
                        "SEditableTextBox":
                        {
                            "Text": "Some Text",
                            "Aka": "a_named_text_input"
                        }
                    },
                    {
                        "SButton": { "Text": "Modify", "HAlign": "Center", "VAlign": "Center",
                            "OnClick": "chameleon_dynamic_slate_example.on_generated_button_click('a_named_text_input')"
                        }
                    }
                ]
            }
        }"""

    def on_generated_button_click(self, aka_name):
        self.data.set_text(aka_name, str(random.random()))

    def on_button_set_content_click(self):
        self.data.set_content_from_json(self.ui_border, self.template_json)


    def on_button_remove_click(self):
        self.data.remove_widget_at(self.ui_border, 0)

    def on_button_log_akas(self):
        all_akas = self.data.get_all_akas()
        widget_paths = [self.data.get_widget_path(aka) for aka in all_akas]

        for aka, widget_path in zip(all_akas, widget_paths):
            print(f"Aka: {aka: <30} :{widget_path}")


    def on_button_append_click(self):
        self.slots_added_count += 1
        # add unique aka name

        json_content = self.template_json.replace('a_named_text_input', f'a_named_text_input_{self.slots_added_count}')
        json_content = json_content.replace('"Padding": 4,', '"Padding": 4, \n"AutoHeight": true,').replace('Text Content', f'Text Content {self.slots_added_count}')
        self.data.append_slot_from_json(self.ui_verticalbox, json_content)


    def on_button_insert_click(self):
        # another way for creating json content is using `json.dumps`
        index = self.data.get_int_value(self.ui_index_input)
        new_widget = {"SButton": {"Text": "a green button", "HAlign": "center"}}
        new_widget["SButton"]["ButtonColorAndOpacity"] = [0.3, 1, 0.3, 1]
        new_widget["AutoHeight"] = True
        self.data.insert_slot_from_json(self.ui_verticalbox, json.dumps(new_widget), index)
        self.slots_added_count += 1

    def on_button_remove_first_click(self):
        self.data.remove_widget_at(self.ui_verticalbox, 0)
