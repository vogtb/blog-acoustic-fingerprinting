# Acoustic Fingerprinting Television

This is the repo that accompanies the blog post for [http://benvogt.io/blog/acoustic-fingerprinting-television/](http://benvogt.io/blog/acoustic-fingerprinting-television/).


### Loading data to fingerprint database

Copyright law and sheer size of data keeps me from uploading my test data, but here's how you would load test data, if you had it.

```bash
python src/python/load.py -d=/Users/bvogt/dev/data/the_drew_carey_show/wav/
```


### Looking up a .wav sample

```bash
python src/python/lookup.py -f=/Users/bvogt/dev/data/distorted_dcs/s01e10_dist.wav
```


### Plot a .wav sample

```bash
python src/python/plot.py -f=/Users/bvogt/dev/data/distorted_dcs/s01e10_dist.wav
```


### Cut clips of all .wav files in a directory

```bash
python src/python/clips.py -d=/Users/bvogt/dev/data/the_drew_carey_show/wav/ -o=/Users/bvogt/dev/data/samples/
```


### Analyze clips, plotting results

```bash
python src/python/analyze.py -d=/Users/bvogt/dev/data/samples/ -o=/Users/bvogt/dev/data/samples/
```
