from presidio_anonymizer import AnonymizerEngine
class PIIanonymizer:
    def __init__(self):
        print("starting anonymizer engine")
        self.anonymizer=AnonymizerEngine()
    def anonymizePII(self,text,analyzer_results):
        result=self.anonymizer.anonymize(text=text,analyzer_results=analyzer_results)
        return result.text
