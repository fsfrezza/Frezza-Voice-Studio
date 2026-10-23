#!/usr/bin/env python3
"""Importa uma voz e retrato como perfil nativo no VoiceStudio local.

Uso:
  python scripts/install_locutor_profile.py --audio locutor.wav --image retrato.jpg
O backend precisa estar em execucao (porta 3900 por padrao).
"""
import argparse
import json
import mimetypes
import pathlib
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
import uuid


def multipart(fields, files):
    boundary = "----frezza-" + uuid.uuid4().hex
    chunks = []
    def add(s):
        chunks.append(s if isinstance(s, bytes) else s.encode("utf-8"))
    for key, value in fields.items():
        add(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n")
    for key, path, mime in files:
        add(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n")
        add(path.read_bytes())
        add("\r\n")
    add(f"--{boundary}--\r\n")
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def run():
    parser = argparse.ArgumentParser(description="Instalar perfil nativo do locutor")
    parser.add_argument("--audio", required=True, type=pathlib.Path)
    parser.add_argument("--image", type=pathlib.Path)
    parser.add_argument("--name", default="Locutor DBZ")
    parser.add_argument("--ref-text", default="", help="Transcricao exata do audio de referencia (opcional)")
    parser.add_argument("--url", default="http://127.0.0.1:3900")
    args = parser.parse_args()
    if not args.audio.is_file():
        parser.error("O audio de referencia nao foi encontrado")
    if args.image and not args.image.is_file():
        parser.error("A imagem nao foi encontrada")
    with tempfile.TemporaryDirectory(prefix="frezza-voice-") as td:
        wav = pathlib.Path(td) / "reference.wav"
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            parser.error("ffmpeg nao encontrado no PATH; necessario para normalizar a referencia")
        # A extensao do arquivo recebido pode nao refletir o codec.
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(args.audio), "-vn", "-ac", "1", "-ar", "24000",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        files = [("ref_audio", wav, "audio/wav")]
        if args.image:
            files.append(("image", args.image, "image/jpeg" if args.image.suffix.lower() in (".jpg", ".jpeg") else "image/png"))
        body, ctype = multipart(
            {"name": args.name, "kind": "clone", "language": "Auto", "ref_text": args.ref_text},
            files,
        )
        request = urllib.request.Request(
            args.url.rstrip("/") + "/profiles", data=body,
            headers={"Content-Type": ctype, "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            raise SystemExit(f"Backend retornou HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
        except urllib.error.URLError as exc:
            raise SystemExit(f"Nao foi possivel acessar {args.url}: {exc.reason}") from exc
        print(json.dumps({"id": result.get("id"), "name": result.get("name"), "kind": result.get("kind")}, ensure_ascii=False, indent=2))
        print("Perfil criado. Selecione-o em Generate (texto) ou Convert (audio).")


if __name__ == "__main__":
    run()
