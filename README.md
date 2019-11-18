# aedat4tomat
Convert AEDAT4 files from DV into .mat files for matlab

Example Usage:
```console
foo@bar:~$ python /home/username/aedat4tomat.py -i "dvFile.aedat4" -o "dvFile.mat"
```

You can also make a simple bash script that will process all aedat4 files in a directory into several .mat files. Then just call it from MATLAB using the unix command.

```
unix(['./processFolderWithInput ' pathToAedatFiles])
```
