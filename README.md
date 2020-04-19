# find64
This tool parses files for base64 strings. Whitespaces, which are often used within base64 strings, are stripped during extraction
## Usage
`python3 find64.py [-h] [-n N] [-s S] [-d] [-c] file`

* `file`        The file to parse for base64.  
* `-h, --help`  Show this help message and exit.  
* `-n N`        The minimum length for a base64 string to be returned. Default 16. Minimum 4.  
* `-s S`        The special characters the base64 string consists of. Default `+/`. Urlsafe `-_`. Order matters.  
* `-d [D]`      Decode the detected base64 string. The optional parameter `D` specifies from which offsets the decoding starts.
* `-c`          Output results as CSV.

## Examples
### Basics
You can use the test file provided in this repository for exploration.
```
$ python3 find64.py testfile
  __ _           _  ____    ___
 / _(_)         | |/ ___|  /   |
| |_ _ _ __   __| / /___  / /| |
|  _| | '_ \ / _` | ___ \/ /_| |
| | | | | | | (_| | \_/ |\___  |
|_| |_|_| |_|\__,_\_____/    |_/  https://github.com/KwnyPwny/find64

Match #0:
  Start: 1767  End: 1995  Length: 228
  Stripped: True (by 20 bytes)
  Shell command: tail -c 5592 testfile | head -c 228
  Stripped Data: TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0LCBzZWQgZGlhbSB2b2x1cHR1YS4K

Match #1:
  Start: 5006  End: 5192  Length: 186
  Stripped: True (by 2 bytes)
  Shell command: tail -c 2353 testfile | head -c 186
  Stripped Data: TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=

Match #2:
  Start: 7014  End: 7039  Length: 25
  Stripped: False
  Shell command: tail -c 345 testfile | head -c 25
  Stripped Data: CSVGhpcyB3YXMgdHJpY2t5IQo
```
Three base64 strings have been detected. The results contain their offsets in the file. If the base64 string contains whitespaces (regex `\s` = `[\r\n\t\f\v ]`) these are stripped. The number of stripped bytes is displayed. The provided shell command can be used to extract the unstripped string from the binary, e.g.
```
$ tail -c 2353 testfile | head -c 186
TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ci
wgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRv
bG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
```
Note that the stripped bytes are contained here (two linefeeds).  
Further, the stripped data is displayed and can be easily copied and base64 decoded like so:
```
$ base64 -d <<< TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
```
### CSV Output
For increased automation, the results can be returned as CSV.
```
$ python3 find64.py testfile -c
0,1767,1995,228,True,20,TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0LCBzZWQgZGlhbSB2b2x1cHR1YS4K
1,5006,5192,186,True,2,TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
2,7014,7039,25,False,0,CSVGhpcyB3YXMgdHJpY2t5IQo
```
The columns are defined as follows:
`#,start,end,length,stripped,bybytes,data`
* `#` Increasing counter for detected base64 strings, starting at 0.
* `start` The offset where the base64 string starts.
* `end` The offset where the base64 string ends.
* `length` The length of the unstripped base64 string (`end` - `start`).
* `stripped` Boolean value if the base64 string was stripped, i.e. if whitespaces were removed.
* `bybytes` The number of bytes that have been stripped.
* `data` The stripped base64 string.

### Decode Flag
You might have recognized that decoding match #2 only yields gibberish.
```
$ base64 -d <<< CSVGhpcyB3YXMgdHJpY2t5IQo
	%F??2v2G&?6??
```
Of course, it is always possible that files contain strings that look like but in fact are no base64 strings. However, this is not the case here. Let's use the decode flag `-d` to see what is going on:
```
$ python3 find64.py testfile -d          

[...]

Match #2:
  Start: 7014  End: 7039  Length: 25
  Stripped: False
  Shell command: tail -c 345 testfile | head -c 25
  Stripped Data: CSVGhpcyB3YXMgdHJpY2t5IQo
  Decoded Data:
    [0:24]: b'\t%F\x86\x972\x07v\x172\x07G&\x966\xb7\x92\x10'
    [1:25]: b'IQ\xa1\xa5\xcc\x81\xdd\x85\xcc\x81\xd1\xc9\xa5\x8d\xad\xe4\x84('
    [2:22]: b'This was tricky'
    [3:23]: b'\x1a\x1a\\\xc8\x1d\xd8\\\xc8\x1d\x1c\x9aX\xda\xdeH'
```
In addition to the default output, four lines of decoded data have been printed. In this case, the line prefixed with `[2:22]` contains the correct decoding. The section about **surrounded base64 strings** explains this in more detail.

If you are only interested in decodings with certain offsets, you can provide the decode flag with parameters:
```
$ python3 find64.py testfile -d2          

[...]

Match #2:
  Start: 7014  End: 7039  Length: 25
  Stripped: False
  Shell command: tail -c 345 testfile | head -c 25
  Stripped Data: CSVGhpcyB3YXMgdHJpY2t5IQo
  Decoded Data:
    [2:22]: b'This was tricky'
```
## Surrounded Base64 Strings
The base64 representation of the string `This was tricky` is `VGhpcyB3YXMgdHJpY2t5`. Unfortunately, in the test file the base64 string is surrounded by the characters `CS` and `IQo`. Since these also belong to the base64 charset, find64 returns the entire string `CSVGhpcyB3YXMgdHJpY2t5IQo` as result. find64 tackles this problem by decoding base64 strings from four positions:  

0. Character 0 to 24:

        CSVGhpcyB3YXMgdHJpY2t5IQo
        ^----------------------^

1. Character 1 to 25:

        CSVGhpcyB3YXMgdHJpY2t5IQo
         ^----------------------^

2. Character 2 to 22:

        CSVGhpcyB3YXMgdHJpY2t5IQo
          ^------------------^

3. Character 3 to 23:

        CSVGhpcyB3YXMgdHJpY2t5IQo
           ^------------------^

The length of the string to be decoded is determined as the largest multiple of four that does not exceed the string's end.
Note that the correct decoding even is detected if the base64 string is preceded by four or more characters.
