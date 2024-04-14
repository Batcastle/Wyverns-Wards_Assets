# Contributing to the Library

All files in the library are in JSON format, unless they are in the __Assets__ folder. In which case, the following file formats are used for the following data:

 - Video: MP4 or WEBM
 - Image: PNG or WEBP
 - Sound: OGG or FLAC
 
All JSON data has a standard format. There are 2 general types of JSON files:

 - Key files: simply provide shorthand keys that allow W&W to more easily know what certain acronyms mean. This may also be used for conjugation and translation later.
 - Data files: provide data for the rest of W&W, such as info on animals, classes, or races
 
Key files all follow a standard format:

```json
    {
        "KEY": "Value"
    }
```

for example:

```json
    {
        "SNM": "Slashing (non-magical)"
    }
```

Data files are a little less structured, as different kinds of data need to be stored differently. Just ensure to stick to the standard in the file you are working in.

## Making a Pull Request
Before you make a pull request. Run `confirm_library_integrity.py` in the root directory of this git repo. You want to see output like this:

```
No Errors found. Library has good integrity.
Size of library in memory: 99.7 KiB
```

If any errors are printed, fix them in the library. If it is not an error with the library, but rather with the script, open an Issue, and reference it in your PR.
