//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// macos.mm - macOS-specific Objective-C/C++ functions
//
//////////////////////////////////////////////////////////////////////////

#import <Cocoa/Cocoa.h>

// Detect if we're running in Dark mode
bool IsDarkMode() {
    if (@available(macOS 10.14, *)) {
        NSString *interfaceStyle = [NSUserDefaults.standardUserDefaults valueForKey:@"AppleInterfaceStyle"];
        return [interfaceStyle isEqualToString:@"Dark"];
    } else {
        return NO;
    }
}
