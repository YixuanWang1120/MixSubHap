# MixSubHap
## A Graph-based Algorithm for Estimating Clonal Haplotypes of Tumor Sample from Sequencing Data

## Step1:simulation
#### #generating the second generation sequencing data, paired-end reads
      Usage:   norsim \[options] <ref.fa> <nor.sim>
      Options: -r FLOAT	mutation rate of GV (0.0010000000)
         -R FLOAT      	fraction of indels (0.000000)
         -X FLOAT      	probability an indel is extended (0.300000)
         -D FLOAT      	delete rate in indel (0.500000)
         -B FLOAT      	BB rate in mutation (0.333330)
         -I <delpos.txt>  	input long indel set file
         -A <nor_AB.idx>  	output the positions of AB mutation type in normal
         -o <nor_simout.txt>  	result for runing case
```
./norsim -r 0.001 -B 0 -A nor_AB.idx ref.fa nor.sim<br>
```
./tumsim -r 0.007  -A 0 -B 0 -n 7000 -p 0 -l 100000 ref.fa nor.sim nor_AB.idx s1.sim<br>
./tumsim -r 0.003  -A 0 -B 0 -n 3000 -p 0 -l 100000 ref.fa s1.sim nor_AB.idx s2.sim<br>

#### #three sub-clones 3:5:2
./readgen -l 250 -r 250 -d 1000 -s 10 -c 30 ref.fa nor.sim n30_left.fq n30_right.fq<br>
./readgen -l 250 -r 250 -d 1000 -s 10 -c 50 ref.fa s1.sim s1_left.fq s1_right.fq<br>
./readgen -l 250 -r 250 -d 1000 -s 10 -c 20 ref.fa s2.sim s2_left.fq s2_right.fq<br>
./merge chr16 n30_left.fq s1_left.fq s2_left.fq  t100_left.fq<br>
./merge chr16 n30_right.fq s1_right.fq s2_right.fq  t100_right.fq<br>
bwa index -a bwtsw ref.fa<br>
bwa aln ref.fa t100_left.fq>t100_left.sai<br>
bwa aln ref.fa t100_right.fq>t100_right.sai<br>
bwa sampe -f p1000-20.sam ref.fa t100_left.sai t100_right.sai t100_left.fq t100_right.fq<br>

## Step2:Dividing and Assembling

#### #extraing variants
./vpe 250 ref.fa s2.sim p1.sam 1.vaf VPE1<br>

#### #count the missing point
./mis s2.sim VPE1 1000 missp<br>

#### #map against reference
* VPEapart.py
    * input:    VPE
    * output:   apart file
* mapAB.py            
    * input:    .xlsx (process apart file to excel file) and ref.xlsx (turn ref.fa to excel file)
    * output:   VPE_variants_AB (merge them to VPEAB.txt)

#### #connecting short chain groups
./hap s2.sim VPE1AB.txt 1000 VPE2AB.txt 1500 VPE3AB.txt 2000 short_chain<br>

## Step3:Generating the Maximum Spanning Tree and Thickness Stripping

#### #clustering by SciClone tool
./sc cluster.txt siclus<br>

#### #caculate the weighted matrix for the undirected graph
* weight_matrix.py      
    * input: 
         * positionAB.xlsx  (apart short_chain into positionAB and variantsAB)
         * variantsAB.xlsx  (apart short_chain into positionAB and variantsAB)
         * cluster.xlsx (turn siclus into excel file)
    * output:
        * w.mat (weighted matrix)
        * w0.mat    (weighted matrix for the founding clone variants)
        * ww.mat    (weighted matrix after thickness stripping)

#### #remove the row and column with all zeros
#### #generating the spanning tree
* max_spanning_tree.py  
    * input:
        * ww_nonezero.mat
        * aww.mat
    * output:   chainAB.txt                      
#### #generating the real clusters and haplotype chain
./rc s2.sim s1.sim nor.sim reclus rchain<br>
* rechainmapped.py      
    * input:    rchain.xlsx
    * output:   rechainAB.txt

#### check
./ck reclus rechainAB.txt chainAB.txt<br>
