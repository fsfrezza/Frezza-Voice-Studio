#!/usr/bin/env python3
"""Importa o fonte público do VoiceStudio v0.5.6 e aplica apenas branding/build.
Nao altera nem contorna verificacoes de licenca de modelos.
"""
import pathlib
import re
import shutil
import sys

source = pathlib.Path(sys.argv[1]).resolve()
dest = pathlib.Path(sys.argv[2]).resolve()
if not (source / "LICENSE").is_file() or not (source / "electron/electron-builder.config.mjs").is_file():
    raise SystemExit("Fonte VoiceStudio incompleto; abortando importacao")

for child in source.iterdir():
    if child.name in {".git", ".github", "README.md"}:
        continue
    target = dest / child.name
    if child.is_dir():
        shutil.copytree(child, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
    else:
        shutil.copy2(child, target)

cfg = dest / "electron/electron-builder.config.mjs"
s = cfg.read_text(encoding="utf-8")
s = s.replace("appId: 'com.voicestudio.desktop'", "appId: 'br.frezza.voicestudio'")
s = s.replace("productName: 'VoiceStudio'", "productName: 'Frezza Voice Studio'")
s = s.replace("artifactName: 'VoiceStudio-Electron-${version}-${os}-${arch}.${ext}'", "artifactName: 'Frezza-Voice-Studio-${version}-${os}-${arch}.${ext}'")
# Nao distribuir um fork com feed de update de terceiros.
s = re.sub(r"const updateUrl = updateChannel.startsWith\('electron-preview-'\)[\s\S]*?;\n", "const updateUrl = 'https://github.com/fsfrezza/Frezza-Voice-Studio/releases/latest/download';\n", s, count=1)
cfg.write_text(s, encoding="utf-8")

pkg = dest / "electron/package.json"
s = pkg.read_text(encoding="utf-8")
s = s.replace('"homepage": "https://github.com/debpalash/VoiceStudio"', '"homepage": "https://github.com/fsfrezza/Frezza-Voice-Studio"')
s = s.replace('"desktopName": "VoiceStudio"', '"desktopName": "Frezza Voice Studio"')
s = s.replace('"productName": "VoiceStudio"', '"productName": "Frezza Voice Studio"')
pkg.write_text(s, encoding="utf-8")
print("Importacao concluida. Licenca e verificacoes de modelos preservadas.")
