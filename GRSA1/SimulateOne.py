import os


def runSmmp(batch,inputFile):
    #edit the line no 92 of main.f to change the path of the input file
    #read the file main.f
    with   open(f'./GRSA{batch}/main.f', 'r', encoding='utf-8') as file:
        data = file.readlines()
        data[91] = "      seqfile='./SEQUENCES/"+inputFile+"'\n"
    #write the file main.f
    with   open(f'./GRSA{batch}/main.f', 'w', encoding='utf-8') as file:
        file.writelines(data)

    #edit line no 258 of grsa.f to change the path of the output file
    #read the file grsa.f
    with   open(f'./GRSA{batch}/grsa.f', 'r', encoding='utf-8') as file:
        data = file.readlines()
        data[257] = "          open(16, file='./RESULTS/"+inputFile +".pdb')	  \n"
    #write the file grsa.f
    with   open(f'./GRSA{batch}/grsa.f', 'w', encoding='utf-8') as file:
        file.writelines(data)
    
    #run the command
    print(f'Entering ./GRSA{batch}')
    # os.system(f'cd ./GRSA{batch}')
    os.system(f'make clean  -C ./GRSA{batch} >!')
    os.system(f'make -C ./GRSA{batch} > !')
    os.system(f'./GRSA{batch}/smmp >! &')
    print(f'Leaving ./GRSA{batch}')
    # os.system("cd ..")
    return



dirs=['three/']
for dir in dirs:
    files=os.listdir("./SEQUENCES/"+dir)
    for file in files:
        if file.endswith('.seq'):
            if(os.path.exists('./RESULTS/'+dir+file+'.pdb')):
                continue
            else:
                print ("Running For "+file)
                runSmmp(1,dir+file)

