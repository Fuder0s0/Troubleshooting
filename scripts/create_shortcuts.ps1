$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')

# Atalho 1: Extrator WhatsApp SIMP
$link1 = $wsh.CreateShortcut("$desktop\Extrator WhatsApp SIMP-PE.lnk")
$link1.TargetPath = "c:\Users\tlima\Downloads\SIMP-PE\executar_extracao_whatsapp.bat"
$link1.WorkingDirectory = "c:\Users\tlima\Downloads\SIMP-PE"
$link1.Description = "Extrator automatizado de mensagens e duvidas dos grupos WhatsApp SIMP-PE"
$link1.IconLocation = "shell32.dll,13"
$link1.Save()

# Atalho 2: Central de Troubleshooting SIMP-PE
$link2 = $wsh.CreateShortcut("$desktop\Troubleshooting SIMP-PE.lnk")
$link2.TargetPath = "c:\Users\tlima\Downloads\SIMP-PE\iniciar_troubleshooting.bat"
$link2.WorkingDirectory = "c:\Users\tlima\Downloads\SIMP-PE"
$link2.Description = "Central de Troubleshooting e Solucoes do Sistema SIMP-PE"
$link2.IconLocation = "shell32.dll,220"
$link2.Save()

Write-Output "Atalhos criados com sucesso na Area de Trabalho!"
