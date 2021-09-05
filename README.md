# WebSS Syntax Configuration

The aim of this project is to make the equivalent of a precompiler where
specific sections of text can be transformed appropriately over another
language.

For instance, one "package"/"module" can be made such that tab blocks can be
used instead of blocks with braces. Something like:
```
if (true):
	console.log('text');
```
Would be serialized to:
```
if (true) {
	console.log('text');
}
```
If only that one package is used, then that's the only transformation that would
happen.

A front end allows to determine what packages will be used, to generate
configuration that can then be used by the compiler, so there is no need to
manipulate text.

You can compare files in `front-end/js-original` and `front-end/js-wbss` to see
how this product can allow you to change the syntax of a language.

## Loading the project

In the directory `back-end/`, run `init.sh` to run appropriate commands. Then
run `generate_webpage.py`. This will
generate a webpage showing the configuration from the file `config.json`. To
compile a file, run `compile.py` with the file name.

## Creating packages

At the moment, I took the compiler code and file from another project and
integrated this project with it, so it's a bit complicated what happens, but
that shall be improved in the future.
