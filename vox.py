import requests
import io
from pygame import mixer

def out(ans):
    # デフォはコレだけど、変える必要が微レ存
    host = "127.0.0.1"
    port = 50021

    # クエリ作成
    response = requests.post(
        f'http://{host}:{port}/audio_query',
        params={"text": ans, "speaker": 1}
    )
    query = response.json()

    # 再生速度を変更
    query["speedScale"] = 1.2

    # 音声合成
    response = requests.post(
        f'http://{host}:{port}/synthesis',
        json=query,
        params={"speaker": 1}
    )

    # 音声再生
    audio_data = io.BytesIO(response.content)
    mixer.init(frequency=24000)
    mixer.music.load(audio_data, "wav")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
