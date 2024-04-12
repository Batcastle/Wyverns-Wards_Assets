# Contributing to the Library

All files in the library are in JSON format, unless they are in the __media__ folder. In which case, the following file formats are used for the following data:

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
