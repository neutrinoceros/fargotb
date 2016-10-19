# Fargo ToolBox

*This software suite is developped by* [Clément Robert](mailto:clement.robert@protonmail.com) *for* [FARGO](http://fargo.in2p3.fr/)*, a project started by Frédéric Masset.*



## Content

### longRunGenerator v0.0
longRunGenerator create more job files and launch them on the go in an append-chain. It gathers information provided in an input file formatted as input_example.dat

### dupplicate v1.0
```
dupplicate base target
```
copies the file tree of $base into a new directory $target. It excludes content from $base/output/ and OAR output files.
It also automatically edit all files newly copied to replace every occurence of $base by $target so the new simulation can in principle be ran immediatly.
Nonetheless, a security has been added to prevent over-enthousiastic users from deleted their results in $base in case something went wrong during the copy or the editing : the original executable files are deprieved of their "x" permission so it has to be turned back on manually using chmod before liftoff.


## Instalation

recommanded method : 
copy the source in the directory of your choice
```
git clone https://github.com/neutrinoceros/fargotb.git
```
then
```
cd fargotb
./install.sh
```

the script makes symbolic links for each executable file and put them into your ~/bin/ directory.
