echo off
assoc .gc = GCrypted
ftype .GCrypted = "%HOMEDRIVE%\GCrypter\GCrypter(*).exe" "%1"
