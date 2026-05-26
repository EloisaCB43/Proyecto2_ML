import json
from pathlib import Path

p = Path('train_mlflow_optuna.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
found = False
new_source = [
    'def parse_mlflow_param(value):\n',
    '    if value is None:\n',
    '        return None\n',
    '    if isinstance(value, str):\n',
    '        val = value.strip()\n',
    '        if val == "None":\n',
    '            return None\n',
    '        import re\n',
    '        val = re.sub(r"[^0-9eE+\-.]+$", "", val)\n',
    '        val = val.strip()\n',
    '        if val.lower() in {"true", "false"}:\n',
    '            return val.lower() == "true"\n',
    '        for cast in (int, float):\n',
    '            try:\n',
    '                return cast(val)\n',
    '            except ValueError:\n',
    '                continue\n',
    '        return val\n',
    '    return value\n',
    '\n',
    'params = {}\n',
    'for k, v in best_run["params"].items():\n',
    '    parsed = parse_mlflow_param(v)\n',
    '    if parsed is not None:\n',
    '        params[k] = parsed\n',
    '\n',
    'model_family = best_run["model_family"]\n',
    '\n',
    'if model_family == "random_forest":\n',
    '    params["random_state"] = 42\n',
    '    params["n_jobs"] = -1\n',
    '    model = RandomForestRegressor(**params)\n',
    'elif model_family == "lightgbm":\n',
    '    params.pop("verbosity", None)\n',
    '    params["random_state"] = 42\n',
    '    model = LGBMRegressor(**params, verbosity=-1)\n',
    'else:\n',
    '    raise ValueError(f"Modelo no soportado para importancias: {model_family}")\n',
]
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code' and any(line.startswith('def parse_mlflow_param(value):') for line in cell.get('source', [])):
        cell['source'] = new_source
        found = True
        break
if not found:
    raise SystemExit('parse_mlflow_param cell not found')

p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('patched')
