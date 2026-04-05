import spacy
class NLPProcessor:
    def __init__(self):
        print("Loading the NLP processor ...")
        self.nlp=spacy.load("en_core_web_lg")
    def processText(self,text):
        # text is processed using the nlp engine we loaded
        doc=self.nlp(text)
        return doc
    def getTokens(self,doc):
        #sentence is split in to tokens 
        tokens=[]
        for token in doc:
            tokens.append(token.text)
        return tokens
    def getPosTags(self,doc):
        #parts of speech of the word is identfied here
        posTags=[]
        for token in doc:
            posTags.append((token.text,token.pos_))
        return posTags
    def getEntities(self,doc):
        entities=[]
        for ent in doc.ents:
            entities.append((ent.text,ent.label_))
        return entities
