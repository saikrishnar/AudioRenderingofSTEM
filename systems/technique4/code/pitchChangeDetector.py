# usr/bin/python

def averagepitch_calc(y):   

    s=0                             # Filter out the unvoiced regions
    length=len(y)    
    for i in range(0,length):
        val=y[i]
        if val[0] == '-':
            y[i] = '0'

    count =0                         # Calculate the average only on the voiced regions
    for i in range(0,length):
      
      if y[i] != '0':
        s+=float(y[i])
        count+=1
      else:
         pass
    
    average_pitch=float(s/count)
    print average_pitch
    return average_pitch





def deviation_calc(array,mean):
    darray=[]
    length = len(array)
    for i in range(0, length):
        val= float(array[i])
        if val > 1.15* mean and val< 2*mean:
            darray.append(i)
    return get_sub_list(darray)
    #print darray
    #return darray



def split_list(n):
    """will return the list index"""
    return [(x+1) for x,y in zip(n, n[1:]) if y-x != 1]

def get_sub_list(my_list):
    """will split the list base on the index"""
    my_index = split_list(my_list)
    output = list()
    prev = 0
    for index in my_index:
        new_list = [ x for x in my_list[prev:] if x < index]
        output.append(new_list)
        prev += len(new_list)
    output.append([ x for x in my_list[prev:]])
    return output




def time_deviation_single(f,array):
    tarray=[]
    for i in f:
        tarray.append(array[i])           # When there is an array of elements ( not array of list)
   
    return tarray    





    
def time_deviation(f,array):
    tarray=[]
    for list in f:
        if len(list)>1:
            tarray.append(list[0])         # When there is an array of lists containing start and end 
            tarray.append(list[-1])
   
    time_stamp=[]
    for i in range(0,len(tarray)):
        temp=tarray[i]
        time_stamp.append(array[temp])
        





    return time_stamp

def main():
   
    f=open('example2.txt');
    #d=f.read()
    time_array=[]
    pitch_array=[]
    for line in f:
        #r=f.split()
        r=line.split()
        #print r
        time_array.append(r[0])                                         # Load the time into an array
        pitch_array.append(r[1])                                        # Load the values of pitch into an array
    f.close()
    avg = averagepitch_calc(pitch_array)                                # Calculate the average value of the pitch based on the pitch array 
    deviation = deviation_calc(pitch_array,avg)                       # Calculate the points which deviate from the average value of the pitch 
    #spatial_time = time_deviation_single(deviation,time_array)
    spatial_time = time_deviation(deviation,time_array)
    print 'spatial_time is'
    print spatial_time
    f=open('timestamp.txt','w')
    array_len=len(spatial_time)
    count=0
    for i in range(array_len):
      try:
        print 'count is ' 
        print count
        f.write( str(spatial_time[count]) + ' ' + str(spatial_time[count+1])+ '\n')
        count = i+1;
      except IndexError:
         pass 
    f.close()       
  
       
if __name__ == '__main__':
    main()

        
