import pandas as pd

# tsvファイルのパスを指定
gdsc1_file_path = './config/gdsc/data/tsv/GDSC1.tsv'
gdsc2_file_path = './config/gdsc/data/tsv/GDSC2.tsv'
cell_lines_details_file_path = './config/gdsc/data/tsv/Cell_Lines_Details.tsv'
screened_compounds_file_path = './config/gdsc/data/tsv/screened_compounds_rel_8.5.tsv'
model_list_file_path = './config/gdsc/data/tsv/model_list_20240110.tsv'

# 各TSVファイルを読み込む
# keep_default_na=False にすると "None" や "NA" をNaNに変換しなくなる
gdsc1_df = pd.read_csv(gdsc1_file_path, sep='\t', keep_default_na=False)
gdsc2_df = pd.read_csv(gdsc2_file_path, sep='\t', keep_default_na=False)
cell_lines_details_df = pd.read_csv(cell_lines_details_file_path, sep='\t', keep_default_na=False)
screened_compounds_df = pd.read_csv(screened_compounds_file_path, sep='\t', keep_default_na=False)
model_list_df = pd.read_csv(model_list_file_path, sep='\t', keep_default_na=False, na_values=[])

# GDSC1.tsv: DRUG_NAMEが'Erlotinib' かつ CELL_LINE_NAMEが['COLO-829', 'HCC2998']
gdsc1_df_filtered = gdsc1_df[
    (gdsc1_df['DRUG_NAME'] == 'Erlotinib') &
    (gdsc1_df['CELL_LINE_NAME'].isin(['COLO-829', 'HCC2998']))
]
gdsc1_df_filtered.to_csv('./config/gdsc/data/GDSC1_small_new.tsv', sep='\t', index=False, na_rep='None')

# GDSC2.tsv: DRUG_NAMEが'Erlotinib' かつ CELL_LINE_NAMEが['COLO-829', 'HCC2998']
gdsc2_df_filtered = gdsc2_df[
    (gdsc2_df['DRUG_NAME'] == 'Erlotinib') &
    (gdsc2_df['CELL_LINE_NAME'].isin(['COLO-829', 'HCC2998']))
]
gdsc2_df_filtered.to_csv('./config/gdsc/data/GDSC2_small_new.tsv', sep='\t', index=False, na_rep='None')

# Cell_Lines_Details.tsv: cell_Sample Nameが['COLO-829', 'HCC2998']
cell_lines_details_df_filtered = cell_lines_details_df[
    cell_lines_details_df['cell_Sample Name'].isin(['COLO-829', 'HCC2998'])
]
cell_lines_details_df_filtered.to_csv('./config/gdsc/data/Cell_Lines_small_new.tsv', sep='\t', index=False, na_rep='None')

# screened_compounds_rel_8.5.tsv: drug_DRUG_IDが'1'
screened_compounds_df_filtered = screened_compounds_df[
    screened_compounds_df['drug_DRUG_ID'] == 1
]
screened_compounds_df_filtered.to_csv('./config/gdsc/data/screened_compounds_small_new.tsv', sep='\t', index=False, na_rep='None')

# model_list_20240110.tsv: mod_model_nameが['COLO-829', 'HCC2998']
model_list_df_filtered = model_list_df[
    model_list_df['mod_model_name'].isin(['COLO-829', 'HCC2998'])
]
model_list_df_filtered.to_csv('./config/gdsc/data/model_list_small_new.tsv', sep='\t', index=False, na_rep='None')
