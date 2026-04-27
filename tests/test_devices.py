"""Tests for device specifications."""

import pytest

from appscreen.devices import (
    Device,
    DeviceType,
    get_device,
    get_devices_by_type,
)


class TestGetDevice:
    """Tests for get_device function."""
    
    def test_get_iphone_device(self):
        """Test getting an iPhone device."""
        device = get_device("iphone-6.9")
        assert device.name == "iphone-6.9"
        assert device.display_size == "6.9\""
        assert device.width == 1260
        assert device.height == 2736
        assert device.fastlane_name == "iPhone69"
        assert device.device_type == DeviceType.IPHONE
    
    def test_get_ipad_device(self):
        """Test getting an iPad device."""
        device = get_device("ipad-13")
        assert device.name == "ipad-13"
        assert device.display_size == "13\""
        assert device.width == 2048
        assert device.height == 2732
        assert device.fastlane_name == "iPadPro129"
        assert device.device_type == DeviceType.IPAD
    
    def test_unknown_device_raises_error(self):
        """Test that unknown device raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_device("unknown-device")
        assert "Unknown device 'unknown-device'" in str(exc_info.value)
        assert "Available devices:" in str(exc_info.value)


class TestGetDevicesByType:
    """Tests for get_devices_by_type function."""
    
    def test_get_iphone_devices(self):
        """Test getting all iPhone devices."""
        devices = get_devices_by_type(DeviceType.IPHONE)
        assert len(devices) == 5
        assert all(d.device_type == DeviceType.IPHONE for d in devices)
    
    def test_get_ipad_devices(self):
        """Test getting all iPad devices."""
        devices = get_devices_by_type(DeviceType.IPAD)
        assert len(devices) == 3
        assert all(d.device_type == DeviceType.IPAD for d in devices)
    
    def test_returns_copy(self):
        """Test that returned list is a copy."""
        devices1 = get_devices_by_type(DeviceType.IPHONE)
        devices2 = get_devices_by_type(DeviceType.IPHONE)
        assert devices1 is not devices2


class TestDeviceDataclass:
    """Tests for Device dataclass."""
    
    def test_device_is_frozen(self):
        """Test that Device is immutable."""
        device = get_device("iphone-6.7")
        with pytest.raises(Exception):  # FrozenInstanceError
            device.width = 1000
    
    def test_device_attributes(self):
        """Test device attributes are correctly set."""
        device = get_device("iphone-5.5")
        assert device.name == "iphone-5.5"
        assert device.display_size == "5.5\""
        assert device.width == 1242
        assert device.height == 2208
        assert device.fastlane_name == "iPhone55"
        assert device.device_type == DeviceType.IPHONE
