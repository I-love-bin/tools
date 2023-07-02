param (
  [string]$ProcessName,
  [string]$DumpFile
)

function Create-File {
  param (
    [string]$Filename
  )
  if( !(Test-Path $FileName) ){
    New-Item -Path . -Name $FileName -ItemType File -Force
  }
}
$HereDoc = @"
  public enum MINIDUMP_TYPE
  {
    Normal = 0x00000000,
    WithDataSegs = 0x00000001,
    WithFullMemory = 0x00000002,
    WithHandleData = 0x00000004,
    FilterMemory = 0x00000008,
    ScanMemory = 0x00000010,
    WithUnloadedModules = 0x00000020,
    WithIndirectlyReferencedMemory = 0x00000040,
    FilterModulePaths = 0x00000080,
    WithProcessThreadData = 0x00000100,
    WithPrivateReadWriteMemory = 0x00000200,
    WithoutOptionalData = 0x00000400,
    WithFullMemoryInfo = 0x00000800,
    WithThreadInfo = 0x00001000,
    WithCodeSegs = 0x00002000
  }
  
  [DllImport("dbghelp.dll",CharSet=CharSet.Auto,ExactSpelling=true)]
  public static extern bool MiniDumpWriteDump(
    IntPtr hProcess,
    uint ProcessId,
    IntPtr hFile,
    MINIDUMP_TYPE DumpType,
    IntPtr ExceptionParam,
    IntPtr UserStreamParam,
    IntPtr CallbackParam
  );

  [DllImport("user32.dll",CharSet=CharSet.Auto,ExactSpelling=true)]
  public static extern int MessageBoxW(
    IntPtr hWnd,
    string lpText,
    string lpCaption,
    uint uType 
  );

  [DllImport("kernel32.dll",CharSet=CharSet.Auto,ExactSpelling=true)]
  public static extern uint GetLastError();
"@

$Win32API = Add-Type -MemberDefinition $HereDoc -Name 'Win32' -Namespace Win32Functions -PassThru
$Process = Get-Process $ProcessName
for ( $count = 0 ; $count -lt $Process.Length ; $count++ ){
  $DumpFile = $DumpFile + "_" + [string]$count
  Create-File $DumpFile
  $FileProp = [System.IO.File]::Create($DumpFile)
  [Win32Functions.win32]::MiniDumpWriteDump($Process[$count].Handle, $Process[$count].Id, $FileProp.Handle, 0x2, [IntPtr]::Zero, [IntPtr]::Zero, [IntPtr]::Zero)
  [Win32Functions.Win32]::GetLastError()
  $FileProp.Close()
}