from presidio_analyzer import AnalyzerEngine
class PIIanalyzer:
    def __init__(self):
        print("Loading the PII analyzer ...")
        self.analyzer=AnalyzerEngine()
    def detectPII(self,text):
        results= self.analyzer.analyze(text=text,language='en')
        return results


