import os
from tempfile import TemporaryDirectory

import pytest

from cloakify import Cloakify
from decloakify import Decloakify

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CIPHER_DIR = os.path.join(ROOT_DIR, "ciphers")


def test_duplicate_cipher_lines():
    for cipher_name in os.listdir(CIPHER_DIR):
        cipher_path = os.path.join(CIPHER_DIR, cipher_name)
        seen_lines = set()
        with open(cipher_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                assert line not in seen_lines
                seen_lines.add(line)


def test_ciphers():
    payload_path = os.path.join(ROOT_DIR, "README.md")

    with TemporaryDirectory() as temp_dir:
        cloaked_path = os.path.join(temp_dir, "cloaked.file")
        decloaked_path = os.path.join(temp_dir, "decloaked.file")
        for cipher_name in os.listdir(CIPHER_DIR):
            cipher_path = os.path.join(CIPHER_DIR, cipher_name)
            Cloakify(payload_path, cipher_path, cloaked_path)
            Decloakify(cloaked_path, cipher_path, decloaked_path)
            
            with open(payload_path, "r") as payload_fp, open(decloaked_path, "r") as decloaked_fp:
                assert payload_fp.read() == decloaked_fp.read()


def test_ciphers_with_password():
    password = "test1234567890"
    payload_path = os.path.join(ROOT_DIR, "README.md")

    with TemporaryDirectory() as temp_dir:
        cloaked_path = os.path.join(temp_dir, "cloaked.file")
        decloaked_path = os.path.join(temp_dir, "decloaked.file")
        for cipher_name in os.listdir(CIPHER_DIR):
            cipher_path = os.path.join(CIPHER_DIR, cipher_name)
            Cloakify(payload_path, cipher_path, cloaked_path, password)
            Decloakify(cloaked_path, cipher_path, decloaked_path, password)
            
            with open(payload_path, "r") as payload_fp, open(decloaked_path, "r") as decloaked_fp:
                assert payload_fp.read() == decloaked_fp.read()

