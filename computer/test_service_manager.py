"""
Test script for Service Manager
Tests the background service functionality
"""

import time
import threading
from chatur.service.service_manager import ServiceManager, ManagedService

def test_service_callback(stop_event: threading.Event):
    """Simple test callback that runs for a few seconds"""
    print("Test service started!")
    
    counter = 0
    while not stop_event.is_set():
        counter += 1
        print(f"Service running... {counter}")
        time.sleep(1)
        
        # Stop after 5 iterations for testing
        if counter >= 5:
            break
    
    print("Test service stopped!")

def test_basic_service_manager():
    """Test basic ServiceManager functionality"""
    print("=" * 60)
    print("Testing ServiceManager")
    print("=" * 60)
    
    # Create service manager
    manager = ServiceManager(test_service_callback)
    
    # Test start
    print("\n1. Starting service...")
    assert manager.start() == True
    assert manager.is_running() == True
    print("✓ Service started")
    
    # Wait a bit
    time.sleep(2)
    
    # Test stop
    print("\n2. Stopping service...")
    assert manager.stop() == True
    assert manager.is_running() == False
    print("✓ Service stopped")
    
    # Test restart
    print("\n3. Testing restart...")
    assert manager.start() == True
    time.sleep(1)
    assert manager.restart() == True
    assert manager.is_running() == True
    print("✓ Restart successful")
    
    # Final stop
    time.sleep(2)
    manager.stop()
    
    print("\n✓ All ServiceManager tests passed!")

def test_managed_service():
    """Test ManagedService with command queue"""
    print("\n" + "=" * 60)
    print("Testing ManagedService")
    print("=" * 60)
    
    # Create managed service
    managed = ManagedService(test_service_callback, auto_restart=False)
    
    # Start control loop
    print("\n1. Starting control loop...")
    managed.start_control_loop()
    time.sleep(0.5)
    print("✓ Control loop started")
    
    # Send start command
    print("\n2. Sending START command...")
    managed.send_command('start')
    time.sleep(2)
    assert managed.service_manager.is_running() == True
    print("✓ Service started via command")
    
    # Send stop command
    print("\n3. Sending STOP command...")
    managed.send_command('stop')
    time.sleep(1)
    assert managed.service_manager.is_running() == False
    print("✓ Service stopped via command")
    
    # Shutdown
    print("\n4. Shutting down...")
    managed.shutdown()
    print("✓ Shutdown complete")
    
    print("\n✓ All ManagedService tests passed!")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SERVICE MANAGER TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_basic_service_manager()
        test_managed_service()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
