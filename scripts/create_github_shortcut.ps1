$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')
$link = $wsh.CreateShortcut("$desktop\Publicar no GitHub (Troubleshooting).lnk")
$link.TargetPath = "c:\Users\tlima\Downloads\SIMP-PE\enviar_para_github.bat"
$link.WorkingDirectory = "c:\Users\tlima\Downloads\SIMP-PE"
$link.Description = "Envia todo o projeto Troubleshooting SIMP-PE para o GitHub Fuder0s0"
$link.IconLocation = "shell32.dll,238"
$link.Save()
Write-Output "Atalho de publicacao criado no Desktop!"
