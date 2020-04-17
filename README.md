# find64
This tool parses files for base64 strings. Whitespaces, which are often used within base64 strings, are stripped during extraction
## Usage
`python3 find64.py [-h] [-n N] [-s S] [-c] file`

`file`        The file to parse for base64.  
`-h, --help`  Show this help message and exit.  
`-n N`        The minimum length for a base64 string to be returned. Default 16. Minimum 4.  
`-s S`        The special characters the base64 string consists of. Default '+/'.  
`-c`          Output results as CSV.

## Examples
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
```
Two base64 strings have been detected. The results contain their offsets in the file. If the base64 string contains whitespaces (regex `\s` = `[\r\n\t\f\v ]`) these are stripped. The number of stripped bytes is displayed. The provided shell command can be used to extract the unstripped string from the binary, e.g.
```
$ tail -c 2353 testfile | head -c 186
TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ci
wgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRv
bG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
```
Note, that the stripped bytes are contained here (two linefeeds).  
Further, the stripped data is displayed and can be easily copied and base64 decoded like so:
```
base64 -d <<< TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
```

For increased automation, the results can be returned as CSV.
```
$ python3 find64.py testfile -c
0,1767,1995,228,True,20,TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0LCBzZWQgZGlhbSB2b2x1cHR1YS4K
1,5006,5192,186,True,2,TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0Lgo=
```
The columns are defined as follows:
`#,start,end,length,stripped,bybytes,data`
