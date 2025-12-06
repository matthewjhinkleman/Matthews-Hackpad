# ==============================
# BOARD & KMK IMPORTS
# ==============================
import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.ssd1306 import SSD1306

# ==============================
# MAIN KEYBOARD OBJECT
# ==============================
keyboard = KMKKeyboard()

# ==============================
# MACROS ENABLED
# ==============================
macros = Macros()
keyboard.modules.append(macros)

# ==============================
# YOUR REAL BUTTON PINS (6)
# ==============================
PINS = [
    board.D0,   # SW1
    board.D1,   # SW2
    board.D2,   # SW3
    board.D3,   # SW4
    board.D7,   # SW5
    board.D10,  # SW6
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# ==============================
# KEYMAP (WITH YOUR MEDIA CONTROLS)
# ==============================
keyboard.keymap = [
    [
        KC.MPRV,   # SW1  ← Media Previous (Go Back)
        KC.VOLD,   # SW2  ← Volume Down (placeholder)
        KC.MPLY,   # SW3  ← Play / Pause ✅
        KC.VOLU,   # SW4  ← Volume Up (placeholder)
        KC.MNXT,   # SW5  ← Media Next / Skip ✅
        KC.MUTE,   # SW6  ← Mute (placeholder)
    ]
]

# ==============================
# ROTARY ENCODER (VOLUME)
# ==============================
encoder = EncoderHandler()
encoder.pins = (
    (board.D8, board.D9),  # Encoder A, B
)

encoder.map = [
    (
        (KC.VOLD, KC.VOLU),  # CCW = Vol Down, CW = Vol Up ✅
    ),
]

keyboard.modules.append(encoder)

# ==============================
# OLED 0.91" SSD1306
# ==============================
i2c = busio.I2C(board.D5, board.D4)

oled = SSD1306(
    i2c=i2c,
    width=128,
    height=32,
    address=0x3C,
)

def oled_task(oled, _):
    oled.fill(0)
    oled.text("HACKPAD", 0, 0, 1)
    oled.text("Media Mode", 0, 12, 1)
    oled.text("Vol: Encoder", 0, 22, 1)
    oled.show()

oled.task = oled_task
keyboard.extensions.append(oled)

# ==============================
# START KMK
# ==============================
if __name__ == '__main__':
    keyboard.go()
