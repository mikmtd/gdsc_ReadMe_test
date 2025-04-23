import os
import pandas as pd
import requests
import re

# 保存先フォルダの指定
raw_dir = "config/gdsc/data/raw"
tsv_dir = "config/gdsc/data/tsv"

# フォルダがなければ作成
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(tsv_dir, exist_ok=True)

# ダウンロード情報
files = [
    {
        "url": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC1_fitted_dose_response_27Oct23.xlsx",
        "filename": "GDSC1_fitted_dose_response_27Oct23.xlsx",
        "output": "GDSC1.tsv",
        "prefix": None
    },
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

    # 読み込み&na_values=[] → "None" や "NA" を NaN に変換しない
    print(f"📊 データ処理中: {f['filename']}")
    if f["filename"].endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path, na_values=[], keep_default_na=False)

    # カラム名の整形（改行除去 + 接頭辞）
    clean_columns = [re.sub(r'\s+', ' ', str(col)).strip() for col in df.columns]
    if f["prefix"]:
        df.columns = [f["prefix"] + col for col in clean_columns]
    else:
        df.columns = clean_columns

    # 特定ファイルに対するID列の変換（.0除去）
    if f["output"] == "Cell_Lines_Details.tsv":
        col_name = "cell_COSMIC identifier"
        if col_name in df.columns:
            df[col_name] = df[col_name].apply(
                lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else str(x)
            )

    elif f["output"] in ["GDSC1.tsv", "GDSC2.tsv"]:
        col_name = "MAX_CONC"
        if col_name in df.columns:
            df[col_name] = df[col_name].apply(
                lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else str(x)
            )

    # セルの中身も空白を除去（前後）
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # TSV形式で保存
    df.to_csv(output_path, sep="\t", index=False)
    print(f"✅ 保存完了: {output_path}")
