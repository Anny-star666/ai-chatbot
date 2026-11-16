import importlib

mods = ["requests", "charset_normalizer", "numpy", "pandas", "pyarrow", "streamlit", "dotenv"]

for m in mods:
    try:
        importlib.import_module(m)
        print(f"{m:20s} OK")
    except Exception as e:
        print(f"{m:20s} FAIL -> {e}")