## 作業会話ノウハウ抽出エージェント

「複数ペアの作業会話データ」からノウハウを抽出し、これをもとに質問に答えるエージェントです。  
作業会話だからこそ得られる、明示的・非明示的ノウハウ、作業の流れ、陥りやすいポイントなどを、生成AIによる俯瞰的観察により発見・提示することを目指します。

ファイル検索は、OpenAI API の file_search を前提としています。

VOICEVOXによる音声化処理は独立させました。これだけ引っ張って使うことも可能なはずです。

---

### 概要

- **conv_miner.py** … OpenAI API の file_search によるRAG
- **vox.py** … VOICEVOX のローカル起動を前提とした、音声化処理
- **voxcore.py** … VOICEVOXコア による音声化処理
- **VectorestoreWatcher.py** … OpenAI の Vectorstore を管理・監視するための補助コード

---

### 注意

本プログラムは、OpenAI社提供の Vectorstore が構築されている前提で作成しています。
