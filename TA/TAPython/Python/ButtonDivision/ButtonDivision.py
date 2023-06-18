# -*- coding: utf-8 -*-
import random

import unreal
import json

from Utilities.Utils import Singleton

class ButtonDivisionExample(metaclass=Singleton):
    def __init__(self, json_path:str):
        self.json_path = json_path
        self.data:unreal.ChameleonData = unreal.PythonBPLib.get_chameleon_data(self.json_path)
        self.id = 0
        self.colors = [[10, 10, 0.5, 1], [10, 10, 10, 1], [10, 0.5, 0.5, 1], [0.5, 0.5, 10, 1], [10, 10, 10, 1]]
        self.get_color_num = 0


    def get_button_json(self, id: int):
        s = f'{{"SButton": {{ "Text": "PlaceHolder Button", "Aka": "button_{id}", "OnClick": "chameleon_button_division.new_button()"}}}}'
        return s


    def new_button(self):
        self.data.set_content_from_json(f"button_{self.id}", self.get_button_json(self.id+1))
        self.id += 1

    def get_parent_aka(self, aka:str):
        aka_to_path = {x: self.data.get_widget_path_from_aka(x) for x in self.data.get_all_akas()}
        current_path = self.data.get_widget_path_from_aka(aka)
        result = ""
        result_aka = ""
        for k, p in aka_to_path.items():
            if p == current_path:
                continue
            if current_path.startswith(p):
                if len(p) > len(result):
                    result = p
                    result_aka = k
        return result_aka, result

    def pick_a_color(self):
        self.get_color_num += 1
        return self.colors[self.get_color_num % len(self.colors)]


    def gen_child_json(self, id):
        
        def gen_button(button_aka, color):
            return {"Padding": 1,
                    "SButton": {"Aka": button_aka, "Text": " "
                    , "OnClick": f"chameleon_button_division.on_button_click('{button_aka}')"
                    , "ButtonColorAndOpacity": color}}

        box_type = "SHorizontalBox" if id % 2  else "SVerticalBox"
        fill_type = "FillWidth" if  box_type == "SHorizontalBox" else "FillHeight"

        item = {box_type: {"Aka": f"c_{id}",  "Slots":[]}}
        item[box_type]["Slots"].append(gen_button(f"b_{id}_A", self.pick_a_color()))
        item[box_type]["Slots"][0][fill_type] = 0.618
        item[box_type]["Slots"].append(gen_button(f"b_{id}_B", self.pick_a_color()))

        if random.random() > 0.5:
            item[box_type]["Slots"][0], item[box_type]["Slots"][1] = item[box_type]["Slots"][1], item[box_type]["Slots"][0]

        if random.random() > 0.8:
            item[box_type]["Slots"].append(gen_button(f"b_{id}_C", self.pick_a_color()))
            item[box_type]["Slots"][0][fill_type] = 1.618

        return json.dumps(item)



    def on_button_click(self, button_aka:str):
        print(f"On_button_click: {button_aka}")
        button_path = self.data.get_widget_path_from_aka(button_aka)
        parent_aka, parent_path = self.get_parent_aka(button_aka)
        print(f"{button_path=}")
        print(f"{parent_aka=}, {parent_path=}")
        slot_id = button_path[button_path.rfind("/Slots_") + len("/Slots_"):button_path.rfind("/SButton"):]
        assert slot_id
        slot_id = int(slot_id)

        # insert
        self.id += 1
        child_json = self.gen_child_json(self.id)
        self.data.insert_slot_from_json(parent_aka, child_json, slot_id)
        self.data.remove_widget_at(parent_aka, slot_id+1)









