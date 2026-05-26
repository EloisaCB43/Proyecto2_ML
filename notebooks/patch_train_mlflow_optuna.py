import json
from pathlib import Path

p = Path('train_mlflow_optuna.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
found = False
old = '    "        val = val.strip(\" ,)\")\n",\n    "        val = val.lstrip(\"(\")\n",'
new = '    "        import re\n",\n    "        val = re.sub(r\"[^0-9eE+\-.]+$\", \"\", val)\n",\n    "        val = val.strip()\n",'
text = p.read_text(encoding='utf-8')
if old not in text:
    raise SystemExit('Old snippet not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print('patched')
