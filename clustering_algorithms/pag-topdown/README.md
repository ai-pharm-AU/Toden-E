# virtual_pags
Find New PAGS

## INSTALLATION

Use Python 2.7. Some dependencies may need to be installed. If required, CD to this directory and use:
`$ pip install -r requirements.txt`


## USAGE

```
usage: python topdown.py [-h] -i INPUT -o OUTPUT [-headers]

Run topdown method to identify new PAGs.

optional arguments:
  -h, --help  show this help message and exit
  -i INPUT    Filename for input. Must be a file with two columns in the
              following order: PAG_ID GENE_SYMBOL
  -o OUTPUT   Name for base of output files. Do not add extension, ex: 'output' not 'output.txt'
  -headers    If you use headers in your input file, specify that with this
              argument so it can be skipped
```

### INPUT

You can use any type of delimiter, but the input file must contain in the first column the PAG_ID and the second column must contain and HGNC Gene Symbol.

### OUTPUT

Two files are output as relational information.

scores_table = output+"_scores.tsv"

genes_table = output+"_genes.tsv"

scores_table contains PAG_ID,SIZE_CHOICE, and COCO_SCORE

genes_table maps the candidate size choice clusters for each pag to the genes they contain. This has PAG_ID,SIZE_CHOICE, and GENE.
  