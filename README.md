## infiniteadwr
This is an absolutely awful Python project which aims to allow for the automatic creation and recreation of randomized AI only games in Advanced Wars: Days of Ruin via high-level input scripts to an emulator. 

This was created largely as a practice project for learning Git and Python, as such the code and everything else within this repository is horrendous and created without a semblance of forethought. It is very unlikely anyone other than me will ever find use for this, but here it is anyway. 

Game ends are detected by open-cv and screenshots, then inputs are completed via AHK.

This implementation only supports four player maps, though this could be changed.

The map and CPU COs are randomized each game. Randomly selected COs automatically perfer to be placed on their own team, but aren't guarnteed placement on it, so that CO combinations remain random. Two of the same CO are not possible in one game.

## Future additions?
* Implementation of other CPU count games (i.e. two-player and four-player)
* A better map pool, the default 4 player maps are... mediocre. Could be achieved via: 
These could be added via design maps, and transfered via save files.
  * Adding maps to ROM via a romhack. Could modify existing romhack [AWDR: The Dawn After Ashes](https://forums.warsworldnews.com/viewtopic.php?f=37&t=14247&p=417152#p417152) to create ROM with just the new maps. Would require learning to hack ROMs for just this one thing, which would suck.
  * Adding four player design maps via in-game map design (code could be modified to handle this easily). As creating them manually is out of the question for any decently sized map-pool,these would have to be imported from an existing repository via a save file. Although these do exist, none of them have a good number of four player maps, instead being focused on two player. Either new map packs would have to be made, or code would have to be modified to handle other player counts.
* Randomization of map parameters for futher visual/gameplay variety
  * Weather (weighted toward clear, but making others possible)
  * Terrain (winter, wasteland, etc.)
* Establishment of a permanent stream of games
  * This project was created with the idea of making it possible to have a 24/7 live steam (or something similiar) of AI advance war games. This has been confirmed to be possible via conducted test streams on my personal workstation. Running it permanently, however, would require a constantly running system. I am exploring avenues with some spare equipment I have, but its unlikely any of the ancient spare machines I have will be able to even run a modern OS.

## Requirements
### Python Packages
* ahk
* pillow
* opencv-python
### Other
* MelonDS
* Advance Wars: Days of Ruin ROM
* Nintendo DS Bios and Firmware files

## Setup
After downloading repository:
* Rename melonDS_anonymized_config.ini to melonDS.ini

The necessary AWDR ROM, melonDS emulator, and NDS Bios files are *not* included in this repository; they are intelectual property and I am not risking legal issues over this project. They must be added manually to your local copy.
* Add melonDS.exe to ~\Melon DS\
* Add Advance Wars Days of Ruin.nds to ~\ADWR Rom\
* Add bios7.bin, bios9.bin, firmware.bin to ~\Melon DS\
