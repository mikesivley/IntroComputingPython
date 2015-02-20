#!/usr/bin/env python2.7

# Import the modules we'll need
import csv,os,glob

# Define the file directory location
fdir = "../data"
# Define the mapping file location
fname = "%s/HGNC_to_Ensembl.txt"%fdir

# Define a function to load the file into a dictionary
def read_gene_dict(fname):
  with open(fname,'rb') as fin: # open for reading
    fin.readline() # discard the header
    reader = csv.reader(fin,delimiter='\t')
    gene_dict = dict((r[1],r[0]) for r in reader if r[1])
    return gene_dict

# Use the function to load the gene mapping dictionary
ens2hgnc = read_gene_dict(fname)

# Show the first 20 key,val pairs (items) in the dictionary
for key,val in ens2hgnc.items()[:20]:
  print "%s => %s"%(key,val)

## ======================================================= ##
# Generate example dataset
# One file per Ensembl gene, 50 rows per file
def generate_dataset(rdir,ens2hgnc):
  import random
  os.makedirs(rdir)
  for ens in ens2hgnc.keys()[:1000]: # limit to 1000 genes
    fname = "%s/%s.ens"%(rdir,ens)
    with open(fname,'wb') as fout: # open for writing
      writer = csv.writer(fout,delimiter='\t')
      rdata = [[ens]+random.sample(range(50),10) for i in xrange(50)]
      writer.writerows(rdata)
  os.system("cat %s/*.ens > %s/ens.all"%(rdir,rdir))
# Only generate the example data if it doesn't already exist
rdir = "%s/random"%fdir
if not os.path.exists(rdir):
  generate_dataset(rdir,ens2hgnc)
# From now on we'll pretend like these are real results
## ======================================================= ##

# Define the result directory location
# this was already defined, but we're pretending
rdir = "%s/random"%fdir
# To get all files in the directory, use the glob module
for in_fname in glob.glob("%s/*.ens"%rdir):
  path      = os.path.dirname(in_fname)
  ens,ext   = os.path.basename(in_fname).split('.')
  hgnc      = ens2hgnc[ens] # change the filename
  ext       = 'hgnc' # change the extension
  out_fname = "%s/%s.%s"%(path,hgnc,ext)
  with open(in_fname,'rb') as fin, open(out_fname,'wb') as fout:
    reader   = csv.reader(fin, delimiter='\t')
    writer   = csv.writer(fout,delimiter='\t')
    data = [row for row in reader]
    # Replace the Ensembl name with the HGNC name
    for row in data:
      # row[0] = ens2hgnc[row[0]]
      row[0] = hgnc
    # Question: was data changed? Why?
    # Write the modified data to the new file name
    writer.writerows(data)
    
# View an example
ens,hgnc = ens2hgnc.items()[0]

print "---"

with open("%s/%s.ens"%(rdir,ens)) as fin:
  print "%s/%s.ens"%(rdir,ens)
  for row in [line.split() for i,line in enumerate(fin) if i<10]:
    print row

print "---"

with open("%s/%s.hgnc"%(rdir,hgnc)) as fin:
  print "%s/%s.hgnc"%(rdir,hgnc)
  for row in [line.split() for i,line in enumerate(fin) if i<10]:
    print row