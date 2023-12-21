import os
import sys
import re
import random
import copy


def getRandomConfig(folderPath):
    selected = random.choice([x for x in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, x))])
    return os.path.join(folderPath, selected)


class BatfishConfigInjector:
    def __init__(self, filePath):
        self.filePath = filePath
        self.configContent = []
        with open(filePath, "r") as file:
            for line in file:
                self.configContent.append(line.strip())
        print("Done reading file.")
    
    def insertInvalidSymbol(self, numFileSamples):
        # select a line an inject number of file samples and random lines to inject
        for i in range(numFileSamples):
            self.configContentNew = []
            lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if line.strip() != "!"])
            for idx, line in enumerate(self.configContent):
                if idx == lineToInject:
                    symbol = random.choice(["@", "%", "^", "&", "(", ")"])
                    if random.choice([True, False]):
                        self.configContentNew.append(line+symbol)
                    else:
                        self.configContentNew.append(symbol+line)
                else:
                    self.configContentNew.append(line)
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.{}".format("invalidSymbol", lineToInject, i), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
        print("Injection complete.")
    
    def injectInvalidRange(self, numPerFile, numFileSamples):
        # matched line that contains an address
        ipPortLines = []
        ipPortLinesToInject = []
        
        # ip:port patten regex
        ip_port_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}'
        for idx, line in enumerate(self.configContent):
            matches = re.findall(ip_port_pattern, line)
            if matches:
                ipPortLines.append(idx)
        
        # select number of file samples and random lines to inject
        for i in range(numFileSamples):
            if len(ipPortLines) < numPerFile:
                ipPortLinesToInject = ipPortLines
            else:
                ipPortLinesToInject = random.sample(ipPortLines, numPerFile)
            self.configContentNew = copy.deepcopy(self.configContent)
            for idx, line in enumerate(self.configContent):
                if idx in ipPortLinesToInject:
                    matches = re.findall(ip_port_pattern, line)
                    ranIndex = random.randrange(len(matches))
                    ipToInject = matches[ranIndex]
                    
                    # Invalid list
                    negNum = [random.randint(-100, -1) for _ in range(100)]
                    posNum = [random.randint(256, 355) for _ in range(100)]
                    invalidList = negNum + posNum
                    
                    # Split the IP address into octets
                    octets = ipToInject.split('.')

                    # Choose a random octet to invalidate
                    invalid_octet_index = random.randrange(len(octets))

                    # Generate an invalid number (outside the range 0-255)
                    invalid_number = random.choice(invalidList)  # Example invalid numbers

                    # Replace the chosen octet with the invalid number
                    octets[invalid_octet_index] = str(invalid_number)

                    # Join the octets back into a string
                    invalid_ip = '.'.join(octets)
                    
                    # Substitute the IP for a new one
                    new_line = line.replace(ipToInject, invalid_ip)
                    
                    # Put that in a file content
                    self.configContentNew[idx] = new_line

            linenumbers = "_".join([str(i) for i in ipPortLinesToInject])
            
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.{}".format("invalidRange", linenumbers, i), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
    print("Injection complete.")
            

    def insertInvalidSubnetFormat(self, numFileSamples):
        # select a line an inject number of file samples and random lines to inject
        for num_file in range(numFileSamples):
            self.configContentNew = []
            
            regexp = re.compile(r'[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}/[\d]{1,3}')    
            
            lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if regexp.search(line.strip())])
            for idx, line in enumerate(self.configContent):
                if idx == lineToInject:
                    symbol = random.choice(["@", "%", "^", "&", "(", ")", "/"])
                    
                    line_list = line.split(' ')
                    subnet_words_in_line = []
                    for i in range(len(line_list)):
                        if line_list[i].count('/') == 1:
                            subnet_words_in_line.append(i)
                    
                    subnet_pos_in_line = random.choice(subnet_words_in_line)          
                    
                    if random.choice([False, True]):    
                        insert_loc_in_word = random.choice(range(len(line_list[subnet_pos_in_line])))
                        line_list[subnet_pos_in_line] = line_list[subnet_pos_in_line][:insert_loc_in_word] + symbol + line_list[subnet_pos_in_line][insert_loc_in_word:]
                        line = ' '.join(line_list)
                    else:
                        insert_loc_in_word = line_list[subnet_pos_in_line].find('/')
                        line_list[subnet_pos_in_line] = line_list[subnet_pos_in_line].replace('/', "//")
                        line = ' '.join(line_list)
                        symbol = "/"
                    
                self.configContentNew.append(line)
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.word_{}.col_{}.ins{}".format("invalidSubnet", lineToInject, subnet_pos_in_line, insert_loc_in_word, ord(symbol)), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
        print("Injection complete.")

    
    def insertInvalidInterfaceFormat(self, numFileSamples):
        # select a line an inject number of file samples and random lines to inject
        for num_file in range(numFileSamples):
            self.configContentNew = []
            
            regexp = re.compile(r'[A-Za-z][\d]{1,3}/[\d]{1,3}')    
            
            # lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if '/' in line.strip()])
            lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if regexp.search(line.strip())])
            for idx, line in enumerate(self.configContent):
                if idx == lineToInject:
                    symbol = random.choice(["@", "%", "^", "&", "(", ")", "/"])
                    
                    line_list = line.split(' ')
                    int_words_in_line = []
                    for i in range(len(line_list)):
                        if line_list[i].count('/') == 1:
                            int_words_in_line.append(i)
                    
                    int_pos_in_line = random.choice(int_words_in_line)          
                    
                    if random.choice([False, True]):    
                        insert_loc_in_word = random.choice(range(len(line_list[int_pos_in_line])))
                        line_list[int_pos_in_line] = line_list[int_pos_in_line][:insert_loc_in_word] + symbol + line_list[int_pos_in_line][insert_loc_in_word:]
                        line = ' '.join(line_list)
                    else:
                        insert_loc_in_word = line_list[int_pos_in_line].find('/')
                        line_list[int_pos_in_line] = line_list[int_pos_in_line].replace('/', "//")
                        line = ' '.join(line_list)
                        symbol = "/"

                    
                self.configContentNew.append(line)
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.word_{}.col_{}.ins_{}".format("invalidInterface", lineToInject, int_pos_in_line, insert_loc_in_word, ord(symbol)), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
        print("Injection complete.")


    def insertInvalidPathFormat(self, numFileSamples):
        # select a line an inject number of file samples and random lines to inject
        for num_file in range(numFileSamples):
            self.configContentNew = []
            
            regexp = re.compile(r'[A-Za-z]/[A-Za-z]')    
            
            lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if regexp.search(line.strip())])
            for idx, line in enumerate(self.configContent):
                if idx == lineToInject:                    
                    line_list = line.split(' ')
                    subnet_words_in_line = []
                    for i in range(len(line_list)):
                        if line_list[i].count('/') == 1:
                            subnet_words_in_line.append(i)
                    
                    subnet_pos_in_line = random.choice(subnet_words_in_line)          
                    
                    insert_loc_in_word = line_list[subnet_pos_in_line].find('/')
                    line_list[subnet_pos_in_line] = line_list[subnet_pos_in_line].replace('/', "//")
                    line = ' '.join(line_list)
                    symbol = "/"

                    
                self.configContentNew.append(line)
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.word_{}.col_{}.ins_{}".format("invalidInterface", lineToInject, subnet_pos_in_line, insert_loc_in_word, ord(symbol)), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
        print("Injection complete.")

    
    def swapControl(self, numFileSamples):
        # select a line an inject number of file samples and random lines to inject
        for num_file in range(numFileSamples):
            self.configContentNew = []  
            control_words = ["permit", "deny", "remark"]
            lineToInject = random.choice([idx for idx, line in enumerate(self.configContent) if any([c in line.strip() for c in control_words])])
            for idx, line in enumerate(self.configContent):
                if idx == lineToInject:                    
                    for c_idx in range(len(control_words)):
                        if control_words[c_idx] in line:
                            control_before = control_words[c_idx]
                            control_after = control_words[(c_idx+random.choice([1,2]))%3]
                            line = line.replace(control_before, control_after)
                            print(line)
                            break
                    
                self.configContentNew.append(line)
            # Open the file in write mode
            with open(self.filePath+".{}.line_{}.from_{}.to_{}".format("swapControl", lineToInject, control_before, control_after), 'w') as file:
                # Write each line to the file
                for line in self.configContentNew:
                    file.write(line + '\n')
        print("Injection complete.")

    

if __name__ == "__main__":
    filePath = "/as2border2.cfg"
    # filePath = "E:\LLM\configs\\as2border2.cfg"
    # folderPath = "E:\\LLM\\configs"
    # filePath = getRandomConfig(folderPath)
    print(filePath)
    bci = BatfishConfigInjector(filePath)
    # bci.insertInvalidSymbol(numFileSamples=25)
    # bci.injectInvalidRange(numPerFile=1, numFileSamples=5)
    # bci.injectInvalidRange(numPerFile=2, numFileSamples=5)           
    # bci.injectInvalidRange(numPerFile=3, numFileSamples=5)            
    # bci.injectInvalidRange(numPerFile=4, numFileSamples=5)             
    # bci.injectInvalidRange(numPerFile=5, numFileSamples=5)
    # bci.insertInvalidSubnetFormat(numFileSamples=10)
    # bci.insertInvalidInterfaceFormat(numFileSamples=20)
    bci.swapControl(numFileSamples=20)