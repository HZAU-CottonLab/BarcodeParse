<!--
 * @Descripttion: 
 * @version: 
 * @Author: zpliu
 * @Date: 2021-07-15 21:41:28
 * @LastEditors: zpliu
 * @LastEditTime: 2021-07-15 22:29:11
 * @@param: 
-->
# BarcodeParse
Parsing the barcode sequences in CRISPR-Case9 system  using Next-generation sequencing


### paraments:

1. `-R1` R1 fastq sequence file (gizped or uncompressed)
2. `-R2` R2 fastq sequence file (gizped or uncompressed)
3. `-verctor5` verctor sequence adjacent to 5' barcode (default='TATAAGCGAAAGAAGCATCAGATGGGCAAACAAAGCACCAGTGGTCTAGTGGTAGAATAGTACCCTGCCACGGTACAGACCCGGGTTCGATTCCCGGCTGGTGCA')
4. `-verctor3` verctor sequence adjacent to 3' barcode (default='TAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTTTTAGCGCGTGCATGCCTGCAGGTCCACAAATTCGGGTC')
5. `-o` out put file

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
1. `barcodeID` unique barcode id 
2. `barcodesequence` barcode sequence
3. `barcodeCount` the number of barcode sequence been sequenced
4. `sgRNAsequence` sgRNA sequence
5. `sgRNACount` the number of sgRNA sequence  been sequenced

```bash
 #example 
 python barcode_parser.py -R1 testData/test_R1.fastq -R2 testData/test_R2.fastq -verctor5 GCGAAAGAAGCATCAGATGGGCAAACAAAGCACCAGTGGTCTAGTGGTAGAATAGTACCCTGCCACGGTACAGACCCGGGTTCGATTCCCGGCTGGTGCA -verctor3 GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTTTTAGCGCGTGCATGCCTGCAGGTCCACAAATTCGGGTC -o testData/sgRNA_count.txt
```
