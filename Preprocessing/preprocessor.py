
class Preprocessor():
    
    def preprocess(self, filename, file, save = False):
        print ("preprocessing", file)
        print(save)

        if save:
            preprocessed_file = open("./Output/preprocessed_"+filename, "w")
            preprocessed_file.write(file)
            preprocessed_file.close()