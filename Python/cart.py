cart = []
def cartop( str ):
		if str.lower() in ['add']:
			nxt_item = raw_input("what do you want to add? ")
			cart.append(nxt_item)
		elif str.lower() in ['show']:
			for x in range(len(cart)):
				print cart[x]
		return 
flag=True
while flag:
	opt = raw_input("hat do you want to do")
	if(opt=="exit"):
		flag=False
	else:
		cartop(opt)
	
	


