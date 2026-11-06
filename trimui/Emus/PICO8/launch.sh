#!/bin/sh
# Lanceur PICO-8 pour TrimUI Brick Pro (firmware d'origine).
# Remplace /mnt/SDCARD/Emus/PICO8/launch.sh.
# - Si pico8_64 et pico8.dat sont dans Emus/PICO8/pico8/ : vrai PICO-8 (natif).
# - Sinon : comportement d'origine (RetroArch + coeur retro8).
# Pour quitter le PICO-8 natif : Start (menu pause) > shutdown.
echo $0 $*
RA_DIR=/mnt/SDCARD/RetroArch
EMU_DIR=/mnt/SDCARD/Emus/PICO8
P8_DIR=$EMU_DIR/pico8

$EMU_DIR/cpufreq.sh
$EMU_DIR/cpuswitch.sh

if [ -f "$P8_DIR/pico8_64" ] && [ -f "$P8_DIR/pico8.dat" ]; then
	cd "$P8_DIR"
	chmod +x pico8_64 2>/dev/null
	# correspondance des boutons : on reprend celle du systeme si elle existe
	if [ ! -f sdl_controllers.txt ] && [ -f /mnt/SDCARD/system/gamecontrollerdb.txt ]; then
		cp /mnt/SDCARD/system/gamecontrollerdb.txt sdl_controllers.txt
	fi
	# SDL2 adaptee a la console, si on en a mis une dans pico8/lib/
	export LD_LIBRARY_PATH="$P8_DIR/lib:$LD_LIBRARY_PATH"
	HOME="$P8_DIR" ./pico8_64 -home "$P8_DIR" -root_path /mnt/SDCARD/Roms/PICO8 \
		-joystick 0 -pixel_perfect 1 -run "$*" > "$P8_DIR/log.txt" 2>&1
	sync
	exit
fi

cd $RA_DIR/

#disable netplay
NET_PARAM=

HOME=$RA_DIR/ $RA_DIR/ra64.trimui -v $NET_PARAM -L $RA_DIR/.retroarch/cores/retro8_libretro.so "$*"
