import sys
import re

from collections import defaultdict

# Files
TAG_FILE = sys.argv[1]
TOKEN_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]

# Vocabulary
vocab = {}
OOV_WORD = "OOV"
INIT_STATE = "init"
FINAL_STATE = "final"

# Transition and emission probabilities
emissions = {}
transitions = {}
transitions_binary = {}
emissions_total = defaultdict(lambda: 0)

tag_set=set()
word_set=set()
tag_binary=set()
transition_total=defaultdict(lambda: 0)
with open(TAG_FILE) as tag_file, open(TOKEN_FILE) as token_file:
    for tag_string, token_string in zip(tag_file, token_file):
        
        tags = re.split("\s+", tag_string.rstrip())
        tokens = re.split("\s+", token_string.rstrip())
    
         


        for index in range(len(tags)):

            # this block is a little trick to help with out-of-vocabulary (OOV)
            # words.  the first time we see *any* word token, we pretend it
            # is an OOV.  this lets our model decide the rate at which new
            # words of each POS-type should be expected (e.g., high for nouns,
            # low for determiners).
            token=tokens[index]
            tag=tags[index]
           
            if(index!=len(tags)-1):
                tag_next=tags[index+1]
            else:
                tag_next=FINAL_STATE
                
            if(index==0):
                prevtag=INIT_STATE
                
            else:
                prevtag=tags[index-1]
            if token not in vocab:
                vocab[token] = 1
                token = OOV_WORD

            if tag not in emissions:
                emissions[tag] = defaultdict(lambda: 0)
            if prevtag not in transitions:
              
    
                
                
                transitions[prevtag] = defaultdict(lambda: defaultdict(lambda: 0))
                transitions_binary[prevtag]=defaultdict(lambda: 0)
            # increment the emission/transition observation
            emissions[tag][token] += 1
            emissions_total[tag] += 1
            
    
            transitions[prevtag][tag][tag_next] += 1
            transitions_binary[prevtag][tag] += 1
            transition_total[prevtag]+=1
            tag_set.add((prevtag,tag))
            word_set.add(token)
            tag_binary.add(tag)
        # don't forget the stop probability for each sentence
    

# Write output to output_file
with open(OUTPUT_FILE, "w") as f:
    for prevtag in transitions:
        
        for tag in transitions_binary[prevtag]:
            
            f.write("Firstword {} {} {}\n".format(prevtag,tag,(transitions_binary[prevtag][tag])/(transition_total[prevtag])))
    
    for prevtag in transitions:
        
      
        for tag in transitions[prevtag]:
            
            for tagnext in transitions[prevtag][tag]:
                  f.write("trans {} {} {} {}\n"
                .format(prevtag, tag,tagnext,(transitions[prevtag][tag][tagnext]+1)/ (transitions_binary[prevtag][tag]+len(tag_set))))
           

    for tag in emissions:
        for token in emissions[tag]:
            f.write("emit {} {} {}\n"
                .format(tag, token, (emissions[tag][token])/ (emissions_total[tag])))
                
