from xml.dom import minidom
import traceback
try:
	f = open("category1.xml", "w")
	try:
		doc = minidom.Document()
	   
		rootNode = doc.createElement("CATEGORY")
		nameNode_c = doc.createElement("NAME")
		#nameNode_c.setAttribute("Food")
        
		doc.appendChild(rootNode)

		rootNode.appendChild(nameNode_c)
		nameNodeText = doc.createTextNode("Operating System")
		nameNode_c.appendChild(nameNodeText)
	
		itemNode = doc.createElement("ITEM")
	
		rootNode.appendChild(itemNode)
    
		nameNode_item = doc.createElement("NAME")
       
		itemNode.appendChild(nameNode_item)

		nameNodeText2 = doc.createTextNode("Windows")

		
		nameNodeText2 = doc.createTextNode("Windows")
		nameNode_item.appendChild(nameNodeText2)

		#doc.writexml(f, "\t", "\t", "\n",  "utf-8")
		f.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
	except:
		traceback.print_exc()
finally:
	f.close()
#except Exception:
#	print "Open file failed!"
	


