# aedat4tomat
Convert AEDAT4 files from DV into .mat files for matlab. Python is required (recommend Anaconda).

First install the dv module...
```
pip install dv
```

Example Conversion:
```console
foo@bar:~$ python /home/username/aedat4tomat.py -i "dvFile.aedat4" -o "dvFile.mat"
```

You can also make a simple bash script that will process all aedat4 files in a directory into several .mat files. Then just call it from MATLAB using the unix command.

```
unix(['./processFolderWithInput ' pathToAedatFiles])
```

(This code is designed to work with aedat4 that contains frames, events, and imu streams. If your data does not have all these fields, just comment out the sections of aedat4tomat.py that deal with the data you are missing.)
