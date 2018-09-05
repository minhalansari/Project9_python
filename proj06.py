##################################################################
#Project 9
#This program takes a file and opens it
#reads file and extracts username, month, and hashtags
#Displays top three hashtags combined counts and hashtags
#Top three hashtags by individual count hashtags and usernames
#Username list
#prompts user to enter two usernames
#displays similarities between two users month and counts
#asks user to plot
#if yes, then display plot
#################################################################

import string, calendar, pylab
import calendar

MONTH_NAMES = [calendar.month_name[month] for month in range(1,13)]

def open_file():
    '''prompts user to enter a file name, opens the file and returns it. 
    If there is an error it tells the user then prompts for another filename.'''
    filename = input("Input a filename: ") #File entered by user
    
    #whileloop that runs while the file is not an empty string
    while filename != ' ': 
        #try and except which checks if the file is valid
        try:
            fp = open(filename, 'r') #filepointer opened for reading
            print()
            return fp #returns the file pointer
            break    #breaks the while look once filepointer is returned
        except FileNotFoundError:
            print("Error in input filename. Please try again.")
            filename = input("Input a filename: ")
            

def validate_hashtag(s):
    '''takes a string and checks if it is a hashtag that 
    doesnt contain punctuation or numbers. returns true or false.'''
    #for loop checking if there is punctuatioin in the string
    for i in string.punctuation:  
        if i in s and i != '#':
            return False
    #for loop checking if there is a number in the string
    for i in range(0,10):
        if str(i) in s[1]:
            return False
    return True    #returns true if there is no number or punctuation
        
def get_hashtags(s):
    '''takes strings and goes through it to search for hashtags. 
    calls validata hashtag function to check the hashtag then returns a list of hashtags'''   
    list1= [] #initialize list
    s = s.split() #split by whitespaces
    #for loop to check if hashtag is in the word and validate it
    for c in s:
        if '#' in c:
            if validate_hashtag(c): # if validate hashtag is true then append to the list
                list1.append(c)
    return list1
def read_data(fp):
    '''takes an opened data file pointed. reads it to return a list of 
    lists containing username, month and hashtags'''
    finallist = [] #intialize list
    #for loop to go through each line and strip and split by the comma
    
    for line in fp:
        line = line.strip().split(',')
        hashtags = get_hashtags(line[2]) #find hashtags in the line
        username = line[0] #separated twitter username
        month = int(line[1]) #month of tweet
        linelist = [username, month, hashtags] #list containing username month and hashtags
        finallist.append(linelist) #append this list to finallist
    return finallist
def get_histogram_tag_count_for_users(data,usernames):
    '''takes data and a list of usernames and returns a histogram,
    which is a dictonary containing hashtags as a key and 
    the count as the value.'''
    hist = {} #intialize histogram dictionary
    #go through each line
    for l in data:
        name = l[0] #separate username
        #if username is part of username entered
        if name in usernames:
            hashtags = l[2] #get hashtags
            #go through hashtag list and add to dictionary as key and count as value
            for h in hashtags:
                if h in hist:
                    hist[h] += 1
                else:
                    hist[h] = 1
    return hist

def get_tags_by_month_for_users(data,usernames):
    '''takes data and a list of usernames and returns a list of 
    tuples with the key being the month number and the value
    being a set with all the hashtags used in that month'''
    #list of tuples with month numbers and empty sets
    list2 = [(1, set()),(2,set()),(3,set()),(4,set()),(5, set()),(6,set()),(7,set()),(8,set()),(9, set()), (10, set()), (11,set()),(12,set())]
    #for loop going through each line
    for l in data:
        name = l[0] #separate username
        # if the name is in the usernames list, take the month and hashtags
        if name in usernames:
            month = int(l[1])
            hashtags = l[2]
            #go through each tuple in the list
            for tup in list2:
                #if month equals month in list
                if month == tup[0]:
                    for h in hashtags: #add each hashtag to the set for that month
                        tup[1].add(h)
    return list2              
   
def get_user_names(L):
    '''takes data and returns an alphabetical list of
    the names that appear in the data'''
    namelist = [] #initialize list
    #for loop going through each line in the data
    for l in L:
        name = l[0]   #separate username
        #add name to namelist if not already there
        if name not in namelist:
            namelist.append(name)
    sortednamelist = sorted(namelist) #sort name list alphabetically
    return sortednamelist

def three_most_common_hashtags_combined(L,usernames):
    '''takes data and a list of usernames. returns a
    list of the three most common hashtags by the users in the list 
    and its count'''
    hist = get_histogram_tag_count_for_users(L, usernames)  #histogram containing hashtags and count
    histlist = [] #initialize list
    #for loop for keys and values in histogram
    for k, v in hist.items():
        tup1 = (v, k) #tuple containing value and key
        histlist.append(tup1) #append tuple to the list
    sortedhlist = sorted(histlist) #sorted list
    finallist = [sortedhlist[-1],sortedhlist[-2], sortedhlist[-3]] #list containing top three values in list
    return finallist  

