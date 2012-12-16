import xml.dom.minidom as Dom

class XMLGeneraotor:
	def __init__(self, xml_name):
		self.doc = Dom.Document()
		self.xml_name = xml_name
	
	def createNode(self, node_name):
		return self.doc.createElement(node_name)

	def addNode(self, node, pre_node=None):
		cur_node = node
		if pre_node is not None:
			pre_node.appendChild(cur_node)
		else:
			self.doc.appendChild(cur_node)
		return cur_node
	
	def setNodeAttr(self, node, att_name, value):
		cur_node = node
		cur_node.setAttribute(self, cur_node, value)

	def setNodeValue(self,cur_node, value):
		node_data = self.doc.createTextNode(value)
		cur_node.appendChild(node_data)
	
	def genXml(self):
		f = open(self.xml_name, "w")
		f.write(self.doc.toprettyxml(indent="\t", newl = "\n", encoding="utf-8"))
		f.close()

def main():
	myXMLGenerator = XMLGenerator("Category.xml")
	

