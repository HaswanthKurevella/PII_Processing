#building an interactive interface for the user to understand about PII-detection and anonymization
#user will give the input and the output will be having each step of the pipeline with the final output of the anonymized data
from nlp_processor import NLPProcessor
from PII_analyzer import PIIanalyzer
from PII_anonymizer import PIIanonymizer
#inputs
ourInput=input("enter your text here:")

#objects
processor=NLPProcessor()
Pii_analyzer=PIIanalyzer()
pii_anonymizer=PIIanonymizer()

#functions
doc=processor.processText(ourInput)
tokens=processor.getTokens(doc)
pos_tags = processor.getPosTags(doc)
entities = processor.getEntities(doc)
pii_results=Pii_analyzer.detectPII(ourInput)
pii_anonymizer_result=pii_anonymizer.anonymizePII(ourInput,pii_results)


print("\nTokens:")
print(tokens)

print("\nPOS Tags:")
print(pos_tags)

print("\nEntities:")
print(entities)

print("\nPII_Detected:")
print(pii_results)

print("\nPII_Anonymized:")
print(pii_anonymizer_result)