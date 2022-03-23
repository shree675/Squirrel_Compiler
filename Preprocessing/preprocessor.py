import re
class Preprocessor():
    
    def preprocess(self, filename, file, save = False):
        #print ("preprocessing", file)
        #print("Save the preprocessed file?", save)
        output = ""

        #------------------------------------------------------------------------------
        # 'replace' implementation of preprocessor
        # Supports chain macros just like in C
        # macros must be single line
        for line in file.splitlines():
            line = line.strip()
            if re.match("replace", line):
                line = line.split(" ",2)
                #print(line)
                file = file.replace(line[1], line[2])
        #------------------------------------------------------------------------------
        # 'import' implementation of preprocessor
        # At the end of this for loop, the modified file is available in output
        for line in file.splitlines():
            line = line.strip()
            if re.match("import", line):
                tokens = line.split(" ")
                #print(tokens)
                import_file_name = tokens[3][1:-1]
                function_name = tokens[1]
                #print("importing file", import_file_name)
                try:
                    import_file_handle = open("./StandardLibrary/"+import_file_name, "r")
                    import_file = import_file_handle.read()
                    import_file_handle.close()
                    pattern = "@"+function_name
                    pattern1 = "int "+pattern
                    pattern2 = "float "+pattern
                    pattern3 = "void "+pattern
                    pattern4 = "char "+pattern
                    pattern5 = "string "+pattern
                    pattern6 = "bool "+pattern
                    start_index = max(import_file.find(pattern1), import_file.find(pattern2), import_file.find(pattern3), import_file.find(pattern4), import_file.find(pattern5), import_file.find(pattern6))
                    #print(start_index)
                    end_index = import_file.find("#", start_index+1)
                    #print(end_index)
                    imported_function = import_file[start_index:end_index]
                    output = imported_function + "\n" + output
                except: 
                    print("Error in opening Standard Library file")
            elif re.match("replace", line):
                pass
            else:
                output = output + "\n" + line
        #------------------------------------------------------------------------------
        #print("Preprocessed file:")
        #print(output)

        if save:
            preprocessed_file = open("./Output/preprocessed_"+filename, "w")
            preprocessed_file.write(output)
            preprocessed_file.close()

        return output