def three_most_common_hashtags_individuals(data_lst,usernames):
    '''takes data and a list of usernames. returns a list of
    the top three hashtags used by each user in the list.
    returns hashtag count and username'''
    lastvalues = [] #initialize list
    finallist= [] #initialize list
    finallist2 = [] #initialize list
    #for loop for each name given
    for name in usernames:
        lastvalues.clear() #clear last values list
        namelist = [name] #list containing the name
        hist = get_histogram_tag_count_for_users(data_lst, namelist) #histogram containing hashtags and count for name
        #for loop for key value in histogram
        for k, v in hist.items():
            tup1 = (v, k, name) #create tuple with value key and name
            finallist.append(tup1) #add to final list
    
    sortedfl = sorted(finallist) #sort list
    #add the last three values to the actual final list
    finallist2.append(sortedfl[-1]) 
    finallist2.append(sortedfl[-2])
    finallist2.append(sortedfl[-3])
    return finallist2            
            
            
def similarity(data_lst,user1,user2):
    '''takes data and two usernames. returns a list of months and 
    a set of hashtags used by both users in that month'''
    user1tags = get_tags_by_month_for_users(data_lst, [user1]) #gives month numbers and set of hashtags used by user1 in that month
    user2tags = get_tags_by_month_for_users(data_lst, [user2]) #gives month numbers and set of hashtags used by user2 in that month
    lastlist = [] #initialize list
    #for loop going through user1tags
    for k,v in user1tags:
        month = k #separate month
        set1 = v #separate set of values
        #for loop going through user2tags
        for k,v in user2tags:
            month2 = k #separate month
            set2 = v #separate set of values
            #if months match up
            if month == month2:
                intersection = set2.intersection(set1) #gives the hashtags that are used by user1 and user2 in the month
                tup1 = (month, intersection) #tuple containing month and common hashtags
                lastlist.append(tup1) #add tuple to list
    return lastlist
        
def plot_similarity(x_list,y_list,name1,name2):
    '''Plot y vs. x with name1 and name2 in the title.'''
    
    pylab.plot(x_list,y_list)
    pylab.xticks(x_list,MONTH_NAMES,rotation=45,ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between '+name1+' and '+name2)
    pylab.tight_layout()
    pylab.show()
    # the next line is simply to illustrate how to save the plot
    # leave it commented out in the version you submit
    #pylab.savefig("plot.png")


def main():
    '''calls the other functions to display top three hashtags combined,
    top three hashtags by individual, usernames. prompt for two usernames
    and display the similarities and give option to plot it'''
    # Open the file
    fp = open_file()
    # Read the data from the file
    data = read_data(fp)
    get_tags_by_month_for_users(data,['michiganstateu', 'MSUnews'])
    histcount = get_histogram_tag_count_for_users(data, ['michiganstateu, MSUnews'])
    # Create username list from data
    list1 = get_user_names(data)
    # Calculate the top three hashtags combined for all users
    print("Top Three Hashtags Combined")
    print("{:>6s} {:<20s}".format("Count","Hashtag"))
    topthreecomb = three_most_common_hashtags_combined(data, list1)
    #for loop going through each hashtag and its count
    for item in topthreecomb:
        count = item[0]
        hashtag = item[1]
        print("{:>6d} {:<20s}".format(count,hashtag))
    print()
    # Print them
    # Calculate the top three hashtags individually for all users
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:<20s} {:<20s}".format("Count","Hashtag","User"))
    topthreeind = three_most_common_hashtags_individuals(data, list1)
     #for loop going through each hashtag and its count
    for item in topthreeind:
        count1 = item[0]
        hashtag1 = item[1]
        user1 = item[2]
        print("{:>6d} {:<20s} {:<20s}".format(count1,hashtag1,user1))
    print()
    # Print them
    print('Usernames: ', ', '.join([str(i) for i in list1]))        
    # Prompt for two user names from username list
    usernames1 = input('Input two user names from the list, comma separated: ')
    #while loop to check if usernames are valid and separates the two usernamess
    while usernames1 != '':
        try:
            for names in usernames1:
                names = usernames1.split(',')
            name1 = names[0].lstrip()
            name2 = names[1].lstrip()
            if name1 in list1:
                print()
                break
            else:
                print('Error in user names.  Please try again')
                usernames1 = input('Input two user names from the list, comma separated: ')
    
        except IndexError:
            print('Error in user names.  Please try again')
            usernames1 = input('Input two user names from the list, comma separated: ')
     #print similarities  
    print('Similarities for', name1,'and', name2)
    print("{:12s}{:6s}".format("Month","Count"))
    sim = similarity(data, name1, name2)
    #initialize lists
    x_list = [] 
    y_list = []
    #for loop to get length and month name and append to list
    for i in sim:
        count = len(i[1])
        month = calendar.month_name[int(i[0])]
        x_list.append(i[0])
        y_list.append(count)
        print("{:12s}{:<6d}".format(month,count))
    print()
    choice = input("Do you want to plot (yes/no)?: ")
    # Prompt for a plot
    #plot is user inputs yes
    if choice.lower() == 'yes':
        plot_similarity(x_list,y_list,name1,name2)
    
if __name__ == '__main__':
    main()





        

