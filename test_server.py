#!/usr/bin/env python3
"""
Quick test script for Keynote-MCP Server
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_server_initialization():
    """Test if the server can be initialized"""
    try:
        from src.server import KeynoteMCPServer
        server = KeynoteMCPServer()
        print("✅ Server initialization: SUCCESS")
        return server
    except Exception as e:
        print(f"❌ Server initialization: FAILED - {e}")
        return None

def test_tools_loading(server):
    """Test if all tools can be loaded"""
    try:
        tools = []
        tools.extend(server.presentation_tools.get_tools())
        tools.extend(server.slide_tools.get_tools()) 
        tools.extend(server.content_tools.get_tools())
        tools.extend(server.export_tools.get_tools())
            
        print(f"✅ Tools loading: SUCCESS ({len(tools)} tools loaded)")
        return tools
    except Exception as e:
        print(f"❌ Tools loading: FAILED - {e}")
        return []

def test_applescript_runner():
    """Test if AppleScript runner works"""
    try:
        from src.utils import AppleScriptRunner
        runner = AppleScriptRunner()
        
        # Test basic AppleScript execution
        result = runner.run_inline_script('return "Hello from AppleScript"')
        if result == "Hello from AppleScript":
            print("✅ AppleScript execution: SUCCESS")
            return True
        else:
            print(f"❌ AppleScript execution: UNEXPECTED RESULT - {result}")
            return False
    except Exception as e:
        print(f"❌ AppleScript execution: FAILED - {e}")
        return False

def test_keynote_availability():
    """Test if Keynote is available"""
    try:
        from src.utils import AppleScriptRunner
        runner = AppleScriptRunner()
        
        # Check if Keynote app exists
        script = '''
        try
            tell application "Finder"
                return exists application file id "com.apple.Keynote"
            end tell
        on error
            return false
        end try
        '''
        
        result = runner.run_inline_script(script)
        if result.lower() == "true":
            print("✅ Keynote availability: SUCCESS")
            return True
        else:
            print("⚠️  Keynote availability: NOT FOUND")
            print("   Please install Keynote from the App Store")
            return False
    except Exception as e:
        print(f"❌ Keynote availability: FAILED - {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Keynote-MCP Server Test Suite")
    print("=" * 40)
    
    # Test server initialization
    server = test_server_initialization()
    if not server:
        print("\n❌ Cannot proceed with tests - server initialization failed")
        return False
    
    # Test tools loading
    tools = test_tools_loading(server)
    if not tools:
        print("\n❌ Cannot proceed with tests - no tools loaded")
        return False
    
    # Test AppleScript runner
    applescript_ok = test_applescript_runner()
    
    # Test Keynote availability
    keynote_ok = test_keynote_availability()
    
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    print(f"   Server initialization: {'✅' if server else '❌'}")
    print(f"   Tools loading: {'✅' if tools else '❌'}")
    print(f"   AppleScript execution: {'✅' if applescript_ok else '❌'}")
    print(f"   Keynote availability: {'✅' if keynote_ok else '⚠️'}")
    
    all_critical_passed = server and tools and applescript_ok
    
    if all_critical_passed:
        print("\n🎉 All critical tests passed!")
        print("   The server should work with Claude Desktop.")
        if not keynote_ok:
            print("   Note: Install Keynote for full functionality.")
    else:
        print("\n💥 Some critical tests failed!")
        print("   Please check the errors above and fix them.")
    
    return all_critical_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
