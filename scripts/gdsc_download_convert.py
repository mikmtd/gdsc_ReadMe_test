import os
import pandas as pd
import requests

# 保存先フォルダの指定
raw_dir = "data/raw"
tsv_dir = "data/tsv"

# フォルダがなければ作成
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(tsv_dir, exist_ok=True)

# ダウンロード情報
files = [
    {
        "url": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC2_fitted_dose_response_27Oct23.xlsx",
        "filename": "GDSC2_fitted_dose_response_27Oct23.xlsx",
        "output": "GDSC2.tsv",
        "prefix": None
    },
    {
        "url": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/Cell_Lines_Details.xlsx",
        "filename": "Cell_Lines_Details.xlsx",
        "output": "Cell_Lines_Details.tsv",
        "prefix": "cell_"
    },
    {
        "url": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/screened_compounds_rel_8.5.csv",
        "filename": "screened_compounds_rel_8.5.csv",
        "output": "screened_compounds_rel_8.5.tsv",
        "prefix": "drug_"
    },
    {
        "url": "https://cog.sanger.ac.uk/cmp/download/model_list_20240110.csv",
        "filename": "model_list_20240110.csv",
        "output": "model_list_20240110.tsv",
        "prefix": "mod_"
    }
]

# ダウンロードと変換処理
for f in files:
    file_path = os.path.join(raw_dir, f["filename"])
    output_path = os.path.join(tsv_dir, f["output"])

    print(f"\n📥 ダウンロード中: {f['filename']}")
    res = requests.get(f["url"])
    if res.status_code != 200:
        print(f"❌ ダウンロード失敗: {f['filename']}")
        continue
    with open(file_path, "wb") as file:
        file.write(res.content)
    print(f"✅ ダウンロード完了: {file_path}")

    # 読み込み
    print(f"📊 データ処理中: {f['filename']}")
    if f["filename"].endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    # カラム名に接頭辞を追加（指定がある場合）
    if f["prefix"]:
        df.columns = [f["prefix"] + str(col) for col in df.columns]

    # TSV形式で保存
    df.to_csv(output_path, sep="\t", index=False)
    print(f"✅ 保存完了: {output_path}")
