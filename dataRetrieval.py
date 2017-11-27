#!/usr/bin/env python3
from bsddb3 import db
import re

def search_db(db, expr, keep_index=None):
    # Search key from the given database.
    # expr: key
    # keep_index: specify the return should contain key:0 or value:1, if
    # None then key-value pair is returned.
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
    # Convert a list of phrases to keys by spliting each word and remove
    # special characters.
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

        # This specify the output should be key only or complete records.
        # 'key' or 'full'
        self.output_format = 'key'

    def parse(self, query):
        # The main parser for the database, the query is a string containing
        # conditions defined in the project specification. This function will
        # print all keys/records satisfy the conditions.

        query = query.lower()
        query = re.sub(r'\.', '', query)

        if query == 'exit':
            return 'exit'

        # Setting output format:
        match = re.findall(r'output\s*=\s*(key|full)', query)
        if len(match) > 0:
            self.output_format = match[0]
            print('Output format set to \"{}\"'.format(self.output_format))
            return 

        # This variable will be a set containing all records satisfy given
        # conditions.
        global_result = None

        # Parse year conditions:
        match, query = find_and_remove(query, r'year *([\<\>\:]) *([0-9]+)')
        for sign, year in match:
            if sign == '>':
                result = self.search_year_from(year, keep_index=1)
            elif sign == '<':
                result = self.search_year_until(year, keep_index=1)
            elif sign == ':':
                result = search_db(self.years_db, year.encode(), keep_index=1)
            else:
                raise ValueError('Sign not recognized')
            # Update global result using set operations:
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)



        # Parse title conditions:
        comp_match = re.findall(r'title *: *\"([\w \:_\-]+)\"', query)
        match1, query = find_and_remove(query, r'title *: *(\"[\w \:_\-]+\")')
        match2, query = find_and_remove(query, r'title *: *([\w_\-]+)')
        for word in format_to_key(match1 + match2):
            result = self.search_title(word)
            print(result)
            result = self.filter_order_match(result, comp_match+match2)
            print(result)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)


        # Parse author conditions:
        match1, query = find_and_remove(query, r'author *: *(\w+)')
        match2, query = find_and_remove(query, r'author *: *\"([\w \.]*)\"')
        for word in format_to_key(match1 + match2):
            result = self.search_author(word)
            result = self.filter_order_match(result, match2+match1)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)


        # Parse other conditions:
        match1, query = find_and_remove(query, r'other *: *(\w+)')
        match2, query = find_and_remove(query, r'other *: *\"([\w ]*)\"')
        for word in format_to_key(match1 + match2):
            result = self.search_other(word)
            result = self.filter_order_match(result, match2+match1)
            if global_result == None:
                global_result = set(result)
            else:
                global_result &= set(result)

        # Parse conditions that does not have prefex, single word/phrase matching:
        comp_match = re.findall(r'\"(.+)\"', query)
        match1, query = find_and_remove(query, r'(\".+\")') # with quotation
        query = re.sub(r'\w+:\w*', '', query) # remove unrecognized prefix
        single = query.split() + match1 # The remaining single words plus phrase in quotation
        single_match = []
        for each in single:
            if ':' not in each:
                single_match.append(each)

        # Search from all terms:
        title_set = None
        author_set = None
        other_set = None
        keys = format_to_key(single_match)
        for word in keys:
            single_title = self.search_title(word)
            single_title = self.filter_order_match(single_title, comp_match + single_match)
            single_author = self.search_author(word)
            single_author = self.filter_order_match(single_author, comp_match + single_match)
            single_other = self.search_other(word)
            single_other = self.filter_order_match(single_other, comp_match + single_match)
            if title_set is None:
                title_set = set(single_title)
            else:
                title_set &= set(single_title)
            if author_set is None:
                author_set = set(single_author)
            else:
                author_set &= set(single_author)
            if other_set is None:
                other_set = set(single_other)
            else:
                other_set &= set(single_other)

        # The result should be union of all categories intersect with the
        # previous results.
        if len(keys) > 0:
            # single_result = set(single_title) | set(single_author) | set(single_other)
            single_result = title_set | author_set | other_set
            if global_result == None:
                global_result = single_result
            else:
                global_result &= single_result

        # Print the result:
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

    def filter_order_match(self, search_result, match):
        # Filter in-order matches.
        result = []
        for key in search_result:
            for record in search_db(self.recs_db, key, keep_index=1):
                for phrase in match:
                    # print(phrase, str(record, 'utf-8').lower())
                    s = str(record, 'utf-8').lower()
                    s = re.sub(r'[:\-\"]', ' ', s)
                    if phrase in s:
                        # print('yes')
                        result.append(key)
        return result

    def search_year_from(self, min_year, keep_index=None):
        # Search year start from min_year
        # keep_index: specify the return should contain key:0 or value:1, if
        # None then key-value pair is returned.
        result = []
        cursor = self.years_db.cursor()
        last = cursor.last()
        if int(min_year) > int(str(last[0], 'utf-8')):
            return result
        item = cursor.set_range(min_year.encode())
        while item != None:
            if str(item[0], 'utf-8') != min_year:
                if keep_index is None:
                    result.append(item)
                else:
                    result.append(item[keep_index])
            item = cursor.next()
        return result

    def search_year_until(self, max_year, keep_index=None):
        # Search year end with max_year
        # keep_index: specify the return should contain key:0 or value:1, if
        # None then key-value pair is returned.
        result = []
        cursor = self.years_db.cursor()
        last = cursor.last()
        if int(max_year) > int(str(last[0], 'utf-8')):
            return result
        item = cursor.first()
        while item != None:
            if int(str(item[0], 'utf-8')) >= int(max_year):
                break
            if keep_index is None:
                result.append(item)
            else:
                result.append(item[keep_index])
            item = cursor.next()
        return result

    def search_title(self, word):
        # Search title
        # word: key
        return search_db(self.terms_db, ('t-'+word).encode(), keep_index=1)

    def search_author(self, word):
        # Search author
        # word: key
        return search_db(self.terms_db, ('a-'+word).encode(), keep_index=1)

    def search_other(self, word):
        # Search other
        # word: key
        return search_db(self.terms_db, ('o-'+word).encode(), keep_index=1)

    def close(self):
        self.recs_db.close()
        self.terms_db.close()
        self.years_db.close()

if __name__ == '__main__':
    dbms = DataRetrieval()
    while True:
        query = input('\033[94mQuery : \033[0m') # color prompt
        if dbms.parse(query) == 'exit':
            break
    dbms.close()
