# coding: utf-8

import sys


class SxfOsmClassificator:

    MAX_READ_LINES = 100
    WRITE_IN_FILE = True
    LOGGER_ENABLE = False

    def __init__(self, _file_name):
        self.m_inputFile = open(_file_name, "r")
        self.m_outputFile = open('25000SxfOsm.ini', "w")

    def __test(self):
        print "private method test"

    def logger(self, string):

        if self.LOGGER_ENABLE:
            sys.stdout.write(string)
        pass

    def write(self, string):

        if self.WRITE_IN_FILE:
            self.m_outputFile.write(string)
        else:
            sys.stdout.write(string)

    def read_file(self):

        sxf_keys = ["P", "C", "T", "L", "V", "S"]

        counter = 0
        for line in self.m_inputFile:
            if line.count("(") != 0:
                open_scope = line.rfind("(")
                # если скобка найдена и после нее ключ - модифицируется
                if line[open_scope+1] in sxf_keys:
                    close_scope = line.rfind(")")
                    self.logger(" # modified: ")
                    self.write(";" + line[0:open_scope] + "\n")
                    self.logger(" # modified: ")
                    self.write(line[open_scope+1:close_scope] + "=\n")
                else:
                    # если скобка одна и после нее нет ключа - копируется
                    self.logger(" # after scope not sxf key: ")
                    self.write(line)
            else:
                # если скобка не найдена - строка копируется в файл
                self.logger(" # scope not found: ")
                self.write(line)
            # if counter > self.MAX_READ_LINES:
            #     break
            counter += 1

        self.m_inputFile.close()
        self.m_outputFile.close()

# ENTRY POINT
if __name__ == "__main__":

    print " >> begin script"

    if len(sys.argv) > 1:
        isnt = SxfOsmClassificator(sys.argv[1])
        isnt.read_file()
    else:
        print "usage: main.py <file_name>"
        sys.exit(-1)
    print "OK."
    print " << script finish"
