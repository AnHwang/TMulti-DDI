import xml.sax

class drug():
    def __init__(self,drugbankId,drugName):
        self.drugbankId = drugbankId
        self.drugName = drugName
        #self.smile = smile
        #self.targets = targets
        #self.enzymes = enzymes


class MyHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.drugbankId = ""
        self.drugName = ""
        self.drug = None
        self.drugs = []
        #self.count = 0
        self.previous_tag = ""
        self.current_tag = "" #this note
        self.next_tag = ""
        self.limit = 0

        self.valid = 0
        self.cover = 0

    def startDocument(self):
        pass

    #start
    def startElement(self, tag_name, tag_attrs):
        if tag_name == "drug" and tag_attrs:
            if tag_attrs["type"] == "small molecule":
                self.limit = 1
                self.valid = 1
                self.cover = 1
                self.current_tag = tag_name
                self.previous_tag = tag_name
            else:
                self.limit = 0
                self.valid = 0


        if self.limit == 1 and tag_name == "drugbank-id" and tag_attrs:
            if tag_attrs["primary"] == "true":
                self.current_tag = tag_name

        if self.limit == 1 and self.cover == 1 and tag_name == "name" and self.previous_tag == "drug":
            self.cover = 0
            self.previous_tag == ""
            self.current_tag = tag_name


        if tag_name == "pathways":
            self.limit = 2

        if tag_name == "salts":
            self.limit = 2


    def characters(self, content):

        if self.limit == 1 and self.current_tag == "drugbank-id":
            #print(content)
            #self.count += 1
            self.drugbankId = content
            self.current_tag = ""


        if  self.limit == 1 and self.previous_tag == "drug" and self.current_tag == "name":
            self.limit = 2
            self.drugName = content
            self.current_tag = ""
            #print(content)


    def endElement(self, tag_name):

        if tag_name == "pathways":
            self.limit = 1
        if tag_name == "salts":
            self.limit = 1
        if tag_name == "drug":
            #self.current_tag == ""
            if self.limit == 1 and self.valid == 1:
                self.drug = drug(self.drugbankId,self.drugName)
                #print(self.drugbankId,self.drugName)
                self.drugs.append(self.drug)

    def endDocument(self):
        pass


if __name__ == '__main__':
    # create XMLReader：parper = xml.sax.make_parser()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    handler = MyHandler()
    parser.setContentHandler(handler)
    parser.parse('fulldatabase.xml')
    for i in handler.drugs:
        print(i)

