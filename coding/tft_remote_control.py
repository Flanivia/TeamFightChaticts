import time
import math
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Callable

import pyautogui

from .tft_command import TFTCommand, TFTCmdType
from .tft_screen_capture import capture_level, capture_gold, capture_item_locations


class MouseControl:
    def click_at(self, loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.mouseUp(button="left")

    def right_click_at(self, loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="right")
        pyautogui.mouseUp(button="right")

    def drag(self, from_loc: Tuple[int, int], to_loc: Tuple[int, int]):
        pyautogui.moveTo(from_loc[0], from_loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.moveTo(to_loc[0], to_loc[1])
        pyautogui.mouseUp(button="left")


class TFTRemoteControlPositions:
    # TODO: compute the positions as properties depending on the screen resolution
    def __init__(self):
        self.row_1=[(580, 670), (710, 670), (840, 670), (970, 670), (1100, 670), (1230, 670), (1360, 670)]
        self.row_2=[(530, 590), (660, 590), (790, 590), (900, 590), (1025, 590), (1150, 590), (1275, 590)]
        self.row_3=[(610, 515), (730, 515), (850, 515), (965, 515), (1080, 515), (1200, 515), (1315, 515)]
        self.row_4=[(560, 430), (680, 430), (790, 430), (905, 430), (1025, 430), (1140, 430), (1250, 430)]
        self.row_5=[(580, 370), (710, 370), (840, 370), (970, 370), (1100, 370), (1230, 370), (1340, 370)]
        self.row_6=[(560, 315), (660, 315), (790, 315), (900, 315), (1025, 315), (1150, 315), (1310, 315)]
        self.row_7=[(550, 240), (730, 240), (850, 240), (965, 240), (1080, 240), (1200, 240), (1315, 240)]
        self.row_8=[(590, 175), (680, 175), (790, 175), (905, 175), (1025, 175), (1140, 175), (1250, 175)]
        self.bench=[(420, 780), (540, 780), (660, 780), (780, 780), (900, 780), (1020, 780), (1140, 780), (1260, 780), (1380, 780)]
        self.board_locations= [
            self.bench, self.row_1, self.row_2, self.row_3, self.row_4,
            self.row_5, self.row_6, self.row_7, self.row_8
        ]
        self.augment_list= [(590, 500), (960, 500), (1320, 500)]
        self.item_list = [(290, 755), (335, 725), (310, 705), (350, 660), (410, 665), (325, 630), (385, 630), (445, 630), (340, 590), (395, 590)]
        self.shop_list=[(570, 1000), (770, 1000), (970, 1000), (1170, 1000), (1370, 1000)]
        self.com_list = [(370, 980), (370, 1060)]
        self.avatar_default = (470, 650)
        self.avatar_velocity = 150
        self.levelup_button = (375, 960)
        self.roll_button = (375, 1045)
        self.carousel_aim = (950, 370)
        self.lock_button = (1450, 900)
        self.item_drop_region = (500, 200, 1375, 725)
        self.item_offset = 30
        self.default_click_pos = (960, 250)

    def by_field(self, field_id: str) -> Tuple[int, int]:
        row = field_id[0]
        col = int(field_id[1])

        if row.startswith('w'):
            return self.bench[col-1]
        if row.startswith('l'):
            return self.row_1[col-1]
        if row.startswith('b'):
            return self.row_2[col-1]
        if row.startswith('g'):
            return self.row_3[col-1]
        if row.startswith('r'):
            return self.row_4[col-1]


@dataclass
class TFTRemoteControl:
    positions: TFTRemoteControlPositions=TFTRemoteControlPositions()
    mouse: MouseControl=MouseControl()
    cmd_handlers: Dict[TFTCmdType, Callable[[TFTCommand]], None] = field(init=False)

    def __post_init__(self):
        self.cmd_handlers = {
            TFTCmdType.SHOP: self.handle_shop_cmd,
            TFTCmdType.PICK_AUGMENT: self.handle_augment_cmd,
            TFTCmdType.LOCK_OR_UNLOCK: self.handle_lock_or_unlock_cmd,
            TFTCmdType.PICK_ITEM_CAROUSEL: self.handle_carousel_cmd,
            TFTCmdType.COLLECT_ALL_ITEMS_DROPPED: self.handle_collect_cmd,
            TFTCmdType.LEVELUP: self.handle_levelup_cmd,
            TFTCmdType.ROLL_SHOP: self.handle_roll_cmd,
            TFTCmdType.SELL_UNIT: self.handle_sell_bench_unit_cmd,
            TFTCmdType.PLACE_UNIT: self.handle_place_unit_cmd,
            TFTCmdType.COLLECT_ITEMS_OF_ROW: self.handle_collect_row_cmd,
            TFTCmdType.ATTACH_ITEM: self.handle_attach_item_cmd,
        }

    def execute_cmd(self, tft_cmd: TFTCommand):
        if tft_cmd.type in self.cmd_handlers:
            self.cmd_handlers[tft_cmd.type](tft_cmd.cmd) # TODO: refactor to put whole command object

    def handle_shop_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        unit = tft_cmd.selected_shop_unit
        shop_pos = self.positions.shop_list[unit]
        self.mouse.click_at(shop_pos)

    def handle_augment_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        augment_pos = self.positions.augment_list[tft_cmd.selected_augment]
        self.mouse.click_at(augment_pos)

    def handle_lock_or_unlock_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        self.mouse.click_at(self.positions.lock_button)

    def handle_carousel_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        self.mouse.right_click_at(self.positions.carousel_aim)

    def handle_collect_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        items = self.compute_item_drop_positions()
        if items:
            self.collect_dropped_items_at(items)

    def compute_item_drop_positions(self) -> list:
        offset = self.positions.item_offset
        box = self.positions.item_drop_region
        item_locs = capture_item_locations(box)
        if not item_locs:
            return None
        return [(p[0] + box[0] + offset, p[1] + box[1] + offset) for p in item_locs]

    def collect_dropped_items_at(self, locations: List[Tuple[int, int]]):
        # TODO: use Dijkstra algorithm to compute the shortest path instead of randomly walking between items
        locations.insert(0, self.positions.avatar_default)
        locations.append(self.positions.avatar_default)

        for pos_from, pos_to in zip(locations[:-1], locations[1:]):
            distance = math.dist(pos_from, pos_to)
            self.mouse.right_click_at(pos_to)
            if pos_to != self.positions.avatar_default:
                time.sleep(distance / self.positions.avatar_velocity)

        self.mouse.click_at(self.positions.default_click_pos)

    def handle_levelup_cmd(self, tft_cmd: TFTCommand):
        level = capture_level()
        gold = capture_gold()
        if not gold or not level:
            return
        act_xp, total_xp = level

        xp_diff_to_level = total_xp - act_xp
        levelup_clicks = math.ceil(xp_diff_to_level / 4)
        levelup_clicks -= 1 if tft_cmd.cmd == 'lvl' and xp_diff_to_level % 4 <= 2 else 0

        while levelup_clicks > 0 and levelup_clicks * 4 <= gold:
            self.mouse.click_at(self.positions.levelup_button)
            levelup_clicks -= 1

        self.mouse.click_at(self.positions.default_click_pos)

    def handle_roll_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.roll_button)
        self.mouse.click_at(self.positions.default_click_pos)

    def handle_sell_bench_unit_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        unit_pos = self.positions.by_field(tft_cmd.unit_to_sell)
        self.mouse.drag(unit_pos, self.positions.shop_list[2])

    def handle_place_unit_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        origin_pos = self.positions.by_field(tft_cmd.unit_to_place)
        aim_pos = self.positions.by_field(tft_cmd.unit_place_aim)
        self.mouse.drag(origin_pos, aim_pos)

    def handle_collect_row_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        row = tft_cmd.row_to_collect
        start_pos = ((self.positions.board_locations[row])[0][0] - 100,
                     (self.positions.board_locations[row])[0][1])
        self.mouse.right_click_at(start_pos)
        time.sleep(2)
        end_pos = ((self.positions.board_locations[row])[6][0] + 100,
                   (self.positions.board_locations[row])[6][1])
        self.mouse.right_click_at(end_pos)

    def handle_attach_item_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        item_pos = self.positions.item_list[tft_cmd.item_to_atttach]
        unit_pos = self.positions.by_field(tft_cmd.unit_to_attach_to)
        self.mouse.drag(item_pos, unit_pos)
