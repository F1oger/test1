# launch_bluestacks_3.py
import re, time, subprocess
from pathlib import Path

# === заполняйте при желании: точные имена инстансов ===
# например: ["Pie64", "Pie64_1", "Pie64_2"]
PREFERRED_INSTANCE_NAMES = []

MAX_TO_LAUNCH = 30          # запускаем не более тридцати
DELAY_BETWEEN = 5.0         # пауза между запусками, сек

def find_hd_player():
    candidates = [
        Path(r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"),
        Path(r"C:\Program Files (x86)\BlueStacks_nxt\HD-Player.exe"),
    ]
    # небольшой поиск на случай нестандартного пути
    for root in [Path(r"C:\Program Files"), Path(r"C:\Program Files (x86)")]:
        if root.exists():
            for p in root.rglob("HD-Player.exe"):
                if "BlueStacks" in p.as_posix():
                    candidates.append(p)
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Не найден HD-Player.exe. Укажите путь вручную.")

def get_instances_from_conf():
    conf = Path(r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf")
    names = set()
    if conf.exists():
        pat = re.compile(r'^bst\.instance\.([^.]+)\.')
        with conf.open('r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = pat.match(line.strip())
                if m: names.add(m.group(1))
    return sorted(names)

def get_instances_from_engine():
    engine_dir = Path(r"C:\ProgramData\BlueStacks_nxt\Engine")
    if engine_dir.exists():
        return sorted([p.name for p in engine_dir.iterdir() if p.is_dir()])
    return []

def pick_instances():
    if PREFERRED_INSTANCE_NAMES:
        return PREFERRED_INSTANCE_NAMES[:MAX_TO_LAUNCH]
    names = get_instances_from_conf()
    if not names:
        names = get_instances_from_engine()
    return names[:MAX_TO_LAUNCH]

def launch(player: Path, name: str):
    print(f"→ Запускаю {name} ...")
    subprocess.Popen([str(player), "--instance", name],
                     creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    player = find_hd_player()
    instances = pick_instances()
    if not instances:
        print("Не нашёл ни одного инстанса. Создайте их в Multi-Instance Manager "
              "или укажите имена в PREFERRED_INSTANCE_NAMES.")
        return
    print(f"HD-Player: {player}")
    print(f"К запуску: {instances}")
    for name in instances:
        launch(player, name)
        time.sleep(DELAY_BETWEEN)
    print("Готово.")

if __name__ == "__main__":
    main()
