import re

class Preprocessor():
    
    def preprocess(self, filename, file, save = False):
        print ("preprocessing", file)
        print(save)

        #------------------------------------------------------------------------------
        # replace implementation of preprocessor
        """ for line in file.splitlines():
            line = line.strip()
            #print(line)
            print("-------------------------------------------------------")
            if re.match("replace", line):
                line = line.split(" ")
                print(line) """
        #------------------------------------------------------------------------------
        # import implementation of preprocessor
        for line in file.splitlines():
            line = line.strip()
            #print(line)
            print("-------------------------------------------------------")
            if re.match("import", line):
                tokens = line.split(" ")
                print(tokens)
                import_file_name = tokens[3]
                function_name = tokens[1]
                print("importing file", import_file_name)
                try:
                    import_file_handle = open("./StandardLibrary/"+import_file_name, "r")
                    import_file = import_file_handle.read()
                    #print(import_file)
                    import_file_handle.close()
                    pattern = "@"+function_name+".*$"
                    pattern = r'@'+function_name+r'(.|\n)*'
                    print(pattern)
                    #"^The.*Spain$"
                    function = re.findall(pattern, import_file)
                    print(function)
                except: 
                    print("Error")
        #------------------------------------------------------------------------------

        if save:
            preprocessed_file = open("./Output/preprocessed_"+filename, "w")
            preprocessed_file.write(file)
            preprocessed_file.close()