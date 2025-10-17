import os, re, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
#import vox
import voxcore

load_dotenv()

# ---- 設定もろもろ -------------------
client = OpenAI(api_key=os.getenv("API_KEY"))
DATA_DIR = Path("./data")                   # 会話ログ置き場
MODEL    = ("gpt-5")
VS_ID    = os.getenv("VECTOR_STORE_ID")     # 既存ベクターストアがあれば使う
FILE_ID  = os.getenv("FILE_ID")             # 既存ファイルがあれば使う
# ------------------------------------

def parse_file_ids(raw: str | None) -> list[str]:
    if not raw:
        return []
    raw = raw.strip()
    return [s.strip() for s in raw.split(",") if s.strip()]

files_to_attach: list[str] = []

def VSatach(VS_ID: str | None = VS_ID, FILE_ID: str | None = FILE_ID):
    # 1) 既存VSがあるか？
    if VS_ID:
        print("use existing vector store:", VS_ID)
        # 既存file_id（.env）を配列化
        env_ids = parse_file_ids(FILE_ID)
        if env_ids:
            files_to_attach.extend(env_ids)
    else:
        # 新規VSを作成
        print("create new vector store")
        picked = list(DATA_DIR.glob("2024-10-*.txt"))
        print("picked:", ", ".join(p.name for p in picked))
        assert picked, "no files matched"

        # アップロード
        up_ids = []
        for p in picked:
            with p.open("rb") as f:
                up = client.files.create(file=f, purpose="user_data")
                up_ids.append(up.id)
        print(f"uploaded {len(up_ids)} files")

        # VS作成
        VS_ID = client.vector_stores.create(name="workshop-logs").id
        print("created vector store:", VS_ID)

        files_to_attach.extend(up_ids)

    # 2) VSにアタッチ（newが無ければスキップ）
    if files_to_attach:
        client.vector_stores.file_batches.create(
            vector_store_id=VS_ID,
            file_ids=files_to_attach
        )
        print(f"attached {len(files_to_attach)} files to vector store")
    else:
        print("no new files to attach; skipping file_batches.create")

    # 3) インデックス待ち
    if files_to_attach:
        for _ in range(60):  # 最大 ~60秒待ち
            items = client.vector_stores.files.list(vector_store_id=VS_ID).data
            pending = [it for it in items if getattr(it, "status", "") not in ("completed", "processed", "ready")]
            if not pending:
                break
            time.sleep(1)

# --- ここから回答生成関数 ----------
def generate_answer(question):
    prompt = f"""
あなたは3Dプリンタ・レーザーカッター作業のヘルプエージェントです。

作業者からの質問：
「{question}」

この回答は音声で提示されます。それを念頭に、聞き取りできる程度の文量で回答してください。
"""
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    resp = client.responses.create(
        model=MODEL,
        input=[{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
        tools=[{"type": "file_search", "vector_store_ids": [VS_ID]}],
    )
    return resp.output_text
# --- ここまで回答生成関数 ----------

# --- メイン処理 ----------
def main():
    print("準備中です・・・\n")
    VSatach(VS_ID, FILE_ID) # ベクターストア準備

    while True:
        question = input("\nご質問はありますか？（終了するには'exit'と入力）：\n")
        if question.lower() == 'exit':                                                                                             
            break
        elif not question.strip():
            print("質問が入力されていません。")
        else:
            print("回答を生成中です・・・")
            answer = generate_answer(question)
            print("\n=== 回答 ===\n")
            print(answer)
            #vox.out(answer)     # 通常ボイボによる音声合成
            voxcore.out(answer)  # ボイボcoreによる音声合成

if __name__ == "__main__":
    main()