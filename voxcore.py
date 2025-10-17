"""
パス周りでどん詰まりした
公式のサンプルコードはここ → https://github.com/VOICEVOX/voicevox_core/blob/main/docs/guide/user/usage.md
"""
import winsound
from pathlib import Path
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

BASE = Path(__file__).parent.resolve()
onnx_dir = BASE / "voicevox_core" / "onnxruntime" / "lib"
dict_dir = BASE / "voicevox_core" / "dict" / "open_jtalk_dic_utf_8-1.11"
model_path = BASE / "voicevox_core" / "models" / "vvms" / "0.vvm"

# 1. Synthesizer 初期化
ort_path = onnx_dir / Onnxruntime.LIB_VERSIONED_FILENAME
synthesizer = Synthesizer(
    Onnxruntime.load_once(filename=str(ort_path)),
    OpenJtalk(str(dict_dir))
)

# 2. モデルロード
with VoiceModelFile.open(str(model_path)) as model:
    synthesizer.load_voice_model(model)

# 3. 音声合成
def out(ans):
    text = ans
    style_id = 5
    aq = synthesizer.create_audio_query(text, style_id)
    aq.speed_scale = 1.3   # ← 話速 1.3倍
    wav = synthesizer.synthesis(aq, style_id)

    #with open("output.wav", "wb") as f:
        #f.write(wav)

    winsound.PlaySound(wav, winsound.SND_MEMORY | winsound.SND_NODEFAULT)