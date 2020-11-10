# haportal
import board
import displayio
import adafruit_imageload
import hapy
from hapy_cards import *
import json
import config

class HaPyPortal:
    def __init__(self, secrets):
        self.display = board.DISPLAY
        self.display.rotation = 270
        # empty screen
        self.haclient = hapy.HAClient(secrets['ha_url'], access_token = secrets['ha_token'])
        self.entities = dict()
        self.cards = dict()
        self.load_cards()
        card_style = config.hapy_config['style']
        self.style = config.hapy_styles[card_style]

    def load_cards(self):
        card_config = config.hapy_cards
        # Load up all the cards of the different supported types
        for card_id in card_config.keys():
            self.cards[card_id] = self.get_card(card_id, card_config[card_id])

    def get_card(self, card_id, card_config):
        if card_config['type'] == 'entity':
            return HACardEntity(card_id, card_config)
        elif card_config['type'] == 'light':
            return HACardLight(card_id, card_config)

    def get_card_background(self):
        color_bitmap = displayio.Bitmap(config.hapy_config['display_width'], config.hapy_config['display_height'], 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = self.style['background_color']
        card_background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        return card_background

    def get_card_header(self):
        header_display = displayio.Group(max_size=4)
        header_height = self.style['font_size'] + 4
        color_bitmap = displayio.Bitmap(config.hapy_config['display_width'], header_height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = self.style['header_background_color']
        header_background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        header_display.append(header_background)
        ha_icon = self.get_icon("mdi:home-assistant", self.style['font_size'], self.style['header_text_color'], self.style['header_background_color'])
        ha_icon.x = 1
        ha_icon.y = 1
        header_display.append(ha_icon)
        return header_display

    def int_to_rgb(self, color):
        blue = color % 256
        green = int( ((color - blue) / 256) % 256 )
        red = int( ((color - blue) / 256 ** 2) - green / 256 )
        return (red, green, blue)

    def get_middle_color(self, color1, color2):
        r1, g1, b1 = self.int_to_rgb(color1)
        r2, g2, b2 = self.int_to_rgb(color2)
        middle_color = (256 ** 2) * ((r1 + r2) / 2)
        middle_color = middle_color + 256 * ((g1 + g2) / 2)
        middle_color = middle_color + ((b1 + b2 ) / 2)
        return int(middle_color)

    def get_icon(self, icon, size, color, bg_color):
        if icon[:4] == "mdi:":
            icon = icon[4:]
        icon_file = config.hapy_config['icon_path'] + str(size) + "/" + icon + "-" + str(size) + ".bmp"
        bitmap, bm_palette = adafruit_imageload.load(icon_file, bitmap=displayio.Bitmap, palette=displayio.Palette)
        icon_palette = displayio.Palette(3)
        middle_color = self.get_middle_color(color, bg_color)
        for palette_color in [0 , 1 , 2]:
            if bm_palette[palette_color] == 0x000000:
                icon_palette[palette_color] = color
            elif bm_palette[palette_color] == 0x808080:
                icon_palette[palette_color] = middle_color
            elif bm_palette[palette_color] == 0xffffff:
                icon_palette[palette_color] = bg_color
        icon_tile = displayio.TileGrid(bitmap, pixel_shader=icon_palette)
        return icon_tile

    def show_card(self, card_id):
        card_entities = self.cards[card_id].entities
        for card_entity in card_entities:
            self.cards[card_id].states[card_entity] = self.haclient.get_state(card_entity)
        self.cards[card_id].set_elements()
        card_display=displayio.Group(max_size=4)
        background = self.get_card_background()
        card_display.append(background)
        header_display = self.get_card_header()
        card_display.append(header_display)
        self.display.show(card_display)