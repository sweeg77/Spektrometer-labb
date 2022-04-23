#Adam Biskop
import numpy as np

experiment_data = np.array([438,491,556,578,602,655])
element_dictionary = {'Aluminium':np.array([394,396]),
                    'Argon':np.array([404,415,420,750,801,811]),
                    'Barium':np.array([455,493,553,577,614,649,659]),
                    'Bly':np.array([368,405]),
                    'Cesium':np.array([455,459,672]),
                    'Helium':np.array([389,447,471,501,587,668,706]),
                    'Järn':np.array([371,373,385,427,430,432,438,440,495,516,526]),
                    'Kadmium':np.array([346,361,467,479,508,643]),
                    'Kalcium':np.array([393,396,422,445,616,643]),
                    'Kobolt':np.array([345]),
                    'Koppar':np.array([406,465,510,515,521,529,570,578]),
                    'Krom':np.array([357,359,360,425,427,428,520]),
                    'Krypton':np.array([427,431,437,446,450,557,587,760,810]),
                    'Kvicksilver':np.array([365,365,366,404,434,436,546,577,579]),
                    'Kväve':np.array([409,410,484,566,567,742,744,746]),
                    'Litium':np.array([460,610,670]),
                    'Magnesium':np.array([383,384,517,518]),
                    'Molybden':np.array([379,386,390,550,553]),
                    'Neon':np.array([470,471,540,585,618,626,640,650]),
                    'Nickel':np.array([341]),
                    'Niob':np.array([405,407]),
                    'Silver':np.array([521,546]),
                    'Strontium':np.array([407,421,460,640]),
                    'Syre':np.array([436,615,616,616,645,700,725,777,777,77]),
                    'Talium':np.array([535]),
                    'Väte':np.array([383,388,397,410,434,486,656]),
                    'Zink':np.array([468,472,481,636]),}

#tar in en bool array och ger tillbaka en array med indexen för True värden setLength är antal True värden( används i SetGen())
def PoniterArr2SetArr(pointerarr,setlength):
    index_start = -1
    set_array = np.zeros(setlength,dtype=int)
    length = len(pointerarr)
    for i in range(setlength):
        for j in range(index_start+1,length):
            if pointerarr[j]:
                index_start = j
                set_array[i] = j
                break
    return set_array

#generator som ger alla delmängder med n element från en mängd med length element (i form av indexer)
def SetGen(length,n):
    pointer_array = np.concatenate((np.ones(n,dtype=bool),np.zeros(length-n,dtype=bool)))
    set_array = np.array([i for i in range(n)])
    finished = False
    while not finished:
        yield set_array
        first_pointer = True
        for p in range(length-1,-1,-1):
            if pointer_array[p] and p == length -1:
                first_pointer = False
                numahead = 1
            elif first_pointer and pointer_array[p]:
                pointer_array[p+1] = True
                pointer_array[p] = False
                set_array = PoniterArr2SetArr(pointer_array, n)
                break
            elif not first_pointer and pointer_array[p] and not pointer_array[p+1]:
               pointer_array[p:] = False
               pointer_array[p+1:p+2+numahead] = True
               set_array = PoniterArr2SetArr(pointer_array,n)
               break
            elif not first_pointer and pointer_array[p]:
                numahead += 1
            elif p==0:
                finished = True

#Ger hur bra ett ämne passar experimentdatan           
def Evaluate_Element(element,data):
    if len(element) > len(data):
        best_match = [0,1,2,3,4,5]
        best_score = sum([(element[i]-j)**2 for i,j in zip(best_match,data)])
        for wave_lengths in SetGen(len(element),6):
           wave_lengths = np.array([element[i] for i in wave_lengths])
           score = sum(abs(wave_lengths-data))  
           if score < best_score:
               best_match = wave_lengths
               best_score = score
        return [best_score/len(data),best_match]
    elif len(element) == len(data):
        return [sum(abs(element-data))/len(data), element]
    else:
        best_score = 100000000000
        best_match = [i for i in range(len(element))]
        for wave_lengths in SetGen(len(data),len(element)):
            wave_lengths = np.array([data[i] for i in wave_lengths])
            score = sum(abs(wave_lengths-element))
            if score < best_score:
               best_match = wave_lengths
               best_score = score
        return [best_score/len(element),best_match]

#skriver ut hur bra varje ämne passar experimentdatan
if __name__ == "__main__":
    x = [[name,round(Evaluate_Element(element, experiment_data)[0])]  for name,element in element_dictionary.items()]
    x = sorted(x, key=lambda x: x[1])
    print(x)
