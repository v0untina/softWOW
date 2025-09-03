import os
import shutil
import random

def random_digits(n=10):
    return ''.join(str(random.randint(0, 9)) for _ in range(n))

def random_mac():
    # VMware любит MAC вида 00:50:56:XX:YY:ZZ
    return "00:50:56:" + ":".join(f"{random.randint(0, 255):02X}" for _ in range(3))

vendors_models = {
    "Samsung": [
        "860 EVO", "870 EVO", "970 EVO Plus", "980 PRO"
    ],
    "Crucial": [
        "MX500"
    ],
    "Kingston": [
        "A400"
    ],
    "WDC": [
        "WD10EZEX", "Blue 3D NAND"
    ],
    "Seagate": [
        "Barracuda 7200.14", "ST1000DM010"
    ],
    "TOSHIBA": [
        "DT01ACA100"
    ],
    "Hitachi": [
        "HDS721010CLA332"
    ],
    "SanDisk": [
        "Ultra 3D"
    ],
    "Intel": [
        "660p"
    ],
    "ADATA": [
        "SU800"
    ]
}
def prepare_vm(base_dir, template_name, rom_file):
    print(f"[+] Базовая папка: {base_dir}")
    print(f"[+] Шаблон: {template_name}")
    print(f"[+] ROM-файл: {rom_file}")

    subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    nums = []
    for f in subfolders:
        if f.startswith("K") and f[1:].isdigit():
            nums.append(int(f[1:]))
    next_num = max(nums) + 1 if nums else 1
    dst_name = f"K{next_num:02d}"
    dst_folder = os.path.join(base_dir, dst_name)

    src_folder = os.path.join(base_dir, template_name)

    print(f"[+] Создаём копию {src_folder} → {dst_folder}")
    shutil.copytree(src_folder, dst_folder)

    rom_dst = os.path.join(dst_folder, "6006.ROM")
    if os.path.exists(rom_dst):
        print(f"[!] Удаляю старый ROM: {rom_dst}")
        os.remove(rom_dst)
    print(f"[+] Копирую новый ROM {rom_file} → {rom_dst}")
    shutil.copy(rom_file, rom_dst)

    vmx_path = os.path.join(dst_folder, "Windows_10_x64.vmx")
    with open(vmx_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_id = random_digits(10)
    new_mac = random_mac()

    vendor = random.choice(list(vendors_models.keys()))
    product = random.choice(vendors_models[vendor])

    # строка 64
    lines[63] = f'smbios.assetTag = "{new_id}"\n'
    print(f"[+] Строка 64 → smbios.assetTag = \"{new_id}\"")

    # строка 114
    lines[113] = f'scsi0:0.productID = "{product}"\n'
    print(f"[+] Строка 114 → scsi0:0.productID = \"{product}\"")

    # строка 115
    lines[114] = f'scsi0:0.vendorID = "{vendor}"\n'
    print(f"[+] Строка 115 → scsi0:0.vendorID = \"{vendor}\"")

    # строка 188
    lines[188] = f'ethernet0.generatedAddress = "{new_mac}"\n'
    print(f"[+] Строка 174 → ethernet0.generatedAddress = \"{new_mac}\"")

    with open(vmx_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[✓] Виртуалка готова: {dst_name}")

# --- пример запуска ---
prepare_vm(
    r"D:\YandexDisk\Долги Суровцев",   # папка где лежит template и все клоны
    "K35",                              # имя папки-шаблона
    r"C:\Users\neon4\Desktop\Asus\6006_1.ROM"  # путь к ROM
)
