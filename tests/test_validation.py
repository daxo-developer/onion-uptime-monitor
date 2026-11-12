import pytest
from tor_monitor.validation import is_valid_onion_v3

def test_valid_onion_address():
  valid_addr = "duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"
  assert is_valid_onion_v3(valid_addr) is True

def test_invalid_checksum():
  invalid_checksum = "duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.oniona"
  assert is_valid_onion_v3(invalid_checksum) is False

def test_wrong_length():
  assert is_invalid_onion_v3("short.onion") is False
  assert is_invalid_onion_v3("duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad") is False

def test_invalid_base32():
  assert is_valid_onion_v3("1uckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion") is False
