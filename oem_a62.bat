@REM # A62/A52 (IDV)
z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear
z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0
z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa
z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050
z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1
z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0
z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 2
z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1
z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 2
z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051097V1110100"

