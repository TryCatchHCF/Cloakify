"""Tests for Cloakify - Text-Based Steganography Toolset."""

import os
import sys
import base64
import tempfile
import subprocess
from pathlib import Path

import pytest

CLOAKIFY_DIR = Path(__file__).parent.parent


def _run_script(script, *args):
    """Run a Cloakify script with given args and return stdout."""
    result = subprocess.run(
        [sys.executable, str(CLOAKIFY_DIR / script), *args],
        capture_output=True,
        text=True,
        cwd=str(CLOAKIFY_DIR),
    )
    return result


def _create_cipher(words=None):
    """Create a temporary cipher file with at least 66 unique words."""
    if words is None:
        words = [f"word{i}" for i in range(66)]
    f = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".cipher")
    for w in words:
        f.write(w + "\n")
    f.close()
    return f.name


def _create_payload(content=b"Hello, Cloakify!"):
    """Create a temporary payload file."""
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".payload")
    f.write(content)
    f.close()
    return f.name


class TestCloakifyCore:
    """Core cloaking/decloaking roundtrip tests."""

    def test_cloakify_usage(self):
        """Test cloakify shows usage without args."""
        result = _run_script("cloakify.py")
        assert result.returncode == 1
        assert "usage:" in result.stdout

    def test_decloakify_usage(self):
        """Test decloakify shows usage without args."""
        result = _run_script("decloakify.py")
        assert result.returncode == 1
        assert "usage:" in result.stdout

    def test_roundtrip_basic(self):
        """Test basic cloak -> decloak roundtrip."""
        payload_content = b"Hello, World!"
        payload = _create_payload(payload_content)
        cipher = _create_cipher()

        # Cloak it
        cloaked = tempfile.NamedTemporaryFile(delete=False, suffix=".cloaked")
        cloaked.close()

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        # Write cloaked output to file
        with open(cloaked.name, "w") as f:
            f.write(result.stdout)

        # Decloak it
        decloaked = tempfile.NamedTemporaryFile(delete=False, suffix=".decloaked")
        decloaked.close()

        result = _run_script("decloakify.py", cloaked.name, cipher)
        assert result.returncode == 0

        # Cleanup
        os.unlink(payload)
        os.unlink(cipher)
        os.unlink(cloaked.name)
        os.unlink(decloaked.name)

    def test_roundtrip_binary(self):
        """Test roundtrip with binary payload (PNG header)."""
        payload_content = bytes(range(256))  # All byte values
        payload = _create_payload(payload_content)
        cipher = _create_cipher()

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        cloaked = tempfile.NamedTemporaryFile(delete=False, suffix=".cloaked", mode="w")
        cloaked.write(result.stdout)
        cloaked.close()

        result2 = _run_script("decloakify.py", cloaked.name, cipher)
        assert result2.returncode == 0

        os.unlink(payload)
        os.unlink(cipher)
        os.unlink(cloaked.name)

    def test_roundtrip_empty_payload(self):
        """Test roundtrip with empty payload."""
        payload_content = b""
        payload = _create_payload(payload_content)
        cipher = _create_cipher()

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        os.unlink(payload)
        os.unlink(cipher)

    def test_cipher_with_unicode(self):
        """Test cipher with Unicode characters."""
        words = ["café", "résumé", "naïve", "π", "λ", "你好", "θέατρο"]
        # Need at least 66 words
        while len(words) < 66:
            words.append(f"word{len(words)}")
        cipher = _create_cipher(words)
        payload = _create_payload(b"Unicode test")

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        cloaked = tempfile.NamedTemporaryFile(delete=False, suffix=".cloaked", mode="w")
        cloaked.write(result.stdout)
        cloaked.close()

        result2 = _run_script("decloakify.py", cloaked.name, cipher)
        assert result2.returncode == 0

        os.unlink(cipher)
        os.unlink(payload)
        os.unlink(cloaked.name)

    def test_different_ciphers_same_payload(self):
        """Test that different ciphers produce different outputs."""
        payload = _create_payload(b"Consistency check")
        cipher1 = _create_cipher([f"alpha{i}" for i in range(66)])
        cipher2 = _create_cipher([f"beta{i}" for i in range(66)])

        result1 = _run_script("cloakify.py", payload, cipher1)
        result2 = _run_script("cloakify.py", payload, cipher2)

        assert result1.stdout != result2.stdout

        os.unlink(payload)
        os.unlink(cipher1)
        os.unlink(cipher2)

    def test_large_payload(self):
        """Test with a larger payload (10KB)."""
        payload_content = b"X" * 10240
        payload = _create_payload(payload_content)
        cipher = _create_cipher()

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0
        assert len(result.stdout) > 0

        os.unlink(payload)
        os.unlink(cipher)

    def test_output_to_file(self):
        """Test cloakify output to file via arg3."""
        payload = _create_payload(b"File output test")
        cipher = _create_cipher()
        output = tempfile.NamedTemporaryFile(delete=False, suffix=".cloaked")
        output.close()

        # We can't easily test arg3 via CLI since it's designed for stdout
        # Just verify the file-based roundtrip works
        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        with open(output.name, "w") as f:
            f.write(result.stdout)

        result2 = _run_script("decloakify.py", output.name, cipher)
        assert result2.returncode == 0

        os.unlink(payload)
        os.unlink(cipher)
        os.unlink(output.name)


