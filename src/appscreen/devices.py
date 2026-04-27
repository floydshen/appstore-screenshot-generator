"""Device specifications for AppStore screenshot generation."""

from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Device type enumeration."""
    IPHONE = "iphone"
    IPAD = "ipad"


@dataclass(frozen=True)
class Device:
    """Device specification with display dimensions and Fastlane compatibility."""
    name: str
    display_size: str
    width: int
    height: int
    fastlane_name: str
    device_type: DeviceType


# iPhone devices
_IPHONE_DEVICES: list[Device] = [
    Device(
        name="iphone-6.9",
        display_size="6.9\"",
        width=1260,
        height=2736,
        fastlane_name="iPhone69",
        device_type=DeviceType.IPHONE,
    ),
    Device(
        name="iphone-6.7",
        display_size="6.7\"",
        width=1290,
        height=2796,
        fastlane_name="iPhone67",
        device_type=DeviceType.IPHONE,
    ),
    Device(
        name="iphone-6.5",
        display_size="6.5\"",
        width=1284,
        height=2778,
        fastlane_name="iPhone65",
        device_type=DeviceType.IPHONE,
    ),
    Device(
        name="iphone-6.1",
        display_size="6.1\"",
        width=1170,
        height=2532,
        fastlane_name="iPhone61",
        device_type=DeviceType.IPHONE,
    ),
    Device(
        name="iphone-5.5",
        display_size="5.5\"",
        width=1242,
        height=2208,
        fastlane_name="iPhone55",
        device_type=DeviceType.IPHONE,
    ),
]

# iPad devices
_IPAD_DEVICES: list[Device] = [
    Device(
        name="ipad-13",
        display_size="13\"",
        width=2048,
        height=2732,
        fastlane_name="iPadPro129",
        device_type=DeviceType.IPAD,
    ),
    Device(
        name="ipad-11",
        display_size="11\"",
        width=1668,
        height=2388,
        fastlane_name="iPadPro11",
        device_type=DeviceType.IPAD,
    ),
    Device(
        name="ipad-10.5",
        display_size="10.5\"",
        width=1668,
        height=2224,
        fastlane_name="iPad105",
        device_type=DeviceType.IPAD,
    ),
]

# All devices combined
_ALL_DEVICES: dict[str, Device] = {
    device.name: device for device in _IPHONE_DEVICES + _IPAD_DEVICES
}


def get_device(name: str) -> Device:
    """
    Get device specification by name.
    
    Args:
        name: Device name (e.g., "iphone-6.9", "ipad-13")
        
    Returns:
        Device specification
        
    Raises:
        ValueError: If device name is not found
    """
    if name not in _ALL_DEVICES:
        available = ", ".join(sorted(_ALL_DEVICES.keys()))
        raise ValueError(f"Unknown device '{name}'. Available devices: {available}")
    return _ALL_DEVICES[name]


def get_devices_by_type(device_type: DeviceType) -> list[Device]:
    """
    Get all devices of a specific type.
    
    Args:
        device_type: Device type (IPHONE or IPAD)
        
    Returns:
        List of devices of the specified type
    """
    if device_type == DeviceType.IPHONE:
        return _IPHONE_DEVICES.copy()
    elif device_type == DeviceType.IPAD:
        return _IPAD_DEVICES.copy()
    return []
