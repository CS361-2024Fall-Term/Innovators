[Setup]
AppName=EasyCal
AppVersion=1.0
DefaultDirName={userappdata}\EasyCal
DefaultGroupName=EasyCal
OutputDir=output
OutputBaseFilename=EasyCal_x64_installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Innovators\EasyCal.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Innovators\icon256.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Innovators\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs
Source: "dist\Innovators\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\EasyCal"; Filename: "{app}\main.exe"; IconFilename: "{app}\icon256.ico"
Name: "{group}\Uninstall"; Filename: "{app}\uninstall.exe"
Name: "{userdesktop}\EasyCal"; Filename: "{app}\EasyCal.exe"; IconFilename: "{app}\icon256.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons"; Flags: unchecked

[Run]
Filename: "{app}\EasyCal.exe"; Description: "Launch EasyCal"; Flags: nowait postinstall skipifsilent