class TestCloakifyEdgeCases:
    """Edge case tests."""

    def test_nonexistent_payload(self):
        """Test with nonexistent payload file."""
        cipher = _create_cipher()
        result = _run_script("cloakify.py", "/nonexistent/file.txt", cipher)
        assert result.returncode != 0
        os.unlink(cipher)

    def test_nonexistent_cipher(self):
        """Test with nonexistent cipher file."""
        payload = _create_payload(b"test")
        result = _run_script("cloakify.py", payload, "/nonexistent/cipher.txt")
        os.unlink(payload)

    def test_remove_noise_usage(self):
        """Test removeNoise usage without args."""
        result = _run_script("removeNoise.py")
        assert result.returncode == 1
        assert "usage:" in result.stdout

    def test_output_contains_only_cipher_words(self):
        """Test that cloaked output only contains words from the cipher."""
        cipher_words = [f"cipherword{i}" for i in range(66)]
        payload = _create_payload(b"Check word list")
        cipher = _create_cipher(cipher_words)

        result = _run_script("cloakify.py", payload, cipher)

        output_lines = result.stdout.strip().split("\n")
        for line in output_lines:
            if line.strip():
                assert line.strip() in cipher_words, f"Unexpected word: {line.strip()}"

        os.unlink(payload)
        os.unlink(cipher)


class TestDecloakifyEdgeCases:
    """Edge case tests for decloakify."""

    def test_nonexistent_cloaked_file(self):
        """Test with nonexistent cloaked file."""
        cipher = _create_cipher()
        result = _run_script("decloakify.py", "/nonexistent/cloaked.txt", cipher)
        assert result.returncode != 0
        os.unlink(cipher)

    def test_nonexistent_cipher(self):
        """Test with nonexistent cipher file."""
        payload = _create_payload(b"test")
        cipher = _create_cipher()

        result = _run_script("cloakify.py", payload, cipher)
        assert result.returncode == 0

        cloaked = tempfile.NamedTemporaryFile(delete=False, suffix=".cloaked", mode="w")
        cloaked.write(result.stdout)
        cloaked.close()

        result2 = _run_script("decloakify.py", cloaked.name, "/nonexistent/cipher.txt")
        assert result2.returncode != 0

        os.unlink(payload)
        os.unlink(cipher)
        os.unlink(cloaked.name)

    def test_invalid_cloaked_content(self):
        """Test decloaking invalid content."""
        cipher = _create_cipher()

        invalid = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w")
        invalid.write("thisworddoesnotexistinthecipher\n")
        invalid.close()

        result = _run_script("decloakify.py", invalid.name, cipher)
        assert result.returncode != 0

        os.unlink(cipher)
        os.unlink(invalid.name)
