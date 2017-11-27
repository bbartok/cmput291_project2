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


def find_and_remove(query, regex):
    match = re.findall(regex, query)
    query = re.sub(regex, '', query)
    return match, query


def format_to_key(match):
    result = []
    for each in match:
        for word in each.split():
            word = re.sub(r'[:\-\"]', '', word)
            result.append(word)
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
        # match = re.findall(r'year *([\<\>\:]) *([0-9]+)', query)
        match, query = find_and_remove(query, r'year *([\<\>\:]) *([0-9]+)')
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



        # Title:
        # TODO: BUG. Name cannot contains characters like &eacute
        # match = re.findall(r'title *: *\"*([\w \:_\-]*)\"', query)
        # match += re.findall(r'title *: *([\w_\-]+)', query)
        # match1, query = find_and_remove(query, r'title *: *\"*([\w \:_\-]*)\"')
        match1, query = find_and_remove(query, r'title *: *(\"*[\w \:_\-]+\")')
        match2, query = find_and_remove(query, r'title *: *([\w_\-]+)')
        # match += single_match
        for word in format_to_key(match1 + match2):
            result = self.search_title(word)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)

        # for title in match1 + match2:
            # for word in title.split():
                # word = re.sub('[:\-]', '', word)
                # result = search_db(self.terms_db, ('t-'+word).encode(), keep_index=1)
                # if global_result == None:
                    # global_result = set(result)
                # else:
                    # global_result &= set(result)

        # Author:
        # TODO: BUG. Name cannot contains characters like &eacute
        # match = re.findall(r'author *: *(\w+)', query)
        # match += re.findall(r'author *: *\"([\w \.]*)\"', query)
        match1, query = find_and_remove(query, r'author *: *(\w+)')
        match2, query = find_and_remove(query, r'author *: *\"([\w \.]*)\"')
        # match += single_match
        for word in format_to_key(match1 + match2):
            result = self.search_author(word)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)

        # for author in match1 + match2:
            # for word in author.split():
                # print(word)
                # result = search_db(self.terms_db, ('a-'+word).encode(), keep_index=1)
                # print('result=', result)
                # if global_result == None:
                    # global_result = set(result)
                # else:
                    # global_result &= set(result)

        # Other:
        # match = re.findall(r'other *: *(\w+)', query)
        match1, query = find_and_remove(query, r'other *: *(\w+)')
        # match += re.findall(r'other *: *\"([\w ]*)\"', query)
        match2, query = find_and_remove(query, r'other *: *\"([\w ]*)\"')
        # match += single_match
        for word in format_to_key(match1 + match2):
            result = self.search_other(word)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)
        # for other in match:
            # for word in other.split():
                # word = re.sub('[:\-]', '', word)
                # result = search_db(self.terms_db, ('o-'+word).encode(), keep_index=1)
                # if global_result == None:
                    # global_result = set(result)
                # else:
                    # global_result &= set(result)

        # No prefex:
        # TODO: not finished
        # match = re.findall(r' (\w+) ', query)
        # match += re.findall(r'(\w+)', query)
        # match += re.findall(r'\"([\w ]*)\"', query)
        # single_match = match
        # single = re.sub(r'output\s*=\s*(key|full)', '', query)
        # single = re.sub(r'year *([\<\>\:]) *([0-9]+)', '', single)
        # single = re.sub(r'title *: *\"*([\w \:_\-]*)\"', '', single)
        # single = re.sub(r'title *: *([\w_\-]+)', '', single)
        # single = re.sub(r'author *: *(\w+)', '', single)
        # single = re.sub(r'author *: *\"([\w \.]*)\"', '', single)
        # single = re.sub(r'other *: *(\w+)', '', single)
        # single = re.sub(r'other *: *\"([\w ]*)\"', '', single)
        # single = single.split()
        match1, query = find_and_remove(query, r'(\".+\")')
        query = re.sub(r'\w+:\w*', '', query)
        single = query.split() + match1
        single_match = []
        for each in single:
            if ':' not in each:
                single_match.append(each)

        keys = format_to_key(single_match)
        for word in keys:
            single_title = self.search_title(word)
            single_author = self.search_author(word)
            single_other = self.search_other(word)

        if len(keys) > 0:
            single_result = set(single_title) | set(single_author) | set(single_other)
            if global_result == None:
                global_result = single_result
            else:
                global_result &= single_result


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

    def search_title(self, word):
        return search_db(self.terms_db, ('t-'+word).encode(), keep_index=1)

    def search_author(self, word):
        return search_db(self.terms_db, ('a-'+word).encode(), keep_index=1)

    def search_other(self, word):
        return search_db(self.terms_db, ('o-'+word).encode(), keep_index=1)

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
