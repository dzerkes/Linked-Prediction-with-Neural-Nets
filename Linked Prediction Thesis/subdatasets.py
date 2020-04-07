dataset_string = 'Dataset/sx-stackoverflow.txt'
parts = 8192

def slice_the_dataset(filename,parts):

    #slice dataset because we cant compile it with the big dataset
    #records are 63 497 050

    counter_max = ((63 * 1000 * 1000 ) + (497 *1000) + 50) / parts
    filecounter = 0
    counter = 0
    sliced_dataset = open('Dataset/sliced_dataset_0.txt', 'w') # here we are writing the sub datasets .. we will be changing the 0 .. to 1 , 2 ...

    with open('Dataset/sx-stackoverflow.txt', 'r') as whole_dataset:
        for line in whole_dataset:
            sliced_dataset.write(line)
            counter += 1

            if (counter == counter_max) and (filecounter != parts): # it helps in case the division is not round! The last Dataset will include everything that remains and will not let something out
                sliced_dataset.close()
                filecounter +=1
                tmp_string = 'Dataset/sliced_dataset_' + str(filecounter) + '.txt'

                sliced_dataset = open(tmp_string,'w')
                counter = 0




    sliced_dataset.close()


slice_the_dataset(dataset_string,parts)
