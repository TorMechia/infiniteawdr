## infiniteadwr
This is an absolutely awful Python project which aims to allow for the automatic creation and recreation of randomized AI only games in Advanced Wars: Days of Ruin via high-level input scripts. 

This project is a work in progress.

This was created largely as a practice project for learning Git and Python, as such the code and everything else within this repository is horrendous and created without a semblance of forethought. It is very unlikely anyone other than me will ever find use for this, but here it is anyway. 

Game ends are detected by open-cv and screenshots, then inputs are completed via AHK.

This implementation only supports four player maps, though this could be changed.

The map and CPU COs are randomized each game. Randomly selected COs automatically perfer to be placed on their own team, but aren't guarnteed placement on it, so that CO combinations remain random. Two of the same CO are not possible in one game.

## Future additions?
- A better map pool, the default 4 player maps are... mediocre. These could be added via design maps, and transfered via save files.

## Requirements
### Python Packages
- ahk
- PIL
- open-cv
### Other
- MelonDS
- Advance Wars: Days of Ruin ROM
- Nintendo DS Bios and Firmware files

## Setup
After downloading repository:
- Rename melonDS_anonymized_config.ini to melonDS.ini

The AWDR rom, melonDS emulator, and NDS Bios files are not included in this repository, and must be added manually.
- Add melonDS.exe to ~\Melon DS\
- Add Advance Wars Days of Ruin.nds to ~\ADWR Rom\
- Add bios7.bin, bios9.bin, firmware.bin to ~\Melon DS\
