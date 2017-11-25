import re, sys

class CreateTerms:

    def __init__(self):
        self.readFile = open(sys.argv[1], 'r')
        self.termsFile = open('terms.txt', 'w')

    def makeFile(self):
        for line in self.readFile:
            self.title(line)
            self.others(line)
            self.authors(line)


        self.readFile.close()
        self.termsFile.close()
        return

    def title(self,line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        title = re.findall(r'<title>(.*?)</title>', line)


        for x in title:
            for y in x.split(' '):
                newTitle = 't-'
                newTitle += re.sub(r'[^a-zA-Z_]', '', y).lower()
                newTitle += ':'
                try:
                    newTitle += endArt[0]
                except IndexError:
                    newTitle += endPro[0]
                newTitle += '\n'
                self.termsFile.write(newTitle)
        return


    def authors(self, line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        author = re.findall(r'<author>(.*?)</author>', line)

        for x in author:
            for y in x.split(' '):
                newAuthor = 'a-'
                newAuthor += re.sub(r'[^a-zA-Z_]', '', y).lower()
                newTitle += ':'
                try:
                    newAuthor += endArt[0]
                except IndexError:
                    newAuthor += endPro[0]
                newAuthor += '\n'
                self.termsFile.write(newAuthor)

        return

    def others(self, line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        other = re.findall(r'<journal>(.*?)</journal>', line)
        other.extend(re.findall(r'<booktitle>(.*?)</booktitle>', line))
        other.extend(re.findall(r'<publisher>(.*?)</publisher>', line))

        for x in other:
            for y in x.split(' '):
                newOther = 'o-'
                newOther += re.sub(r'[^a-zA-Z_]', '', y).lower()
                newOther += ':'
                try:
                    newOther += endArt[0]
                except IndexError:
                    newOther += endPro[0]
                newOther += '\n'
                self.termsFile.write(newOther)
        return



def main():
    x = CreateTerms()
    x.makeFile()
    return

main()
