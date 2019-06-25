import xml.sax

output = open("xmlTestSummary","w")

class xml_Handler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.synset = ""
        self.domains = ""
        self.sumo = ""
        self.synonyms = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "synset":
            id = attributes["id"]
            print "\nsynset id:", id
            output.write('\n'+str(id) +'\t')

        elif tag == "sumo":
            if "type" in attributes._attrs.keys():
                type = attributes["type"]
                #print "sumo.type:", type
                output.write(type + '\t')

    # Call when an elements ends
    def endElement(self, tag):
        #if self.CurrentData == "synset":
        #    print "synset:", self.synset
        if self.CurrentData == "domains":
            #print "domains:", self.domains
            #domaintSet.add(self.domains)
            output.write(self.domains + '\t')
        elif self.CurrentData == "sumo":
            #print "sumo.value:", self.sumo
            output.write(self.sumo)
        #elif self.CurrentData == "synonyms":
            #print "synonyms:", self.synonyms
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "synset":
            self.synset = content
        elif self.CurrentData == "domains":
            self.domains = content
        elif self.CurrentData == "sumo":
            self.sumo = content
        #elif self.CurrentData == "synonyms":
        #    self.synonyms = content
