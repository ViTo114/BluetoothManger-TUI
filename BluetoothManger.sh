#! /bin/bash
tput civis

menuPrincipale()
{
dialog --menu "BluetoothManager TUI" 12 35 4 \
"Status" "" \
"Connect" "" \
"Modify Connection" "" \
" " "" \
"Exit" "" \
3>&1 1>&2 2>&3
}



menuStatus()
{
scelta=$(dialog --menu "Chose the status" 12 35 2 \
"ON" "" "OFF" "" 3>&1 1>&2 2>&3) || return

if [ "$scelta" = "ON" ]; then
  bluetoothctl power on  >/dev/null 2>&1
else
  bluetoothctl power off >/dev/null 2>&1
fi


}

menuConnect()
{
stato="$(bluetoothctl show | grep -Po '^\s*PowerState:\s*\K(on|off)')"

if [ "$stato" == "off" ]
then
dialog --title "Warning" --msgbox "Bluetooth disabled.\nEnable it to run a scan." 8 50
fi


}



while true
do
scelta=$(menuPrincipale)

if [ "$scelta" = "Status" ]
then
  menuStatus
  
elif [ "$scelta" == "Connect" ]
then
menuConnect
	
  
elif [ "$scelta" = "Exit" ]
then
  break
  
fi
done


done

