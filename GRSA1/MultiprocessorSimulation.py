import os
import asyncio

async def runSmmp(batch,inputFile):
    #edit the line no 92 of main.f to change the path of the input file
    #read the file main.f
    with await open(f'./GRSA{batch}/main.f', 'r', encoding='utf-8') as file:
        data = file.readlines()
    data[91] = "      seqfile='../SEQUENCES/"+inputFile+"'\n"
    #write the file main.f
    with await open(f'./GRSA{batch}/main.f', 'w', encoding='utf-8') as file:
        file.writelines(data)

    #edit line no 258 of grsa.f to change the path of the output file
    #read the file grsa.f
    with await open(f'./GRSA{batch}/main.f', 'r', encoding='utf-8') as file:
        data = file.readlines()
    data[257] = "          open(16, file='../RESULTS/"+inputFile +".pdb')	  \n"
    #write the file grsa.f
    with await open(f'./GRSA{batch}/main.f', 'w', encoding='utf-8') as file:
        file.writelines(data)
    
    #run the command
    await os.system(f'cd  ./GRSA{batch}')
    await os.system("make clean")
    await os.system("make")
    await os.system("./smmp")
    add_task(batch)
 
    return

dir ="three/"
files = os.listdir("./SEQUENCES/"+dir)
it =0

async def add_task(batch):
    global it
    while (it< len(files)):
        filename = files[it]
        if filename.endswith('.seq'):
            if(os.path.exists('./RESULTS/'+dir+filename+'.pdb')):
                it= it+1
                continue
            else:
                print ("Running For "+filename)
                runSmmp(batch,dir+filename)

    return



# dirs=['three/']
# for dir in dirs:
#     files=os.listdir("./SEQUENCES/"+dir)
#     print(files[0])
    # for file in files:
    #     if file.endswith('.seq'):
    #         if(os.path.exists('./RESULTS/'+dir+file+'.pdb')):
    #             continue
    #         else:
    #             print ("Running For "+file)
                # runSmmp(dir+file)



async def main():
    await asyncio.gather(*(add_task(n+1) for n in range(3)))
    return
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())