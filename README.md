## infiniteawdr
A Python project which aims to allow for the automatic creation of randomized AI only games in Advanced Wars: Days of Ruin via input scripts to an emulator (MelonDS). 

In retrospect, many of the design decisions herein were poorly planned. Note that this was created largely as a practice project for learning Git and Python; as such, most of this project's design is... nonideal. 

Game ends are detected by open-cv and screenshots, then inputs are completed via AHK.

This implementation only supports four player maps, though this could be changed.

The map and CPU COs are randomized each game. Randomly selected COs automatically perfer to be placed on their "correct" team color, but are not guarnteed placement on it ("soft sorted"). This allows each CO to have the correct color most of the time, while maintaining that the exact COs in each match is completely random. The only restriction placed on random CO selection is that no two teams can have the same CO. The CO selection option of "No CO" is ignored.

## Future additions?
* Implementation of other CPU count games (i.e. two-player and four-player)
* A better map pool, the default 4 player maps are... mediocre. Could be achieved via: 
These could be added via design maps, and transfered via save files.
  * Adding maps to ROM via a romhack. Could modify existing romhack [AWDR: The Dawn After Ashes](https://forums.warsworldnews.com/viewtopic.php?f=37&t=14247&p=417152#p417152) to create ROM with just the new maps. 
  * Adding four player design maps via in-game map design (code could be modified to handle this easily). As creating them manually is out of the question for any decently sized map-pool,these would have to be imported from an existing community save file. Although these do exist, none of them have a good number of four player maps, instead being focused on two player. 
* Randomization of map parameters for futher visual/gameplay variety
  * Weather (weighted toward clear, but making others possible)
  * Terrain (winter, wasteland, etc.)
* Establishment of a permanent stream of games
  * A [proof of concept stream](https://www.youtube.com/watch?v=zHD_zqTZlN0) was already conducted, but potential is present for a long-term setup.
  * This would require implementation of a system to detect when something has gone wrong (e.g. emulator error, game stalemate), and automatically reset everything.

## Requirements
#### Python Packages
* ahk
* pillow
* opencv-python
#### Other
* [MelonDS](https://melonds.kuribo64.net/)
* Advance Wars: Days of Ruin ROM
* Nintendo DS Bios and Firmware files

## Setup
* Clone repository this repository to a Windows machine
* Rename `.\Melon DS\melonDS_anonymized_config.ini` to `melonDS.ini`

*The necessary AWDR ROM, MelonDS emulator, and NDS Bios files are *not* included in this repository; they must be added manually to your local copy.*
* Add the other required files
  * Add `melonDS.exe` to `.\Melon DS\`
  * Add `Advance Wars Days of Ruin.nds` *(your AWDR ROM)* to `.\ADWR Rom\`
  * Add `bios7.bin`, `bios9.bin`, `firmware.bin` to `.\Melon DS\`

