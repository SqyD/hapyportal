hapy_config = {
    "home_card" : "ventilation",
    "style" : "default",
    "display_width" : 240,
    "display_height" : 320,
    "icon_path" : "/sd/icons/"
}

hapy_cards = {
    "ventilation": {
        "name": "Ventilation",
        "type": "entity",
        "entity": "fan.ventilation",
    },
    "office_lights": {
        "title": "Office Light",
        "type": "light",
        "entity": "light.office_group",
    },
    "living_cabinet": {
        "title": "Lights",
        "type": "entities",
        "entity_ids": ["light.living_left", "light.living_right"],
    }
}

hapy_styles = {
    "default": {
        "background_color" : 0xffffff,
        "font" : "Roboto",
        "font_size" : 36,
        "text_color" : 0x000000,
        "icon_state_on_color" : 0xffff00,
        "header_background_color" : 0x049cdb,
        "header_text_color" : 0xffffff
    },
    "dark": {
        "background_color" : 0x000000,
        "font" : "Roboto",
        "font_size" : 18,
        "text_color" : 0xffffff,
        "icon_state_on_color" : 0xffff00,
        "header_background_color" : 0x000000,
        "header_text_color" : 0xffffff
    }
}
