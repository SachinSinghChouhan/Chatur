"""Test different pycaw methods"""

from pycaw.pycaw import AudioUtilities
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

print("Testing pycaw volume control methods...\n")

# Method 1: Direct AudioUtilities
print("=" * 60)
print("Method 1: AudioUtilities.GetSpeakers()")
print("=" * 60)

try:
    devices = AudioUtilities.GetSpeakers()
    print(f"✅ Got device: {devices}")
    print(f"   Type: {type(devices)}")
    print(f"   Dir: {[x for x in dir(devices) if not x.startswith('_')][:10]}")
    
    # Try to get volume interface
    from pycaw.pycaw import IAudioEndpointVolume
    
    # Check if device has Activate method
    if hasattr(devices, 'Activate'):
        print("   ✅ Has Activate method")
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        print(f"   ✅ Current volume: {int(current * 100)}%")
    else:
        print("   ❌ No Activate method")
        
        # Try alternative
        if hasattr(devices, 'EndpointVolume'):
            print("   ✅ Has EndpointVolume property")
            volume = devices.EndpointVolume
            print(f"   Type: {type(volume)}")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 2: Using sessions
print("\n" + "=" * 60)
print("Method 2: AudioUtilities.GetAllSessions()")
print("=" * 60)

try:
    sessions = AudioUtilities.GetAllSessions()
    print(f"✅ Got {len(list(sessions))} sessions")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Method 3: Direct COM
print("\n" + "=" * 60)
print("Method 3: Direct COM Interface")
print("=" * 60)

try:
    from comtypes import CoCreateInstance, GUID
    from pycaw.pycaw import IMMDeviceEnumerator, EDataFlow, ERole, IAudioEndpointVolume
    
    # CLSID for MMDeviceEnumerator
    CLSID_MMDeviceEnumerator = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
    
    deviceEnumerator = CoCreateInstance(
        CLSID_MMDeviceEnumerator,
        IMMDeviceEnumerator,
        CLSCTX_ALL
    )
    print("✅ Created device enumerator")
    
    defaultDevice = deviceEnumerator.GetDefaultAudioEndpoint(
        EDataFlow.eRender.value, ERole.eMultimedia.value
    )
    print("✅ Got default device")
    
    interface = defaultDevice.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("✅ Got volume interface")
    
    current = volume.GetMasterVolumeLevelScalar()
    print(f"✅ Current volume: {int(current * 100)}%")
    
    # Test setting volume
    print("\nTesting volume control...")
    volume.SetMasterVolumeLevelScalar(0.75, None)
    print("✅ Set to 75%")
    
    new_vol = volume.GetMasterVolumeLevelScalar()
    print(f"✅ Verified: {int(new_vol * 100)}%")
    
    print("\n🎉 SUCCESS! Method 3 works!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing Complete")
print("=" * 60)
