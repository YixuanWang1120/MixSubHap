# MixSubHap
## A Graph-based Algorithm for Estimating Clonal Haplotypes of Tumor Sample from Sequencing Data

## Step1:simulation
#### #Generating the second generation sequencing data, paired-end reads.
**1.  NorSim**<br>

      Usage:   norsim [options] <ref.fa> <nor.sim>
      Options: -r FLOAT	mutation rate of GV (0.0010000000)
               -R FLOAT      	fraction of indels (0.000000)
               -X FLOAT      	probability an indel is extended (0.300000)
               -D FLOAT      	delete rate in indel (0.500000)
               -B FLOAT      	BB rate in mutation (0.333330)
               -I <delpos.txt>  	input long indel set file
               -A <nor_AB.idx>  	output the positions of AB mutation type in normal
               -o <nor_simout.txt>  	result for runing case
```
./norsim -r 0.001 -B 0 -A nor_AB.idx ref.fa nor.sim
```
**2.  TumSim**<br>

      Usage:   tumsim [options] <ref.fa> <base.sim> <nor_AB.idx> <subclone.sim>
      Options: -r FLOAT      	mutation rate of SV (0.0000100000)
               -R FLOAT      	fraction of indels (0.000000)
               -X FLOAT      	probability an indel is extended (0.300000)
               -D FLOAT      	delete rate in indel (0.500000)
               -B FLOAT      	BB rate in mutation (0.333330)
               -b FLOAT      	LOH BB rate in mutation (0.500000)
               -A FLOAT      	mutation rate of LOH in normal AB (0.0000100000)
               -p FLOAT      	the position of high desity (0.500000)
               -n int      	mutation number in high desity (100)
               -l int       	length of high desity (100000)
               -I <indelpos.txt>  		input long indel set file. generating <subclone.sim.idx> for 'ReadGen'
               -N <other_chged.idx> 	input changed positions in other subclone(may multi-choices)
               -C <*_chged.idx>  		output changed positions in this turmor
               -o <*_simout.txt>  	output result for runing case
```
./tumsim -r 0.007  -A 0 -B 0 -n 7000 -p 0 -l 100000 ref.fa nor.sim nor_AB.idx s1.sim
./tumsim -r 0.003  -A 0 -B 0 -n 3000 -p 0 -l 100000 ref.fa s1.sim nor_AB.idx s2.sim
```

#### #The ratio of three sub-clones is 3:5:2.
**3.  ReadGen**<br>

      Usage:   readgen [options] <ref.fa> <*.sim> <left.fq> <right.fq>
      Options: -d INT		outer distance between the two ends of paired_end reads [10000]
               -s INT     standard deviation of MAX_DIS [10]
               -l INT     length of left  read [100]
               -r INT     length of right read [100]
               -c float   cover rate of read [5.000000]
               -e float   error r  ate in generate reads [0.000000]
               -S       	output single read(not paired_end reads)
               -k       	keep 'N' character in reads
               -I <subclonde.sim.idx>   long insert table file from 'TumSim'
               -O <genread.log>  		  result for runing case
```
./readgen -l 250 -r 250 -d 1000 -s 10 -c 30 ref.fa nor.sim n30_left.fq n30_right.fq
./readgen -l 250 -r 250 -d 1000 -s 10 -c 50 ref.fa s1.sim s1_left.fq s1_right.fq
./readgen -l 250 -r 250 -d 1000 -s 10 -c 20 ref.fa s2.sim s2_left.fq s2_right.fq
```
**4. Merge**<br>

      Usage:   merge  ref_name  *1.fq ... *n.fq   all.fq
```
./merge chr16 n30_left.fq s1_left.fq s2_left.fq  t100_left.fq
./merge chr16 n30_right.fq s1_right.fq s2_right.fq  t100_right.fq
```
**5. BWA**<br>
```
bwa index -a bwtsw ref.fa
bwa aln ref.fa t100_left.fq>t100_left.sai
bwa aln ref.fa t100_right.fq>t100_right.sai
bwa sampe -f p1.sam ref.fa t100_left.sai t100_right.sai t100_left.fq t100_right.fq
```
## Step2:Dividing and Assembling

#### #Extraing variants as VPE information.
**6. VPE**<br>

      Usage:   vpe readlength ref.fa vpoint.sim in.sam out.vaf VPEname
```
./vpe 250 ref.fa s2.sim p1.sam 1.vaf VPE1
```
#### #Counting the missing point.
**7. Misspoint**<br>

      Usage:   misspoint vpoint.sim VPEname1 insertsize1 VPEname2 insertsize2 outname   
```
./misspoint s2.sim VPE1 1000 VPE2 1500 missp
```
#### #Mapping against the reference.
**8.  VPEapart.py**<br>
      
      Usage: input:    VPE
             output:   apart file
**9.  mapAB.py**<br>

      Usage: input:    .xlsx (process apart file to excel file) and ref.xlsx (turn ref.fa to excel file)
             output:   VPE_variants_AB (merge them to VPEAB.txt)


#### #Clustering by SciClone tool.
**10. SciClone**<br>
[https://github.com/genome/sciclone]

**11. Sci-cluster**<br>

      Usage:   sc cluster.txt cluster 
```
./sc cluster.txt siclus
```
#### #Connecting short chain groups.
**12. Haplotype**<br>

      Usage:   haplotype vpoint.sim cluster VPEname1 insertsize1 VPEname2 insertsize2 VPEname2 insertsize3 out
```
./haplotype s2.sim siclus VPE1AB.txt 1000 VPE2AB.txt 1500 VPE3AB.txt 2000 short_chain
```
## Step3:Generating the Maximum Spanning Tree and Thickness Stripping
#### #Caculating the weighted matrix for the undirected graph.
**13. weight_matrix.py**<br>

      Usage: input: 
               positionAB.xlsx  (apart short_chain into positionAB and variantsAB)
               variantsAB.xlsx  (apart short_chain into positionAB and variantsAB)
               cluster.xlsx (turn siclus into excel file)
             output:
               w.mat (weighted matrix)
               w0.mat    (weighted matrix for the founding clone variants)
               ww.mat    (weighted matrix after thickness stripping)

#### #Removing the row and column with all zeros.
**14. none_zero.m**<br>

      Usage: input: w0.mat and ww.mat
             output: w0_nonezero.mat and a0.mat
                     ww_nonezero.mat and aww.mat
#### #Generating the spanning tree.
**15. max_spanning_tree.py**<br>

      Usage: input:
               ww_nonezero.mat
               aww.mat
             output: chainAB.txt         
             
#### #Generating the real clusters and haplotype chain.
**16. Re-cluster**<br>

      Usage:   rc vpoint1.sim vpoint2.sim vpoint3.sim realcluster realchain
```./rc s2.sim s1.sim nor.sim reclus rchain
```
**17. rechainmapped.py**

      Usage: input:    rchain.xlsx
             output:   rechainAB.txt

#### Checking
**18. Check**<br>

      Usage:check realcluster realchain chain
```
./ck reclus rechainAB.txt chainAB.txt
```
