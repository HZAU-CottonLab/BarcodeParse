<!--
 * @Descripttion: 
 * @version: 
 * @Author: zpliu
 * @Date: 2021-07-15 21:41:28
 * @LastEditors: zpliu
 * @LastEditTime: 2021-07-15 21:49:09
 * @@param: 
-->
# BarcodeParse
Parsing the barcode sequences in CRISPR-Case9 system  using Next-generation sequencing


### paraments:

    + `-R1` R1 fastq sequence file (gizped or uncompressed)
    + `-R2` R2 fastq sequence file (gizped or uncompressed)
    + `-verctor5` verctor sequence adjacent to 5' barcode (default='TATAAGCGAAAGAAGCATCAGATGGGCAAACAAAGCACCAGTGGTCTAGTGGTAGAATAGTACCCTGCCACGGTACAGACCCGGGTTCGATTCCCGGCTGGTGCA')
    + `-verctor3` verctor sequence adjacent to 3' barcode (default='TAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTTTTAGCGCGTGCATGCCTGCAGGTCCACAAATTCGGGTC')
    + `-o` out put file

```bash
    python barcode_parser.py -h 

usage: barcode_parser.py [-h] [-R1 R1] [-R2 R2] [-verctor5 VERCTOR5]
                         [-verctor3 VERCTOR3] [-o O]

optional arguments:
  -h, --help          show this help message and exit
  -R1 R1              R1 sequence file
  -R2 R2              R2 sequence file
  -verctor5 VERCTOR5  verctor sequence adjacent to 5' barcode
  -verctor3 VERCTOR3  verctor sequence adjacent to 3' barcode
  -o O                out put file
```
### header of output 
    + `barcodeID` unique barcode id 
    + `barcodesequence` barcode sequence
    + `barcodeCount` the number of barcode sequence been sequenced
    + `sgRNAsequence` sgRNA sequence
    + `sgRNACount` the number of sgRNA sequence  been sequenced
