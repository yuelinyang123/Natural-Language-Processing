
# coding: utf-8

# In[6]:


from collections import Counter
import math
import sys
def readfile(filename):
    label=[]
    red_counter=Counter()
    blue_counter=Counter()
    total_word=[]
    with open(filename) as f:
        lines=f.readlines()
        for line in lines:
            onerow=line.split()
            label.append(onerow[0])
            for i in range(len(onerow)-1):
                total_word.append(onerow[i+1])
            if(onerow[0]=='RED'):
                for i in range(len(onerow)-1):
                    red_counter[onerow[i+1]]+=1
                    blue_counter[onerow[i+1]]+=0
            else:
                for i in range(len(onerow)-1):
                    blue_counter[onerow[i+1]]+=1
                    red_counter[onerow[i+1]]+=0
    vac_size=len(set(total_word))
    return label, red_counter, blue_counter, vac_size


# In[7]:


def smooth(counter):
    vac_size=0
    for key, value in counter.items():
        counter[key]=value+1
        vac_size+=value
    return counter, vac_size


# In[8]:


def getlabel(word_list, red_counter, blue_counter,red_vac_size,blue_vac_size,labels,vac_size):
    red_class_size=0
    # initial red prob
    for label in labels:
        if(label=='RED'):
            red_class_size+=1
    
    
    red_prob=math.log(red_class_size/len(labels))*len(word_list)
    ## intial blue prob
    blue_prob=math.log(1-(red_class_size/len(labels)))*len(word_list)
    for i in word_list:
        if(red_counter[i]!=0):
            red_prob+=math.log(red_counter[i]/(red_vac_size+vac_size))
        else:
             red_prob+=math.log(red_counter['UNKNOWNWORD']/(red_vac_size+vac_size))
        if(blue_counter[i]!=0):
            blue_prob+=math.log(blue_counter[i]/(blue_vac_size+vac_size))
        else:
            blue_prob+=math.log(blue_counter['UNKNOWNWORD']/(blue_vac_size+vac_size))
    if red_prob>=blue_prob:
        return 'RED'
    else:
        return 'BLUE'
    
    
    
    
    
    
    


# In[9]:


def main (train,test,train2,test2):
    ### part one test the first train datasets
    labels, red_counter, blue_counter,vac_size=readfile(train)
    red_counter, red_vac_size=smooth(red_counter)
    blue_counter, blue_vac_size=smooth(blue_counter)
    true_label=[]
    pred_label=[]
    with open (test) as f:
        lines=f.readlines()
        for line in lines:
            onerow=line.split()
            true_label.append(onerow[0])
            pred_label.append(getlabel(onerow[1:],red_counter,blue_counter,red_vac_size,blue_vac_size,labels,vac_size))
            
    labels_2, red_counter_2, blue_counter_2,vac_size_2=readfile(train2)
    red_counter_2, red_vac_size_2=smooth(red_counter_2)
    blue_counter_2, blue_vac_size_2=smooth(blue_counter_2)
    true_label_2=[]
    pred_label_2=[]
    with open (test2) as f:
        lines=f.readlines()
        for line in lines:
            onerow=line.split()
            true_label_2.append(onerow[0])
            pred_label_2.append(getlabel(onerow[1:],red_counter_2,blue_counter_2,red_vac_size_2,blue_vac_size_2,labels_2,vac_size_2))
    ### evaluation         
  
    true_red_pre_red=0
    true_red_pre_blue=0
    true_blue_pre_blue=0
    true_blue_pre_red=0
    for index in range(len(true_label)):
        if(true_label[index]=='RED' and pred_label[index]=='RED'):
             true_red_pre_red+=1
        elif(true_label[index]=='RED' and pred_label[index]=='BLUE'):
             true_red_pre_blue+=1
        elif(true_label[index]=='BLUE' and pred_label[index]=='BLUE'):
             true_blue_pre_blue+=1
        else:
             true_blue_pre_red+=1
                
            
    accuracy=(true_red_pre_red+true_blue_pre_blue)/(true_red_pre_red+true_red_pre_blue+true_blue_pre_blue+true_blue_pre_red)
    red_precision=true_red_pre_red/(true_red_pre_red+true_blue_pre_red)
    red_recall=true_red_pre_red/(true_red_pre_red+true_red_pre_blue)
    blue_precision= true_blue_pre_blue/(true_red_pre_blue+true_blue_pre_blue) 
    blue_recall=true_blue_pre_blue/(true_blue_pre_blue+true_blue_pre_red)
            
    true_red_pre_red_2=0
    true_red_pre_blue_2=0
    true_blue_pre_blue_2=0
    true_blue_pre_red_2=0
    for index in range(len(true_label_2)):
        if(true_label_2[index]=='RED' and pred_label_2[index]=='RED'):
             true_red_pre_red_2+=1
        elif(true_label_2[index]=='RED' and pred_label_2[index]=='BLUE'):
             true_red_pre_blue_2+=1
        elif(true_label_2[index]=='BLUE' and pred_label_2[index]=='BLUE'):
             true_blue_pre_blue_2+=1
        else:
             true_blue_pre_red_2+=1
                
    
    accuracy_2=(true_red_pre_red_2+true_blue_pre_blue_2)/(true_red_pre_red_2+true_red_pre_blue_2+true_blue_pre_blue_2+true_blue_pre_red_2)
    red_precision_2=true_red_pre_red_2/(true_red_pre_red_2+true_blue_pre_red_2)
    red_recall_2=true_red_pre_red_2/(true_red_pre_red_2+true_red_pre_blue_2)
    blue_precision_2= true_blue_pre_blue_2/(true_red_pre_blue_2+true_blue_pre_blue_2) 
    blue_recall_2=true_blue_pre_blue_2/(true_blue_pre_blue_2+true_blue_pre_red_2)
    writefile=open('task1.txt','w')
    writefile.write('overall accuracy')
    writefile.write('\n')
    writefile.write(str(round(accuracy,1)))
    writefile.write('\n')
    writefile.write('precision for red')
    writefile.write('\n')
    writefile.write(str(round(red_precision,1)))
    writefile.write('\n')
    writefile.write('Recall for red')
    writefile.write('\n')
    writefile.write(str(round(red_recall,1)))
    writefile.write('\n')
    writefile.write('precision for blue')
    writefile.write('\n')
    writefile.write(str(round(blue_precision,1)))
    writefile.write('\n')
    writefile.write('recall for blue')
    writefile.write('\n')
    writefile.write(str(round(blue_recall,1)))
    writefile.write('\n')
    writefile.write('\n')
    writefile.write('overall accuracy')
    writefile.write('\n')
    writefile.write(str(round(accuracy_2,1)))
    writefile.write('\n')
    writefile.write('precision for red')
    writefile.write('\n')
    writefile.write(str(round(red_precision_2,1)))
    writefile.write('\n')
    writefile.write('recall for red')
    writefile.write('\n')
    writefile.write(str(round(red_recall_2,1)))
    writefile.write('\n')
    writefile.write('precision for blue')
    writefile.write('\n')
    writefile.write(str(round(blue_precision_2,1)))
    writefile.write('\n')
    writefile.write('recall for blue')
    writefile.write('\n')
    writefile.write(str(round(blue_recall_2,1)))
    writefile.write('\n')

    
    
    
    
    
    
    
    

    
    
    


# In[10]:


if __name__ == '__main__':
    a=sys.argv[1]
    b=sys.argv[2]
    c=sys.argv[3]
    d=sys.argv[4]
    main(a,b,c,d)
        


# In[ ]:




