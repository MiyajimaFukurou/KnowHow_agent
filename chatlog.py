import json

# --- 会話記録をjsonに積み上げ ------
def log_save(usr: str, ans: str, logfile: str = "chat_log.jsonl") -> None:
    rec = {"usr": "" if usr is None else str(usr),
           "ans": "" if ans is None else str(ans)}
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# --- 会話記録の末尾からn件を取得 ------
def last_n_chatlog(logfile: str = "chat_log.jsonl", n: int = 5):
    if n <= 0:
        return []
    out = []
    buf = b""
    chunk = 4096
    try:
        with open(logfile, "rb") as f:
            f.seek(0, 2)              # ファイル末尾へ
            pos = f.tell()
            while pos > 0 and len(out) < n:
                step = min(chunk, pos)
                pos -= step
                f.seek(pos)
                buf = f.read(step) + buf
                parts = buf.split(b"\n")
                buf = parts[0]        # 先頭は次ループで結合
                for line in reversed(parts[1:]):
                    s = line.strip()
                    if not s:
                        continue
                    try:
                        out.append(json.loads(s.decode("utf-8")))
                    except Exception:
                        # 壊れた行はスキップ
                        pass
                    if len(out) >= n:
                        break
            # ファイル先頭まで到達し、残りがあればそれも読む
            if pos == 0 and buf.strip() and len(out) < n:
                try:
                    out.append(json.loads(buf.decode("utf-8").strip()))
                except Exception:
                    pass
    except FileNotFoundError:
        return []

    return list(reversed(out))  # 古→新で返す
