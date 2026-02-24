import os

from langchain_community.document_loaders import TextLoader

class TxtLoader():

    def __init__(self):
        super().__init__()

    def doLoad(self, fileName):
        path = self.getFilePath(fileName)
        return self.loadTxt(path)

    def getFilePath(self, fileName):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "resources", fileName)


    def loadTxt(self, filePath):
        loader = TextLoader(filePath, encoding="utf-8")
        return loader.load()





if __name__ == '__main__':
    print(TxtLoader().doLoad("【经销进货+分子出库】说明.txt"))