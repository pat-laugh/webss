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

Stuff that need to be installed on your machine: `npm`, `npx`, `python3`.

In the directory `back-end/`, run `init.sh` to run appropriate commands. Then
run `generate_webpage.py`. This will
generate a webpage showing the configuration from the file `config.json`. To
compile a file, run `compile.py` with the file name.

To check what input and output could look like with the current packages and
configuration, check the files in `test-data`.

## Example

Commands to run:
```
webss$ cd back-end/
webss/back-end$ ./init.sh
webss/back-end$ ./generate_webpage.py
Webpage: file://.../webss/front-end/out/index.html
```
That webpage can then be opened, and the structure of what the compiler parses
modified. For instance, within package "#1 - File", you can add the package
"Data List": hover the mouse above it, then click "Show packages", then select
"Data List" in the dropdown corresponding to the package, then click "Add
package".

You can add a data list structure in the test file:
```
webss/back-end$ echo 'var data_list = [
    2
    3
];' >>test-data/testinput.js.wbss
```

And then compile that:
```
webss/back-end$ ./compile.py test-data/testinput.js.wbss
...
```
The data list should be exactly the same as written. That's because the config
was not changed and the compiler is not set to parse data lists.

You can copy the configuration from the webpage, then overwrite the contents of
`webss/back-end/config.json`. Run the same command as before. Now, you should
see a slightly different result: a comma separates the numbers 2 and 3!

## Creating packages

At the moment, I took the compiler code and file from another project and
integrated this project with it, so it's a bit complicated what happens, but
that shall be improved in the future.
