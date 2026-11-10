#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def parse_constant(value: str) -> bytes:
    try:
        key = bytes.fromhex(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("常量必须是十六进制字符串") from exc
    if len(key) != 33:
        raise argparse.ArgumentTypeError("常量必须为33字节")
    return bytes(byte ^ 0x7B for byte in key[1:])


def decrypt(data: bytes, key: bytes) -> bytes:
    if len(data) < 32 or len(data) % 16:
        raise ValueError("文件长度无效")
    cipher = Cipher(algorithms.AES(key), modes.CBC(data[:16]))
    decryptor = cipher.decryptor()
    padded = decryptor.update(data[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def main() -> int:
    parser = argparse.ArgumentParser(description="解密提取出的 QQ ASAR 文件")
    parser.add_argument("input", type=Path, help="输入目录")
    parser.add_argument("output", type=Path, help="输出目录")
    parser.add_argument("constant", type=parse_constant, help="原始密钥")
    args = parser.parse_args()

    source = args.input.resolve()
    destination = args.output.resolve()
    if not source.is_dir():
        parser.error("输入目录不存在")
    if source == destination or source in destination.parents or destination in source.parents:
        parser.error("输入和输出目录不能相同或互相包含")
    if destination.exists() and not destination.is_dir():
        parser.error("输出路径不是目录")

    success = failed = 0
    for path in sorted(source.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(source)
        target = destination / relative
        try:
            plaintext = decrypt(path.read_bytes(), args.constant)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(plaintext)
            print(f"成功: {relative}")
            success += 1
        except (OSError, ValueError) as exc:
            print(f"失败: {relative}: {exc}", file=sys.stderr)
            failed += 1

    print(f"成功: {success}，失败: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
