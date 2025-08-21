from m5stack import *
from m5ui import *
from uiflow import *
import unit

setScreenColor(0x111111)

try:
  color_0 = unit.get(unit.COLOR, unit.PORTA)
except Exception as e:
  color_0 = None
  print("COLOR unit not found:", e)

try:
  synth_0 = unit.get(unit.SYNTH, (0,25))
except Exception as e:
  synth_0 = None
  print("SYNTH unit not found:", e)

# 元コードの変数（UIは変更しない）
step_number = None
target_r = None
target_g = None
target_b = None

rectangle0 = M5Rect(0, 0, 135, 120, 0xFFFFFF, 0xFFFFFF)
label0 = M5TextBox(2, 124, "color", lcd.FONT_Default, 0xFFFFFF, rotate=0)
circle0 = M5Circle(42, 175, 3, 0xFFFFFF, 0xFFFFFF)
circle1 = M5Circle(88, 175, 3, 0xFFFFFF, 0xFFFFFF)
rectangle1 = M5Rect(57, 185, 17, 25, 0xFFFFFF, 0xFFFFFF)
line0 = M5Line(M5Line.PLINE, 50, 195, 80, 195, 0xFFFFFF)

# ===== マッピング：0-255 -> 0-127 =====
def rgb_to_midi(v):
  if v is None:
    return None
  n = int((v * 127) / 255)
  return n if n < 128 else None

# 直前のノートを記憶して、変化があったときだけ更新
prev_notes = [None, None, None]

def read_and_paint():
  """カラー取得 & 画面色更新（UIは元の通り）"""
  global target_r, target_g, target_b
  if not color_0:
    return None
  target_r = color_0.red
  target_g = color_0.green
  target_b = color_0.blue
  rgb24 = (target_r << 16) | (target_g << 8) | target_b
  rectangle0.setBgColor(rgb24)
  label0.setColor(rgb24)
  return (target_r, target_g, target_b)

def apply_notes_from_rgb(r, g, b):
  """RGBをノートに変換し、前回から変化があればノート更新"""
  global prev_notes
  if not synth_0:
    return
  notes = [rgb_to_midi(r), rgb_to_midi(g), rgb_to_midi(b)]
  # 変化があれば一度停止してから鳴らす（同じノートを重ね打ちしない）
  if notes != prev_notes:
    synth_0.set_all_notes_off(0)
    for ch, nt in enumerate(notes):
      if nt is not None:
        synth_0.set_note_on(ch, nt, 127)
    prev_notes = notes

def start_continuous_sound():
  """押している間ループして連続更新"""
  if not color_0:
    return
  line0.hide()
  rectangle1.show()
  # ループ：ボタンが押されている間は連続サンプリング
  while btnA.isPressed():
    rgb = read_and_paint()
    if rgb:
      apply_notes_from_rgb(*rgb)
    wait_ms(40)  # 更新間隔（約25Hz）

def stop_sound():
  """離したら停止"""
  if synth_0:
    synth_0.set_all_notes_off(0)
  # 前回ノートをリセット
  global prev_notes
  prev_notes = [None, None, None]
  rectangle1.hide()
  line0.show()

def on_btnA_pressed():
  start_continuous_sound()
  pass

def on_btnA_released():
  stop_sound()
  pass

btnA.wasPressed(on_btnA_pressed)
btnA.wasReleased(on_btnA_released)

# 初期状態：停止表示
rectangle1.hide()
line0.show()

# 楽器設定は元コード通り
if synth_0:
  synth_0.set_instrument(0, 0, 1)
  synth_0.set_instrument(0, 1, 2)
  synth_0.set_instrument(0, 2, 3)
  synth_0.set_channel_volume(0, 100)
