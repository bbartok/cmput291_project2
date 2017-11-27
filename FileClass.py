import re, sys

class CreateTerms:

    def __init__(self):
        #initilizes terms.tx, years.txt, and recs.txt
        self.readFile = open(sys.argv[1], 'r')       
        self.termsFile = open('terms.txt', 'w')      
        self.yearFile = open('years.txt', 'w')
        self.recsFile = open('recs.txt', 'w')

    def makeFile(self):
        #runs methods to create the files
        for line in self.readFile:
            self.title(line)
            self.others(line)
            self.authors(line)
            self.years(line)
            self.records(line)

        #closes files
        self.readFile.close()
        self.termsFile.close()
        self.yearFile.close()
        self.recsFile.close()
        return

    def title(self,line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        title = re.findall(r'<title>(.*?)</title>', line)
        newTitle = ''
        newList = []
        for i in title:
            newList.append(re.sub(r'[^0-9a-zA-Z_]',' ', i))
                
                            

        for x in newList:
            for y in x.split(' '):
                newTitle = 't-'
                newTitle += re.sub(r'[^0-9a-zA-Z_]', '', y).lower()
                if len(newTitle) < 5:
                    continue
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
        newAuthor = ''
        
        for x in author:
            for y in x.split(' '):
                
                newAuthor = 'a-'
                newAuthor += re.sub(r'[^0-9a-zA-Z_]', '', y).lower()
                if len(newAuthor) < 5:
                    continue
                newAuthor += ':'
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
        newOther = ''
        
        for x in other:
            for y in x.split(' '):
                newOther = 'o-'
                newOther += re.sub(r'[^0-9a-zA-Z_]', '', y).lower()
                if len(newOther) < 5:
                    continue
                newOther += ':'
                try:
                    newOther += endArt[0]
                except IndexError:
                    newOther += endPro[0]
                newOther += '\n'
                self.termsFile.write(newOther)
        return

    def years(self, line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        year = re.findall(r'<year>(.*?)</year>', line)
        newYear =''

        for x in year:
            for y in x.split(' '):
                newYear += y
                newYear += ':'
                try:
                    newYear += endArt[0]
                except IndexError:
                    newYear += endPro[0]

                newYear += '\n'
                self.yearFile.write(newYear)
        return

    def records(self, line):
        endArt = re.findall(r'<article key="(.*?)"', line)
        endPro = re.findall(r'<inproceedings key="(.*?)"', line)
        lineArt = re.findall(r'<article key=(.*?)</article>', line)
        linePro = re.findall(r'<inproceedings key=(.*?)</inproceedings>', line)
        lineFull = ''
        try:
            lineFull = endArt[0]
            lineFull += ':'
            try:
                lineFull += '<article key="'
                lineFull += endArt[0]
                lineFull += lineArt[0]
                lineFull += '</article>\n'
            except IndexError:
                pass
                
        except IndexError:
            try:
                lineFull = endPro[0]
                lineFull += ':'
            except IndexError:
                return
            try:
                lineFull += '<inproceedings key='
                lineFull += endPro[0]
                lineFull += linePro[0]
                lineFull += '</inproceedings>\n'
            except IndexError:
                pass
                
        self.recsFile.write(lineFull)
        return





def main():
    x = CreateTerms()
    x.makeFile()
    return

main()
