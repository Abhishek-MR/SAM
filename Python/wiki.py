import wikipedia
title = raw_input("What do you want to know about ")

try:
    
	print wikipedia.summary(title , sentences=2)
except wikipedia.exceptions.PageError:
	print "I don't know"
except wikipedia.exceptions.DisambiguationError as e:
    flag=True
    i=0
    while flag:
	    
        option = e.options[i]
        print wikipedia.summary(option , sentences=2)
        res=int(input("Is this what youre looking for?"))
        if(res==1):
            flag=False
        else :
            i+=1
            
        
