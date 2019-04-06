mport math
import sys
import time
import multiprocessing as mp

from collections import defaultdict

# Magic strings and numbers
NUM_PROCESSES = mp.cpu_count()     # Uses all cores available
PROCESSOR_RATIO = 2
HMM_FILE = sys.argv[1]
TEXT_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]
TRANSITION_TAG = "trans"
EMISSION_TAG = "emit"
Firstword_TAG="Firstword"
OOV_WORD = "OOV"         # check that the HMM file uses this same string
INIT_STATE = "init"      # check that the HMM file uses this same string
FINAL_STATE = "final"    # check that the HMM file uses this same string

# Transition and emission probabilities
# Structured as a nested defaultdict in defaultdict, with inner defaultdict
#   returning 0.0 as a default value, since dirty KeyErrors are equivalent to
#   zero probabilities
#
# The advantage of this is that one can add redundant transition probabilities
transition = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -10)))
emission = defaultdict(lambda: defaultdict(lambda: -10))
initials=defaultdict(lambda: 0.0)
# Store states to iterate over for HMM
# Store vocab to check for OOV words
states = set()
vocab = set()


# Actual Viterbi function that takes a list of lines of text as input
# The original version (and most versions) take in a single line of text.
# This is to reduce process creation/tear-down overhead by allowing us
#   to chunk up the input and divide it amongst the processes without
#   resource sharing
# NOTE: the state and vocab sets are still shared but it does not seem
#       to impact performance by much
def viterbi(lines):

    ret = [""] * len(lines)
    for (index, line) in enumerate(lines):
        
        
        w = line.split()
        
        # Setup Viterbi for this sentence:
        # V[x][y] where x is the index of the word in the line
        #   and y is a state in the set of states
        V = defaultdict(lambda: defaultdict(lambda:{}))
        
        # Initialize backtrace so we get recover the path:
        # back[x][y] where x is the index of the word in the line
        #   and y is the previous state with the highest probability
        back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:"")))
        
        # Initialize V with init state
        # REDUNDANT
        K={}
        K[-1]=({'*'})
        K[0]=({'*'})
        for k in range(len(w)):
            K[k+1]=states
        
            
        V[0]['*']['*'] = 0.0
         
        # Iterate over each word in the line
        for k in [i+1 for i in range(len(w))]:
          
            # If word not in vocab, replace with OOV word
            if w[k-1] not in vocab:
                w[k-1] = OOV_WORD

            # Iterate over all possible current states:
            for u in K[k-1]:
                #print(K[k-1])
                
                for v in K[k]:
                    
                    #print(len(K[k]))
                    emission_prob = emission[v][w[k-1]]
                    if emission_prob >= 0.0:
                        continue
               
                   
                    for j in K[k-2]:
                        #print(j,u,v,transition[j][u][v])
                        if(transition[j][u][v]==0.0):
                            continue
                        #print(k-1,j,u,v)
                       # print(V)
                        #print(V[k-1][j][u])
                        #print(transition[j][u][v])
                        try:
                            value = V[k-1][j][u] + transition[j][u][v]+emission_prob
                        except KeyError as e:
                            continue
                    # Replace if probability is higher
                    
                        if  ((V[k][u].get(v) is None) or (value>V[k][u][v])):
                            V[k][u][v] = value
                           
                            back[k][u][v] = j
                       
              
       
        
           
        value_int=-10000000 
        y_last=''
        y_last_two=''
        y_list=[]
       
        for u in K[len(w)-2]:
                for v in K[len(w)-1]:
                   # print(u,v)
                    if (transition[u][v][FINAL_STATE]>=0.0):
                        continue
                    try:
                        
                        value_new=V[len(w)][u][v]+transition[u][v][FINAL_STATE]
                    except KeyError as e:
                        continue
               
                    if(value_new>value_int):
                        value_int=value
                        y_last=v
                        y_last_two=u
        y_list.append(y_last)
        y_list.append(y_last_two)
        for k in range(len(w)-2):
            y=back[len(w)-k][y_list[k+1]][y_list[k]]
            y_list.append(y)      
                    
          
    # Return a list of processed lines
        ret[index] = " ".join(y_list[::-1])
    return ret


# Chunk a list l into n sublists
def chunks(l, n):
    chunk_size = len(l) // n
    return [[l[i:i + chunk_size]] for i in range(0, len(l), chunk_size)]


# Main method
def main():

    # Mark start time
    t0 = time.time()

    # Read HMM transition and emission probabilities
    with open(HMM_FILE, "r") as f:
        for line in f:
            line = line.split()

            # Read transition
            # Example line: trans NN NNPS 9.026968067100463e-05
            # Read in states as qq -> q
            if line[0] == TRANSITION_TAG:
                (qqq, qq,q, trans_prob) = line[1:5]
                transition[qqq][qq][q] = math.log(float(trans_prob))
                states.add(qqq)
                states.add(qq)
                states.add(q)

            # Read in states as q -> w
            elif line[0] == EMISSION_TAG:
                (q, w, emit_prob) = line[1:4]
                emission[q][w] = math.log(float(emit_prob))
                states.add(q)
                vocab.add(w)
            elif line[0]==Firstword_TAG:
                (qq,q, prob) = line[1:4]
                if(float(prob)!=0):
                    if(qq=='init'):
                        transition['*']['*'][q]=math.log(float(prob))
                    else:
                        transition['*'][qq][q]=math.log(float(prob))
            # Ignores all other lines

    # Read lines from text file and then split by number of processes
    text_file_lines = []
    with open(TEXT_FILE, "r") as f:
        text_file_lines = f.readlines()

    # If too few lines of text, run on single process
     
         
    results = viterbi(text_file_lines)
    print(results)
    # Otherwise divide workload amongst process threads

    # Print output to file
    with open(OUTPUT_FILE, 'w') as f:
        for line in results:
            f.write(line)
             
            f.write('\n')

    # Mark end time
    t1 = time.time()

    # Print info to stdout
    print("Processed {} lines".format(len(text_file_lines)))
    print("Time taken to run: {}".format(t1 - t0))

if __name__ == "__main__":    
    main()


