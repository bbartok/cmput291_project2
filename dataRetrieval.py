#!/usr/bin/env python3
from bsddb3 import db
import re

def search_db(db, expr, keep_index=None):
    cursor = db.cursor()
    item = cursor.set(expr)
    result = []
    while item != None:
        if keep_index is None:
            result.append(item)
        else:
            result.append(item[keep_index])
        item = cursor.next_dup()
    return result

class DataRetrieval:
    def __init__(self):
        self.recs_db = db.DB()
        self.recs_db.set_flags(db.DB_DUP)
        self.recs_db.open('re.idx')

        self.terms_db = db.DB()
        self.terms_db.set_flags(db.DB_DUP)
        self.terms_db.open('te.idx')

        self.years_db = db.DB()
        self.years_db.set_flags(db.DB_DUP)
        self.years_db.open('ye.idx')
        cur = self.years_db.cursor()

        self.output_format = 'key'

    def parse(self, query):
        query = query.lower()
        query = re.sub(r'\.', '', query)

        if query == 'exit':
            return 'exit'

        match = re.findall(r'output\s*=\s*(key|full)', query)
        if len(match) > 0:
            self.output_format = match[0]
            print('Output format set to \"{}\"'.format(self.output_format))
            return 

        # Years:
        match = re.findall(r'year *([\<\>\:]) *([0-9]+)', query)
        global_result = None
        # global_result = set()
        for sign, year in match:
            if sign == '>':
                result = self.search_year_from(year, keep_index=1)
            elif sign == '<':
                result = self.search_year_until(year, keep_index=1)
            elif sign == ':':
                result = search_db(self.years_db, year.encode(), keep_index=1)
            else:
                raise ValueError('Sign not recognized')
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)

        # No prefex:
        # TODO: not finished
        # match = re.findall(r' (\w+) ', query)
        # match += re.findall(r'(\w+)', query)
        # match += re.findall(r'\"([\w ]*)\"', query)
        # single_match = match
        single_match = []

        # Title:
        # TODO: BUG. Name cannot contains characters like &eacute
        match = re.findall(r'title *: *\"*([\w \:_\-]*)\"', query)
        match += re.findall(r'title *: *([\w_\-]+)', query)
        match += single_match
        for title in match:
            for word in title.split():
                word = re.sub('[:\-]', '', word)
                result = search_db(self.terms_db, ('t-'+word).encode(), keep_index=1)
                if global_result == None:
                    global_result = set(result)
                else:
                    global_result &= set(result)

        # Author:
        # TODO: BUG. Name cannot contains characters like &eacute
        match = re.findall(r'author *: *(\w+)', query)
        match += re.findall(r'author *: *\"([\w \.]*)\"', query)
        match += single_match
        for author in match:
            for word in author.split():
                result = search_db(self.terms_db, ('a-'+word).encode(), keep_index=1)
                if global_result == None:
                    global_result = set(result)
                else:
                    global_result &= set(result)

        # Other:
        match = re.findall(r'other *: *(\w+)', query)
        match += re.findall(r'other *: *\"([\w ]*)\"', query)
        match += single_match
        for other in match:
            for word in other.split():
                word = re.sub('[:\-]', '', word)
                result = search_db(self.terms_db, ('o-'+word).encode(), keep_index=1)
                if global_result == None:
                    global_result = set(result)
                else:
                    global_result &= set(result)


        if global_result is None:
            print('Invalid syntax')
        else:
            if self.output_format == 'key':
                for key in global_result:
                    print(str(key, 'utf-8'))
            elif self.output_format == 'full':
                for key in global_result:
                    for record in search_db(self.recs_db, key, keep_index=1):
                        print(str(record, 'utf-8'))

    def search_year_from(self, min_year, keep_index=None):
        result = []
        cursor = self.years_db.cursor()
        item = cursor.set_range(min_year.encode())
        while item != None:
            if keep_index is None:
                result.append(item)
            else:
                result.append(item[keep_index])
            item = cursor.next()
        return result

    def search_year_until(self, max_year, keep_index=None):
        result = []
        cursor = self.years_db.cursor()
        item = cursor.first()
        while int(item[0]) <= int(max_year):
            if keep_index is None:
                result.append(item)
            else:
                result.append(item[keep_index])
            item = cursor.next()
        return result

    def close(self):
        self.recs_db.close()
        self.terms_db.close()
        self.years_db.close()

if __name__ == '__main__':
    dbms = DataRetrieval()
    while True:
        query = input('> ')
        if dbms.parse(query) == 'exit':
            break
    dbms.close()
