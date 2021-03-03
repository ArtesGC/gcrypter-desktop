echo off
echo "GCrypter"
echo "Definindo o programa padrão para os arquivos .gc \n"
runas /noprofile /user:%USERNAME%\administrator "./winFileAssoc.bat"
echo "Operação terminada.."
pause
exit