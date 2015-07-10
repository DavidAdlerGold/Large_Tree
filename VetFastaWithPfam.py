#!/usr/bin/env python

#everythinglocal("test.fasta", "Sod_Fe_N", "Sod_Fe_C", "/home/abigail/Documents/Summons/GetEverything")
#this should work on anything that is straight from NCBI. 
##everythingnotlocal("TestTop10000SOD.fasta", 2500, "Sod_Fe_N", "Sod_Fe_C", "/home/abigail/Documents/Summons/GetEverything")
##
##Use local version if you have pfam database installed and you are me and your computer can handle it
##ELSE use everythingnotlocal, and you'll have to manually submit things to Pfam server
## Run this file, then run everythingnotlocal(inputfasta, splitnumber, domain1, domain2, directory of fasta)


# SHORTEN: takes an input .fasta file (straight from NCBI) (filein), and spits out a new
#file named (fileout) with shortened names
#in format [Species_name]|gi:########

def shorten(filein):
    #using regular expressions
    import re
    original = open (filein)
    #this makes sure that the file name ends in .fasta, because I could't figure out
    #how to remove everything after the "." from a file name. I now know the split fxn,
    #but didn't while writing most of this, so it is only consistant with .fasta
    if ".txt" in filein:
        writeto = str(filein[:-4])+"Short.fasta"
    if ".fasta" in filein:
        writeto = str(filein[:-6])+"Short.fasta"
    else:
        writeto = str(filein)+"Short.fasta"
    #this opens a new file to write to
    with open (writeto, "w") as new:
        #this removes words in brackets that aren't Species_name
        #and then changes NCBI's default naming scheme to be
        #[Species_name]|gi:#########
        for line in original:
            edit1 = re.sub ("\[..\]", "", line)
            edit2 = re.sub ("\[..\W..\]", "", edit1)
            edit3 = re.sub ("(>)(gi)(\|)([0-9]*)(\|)([A-Za-z]*)(\|)([0-9()/A-Za-z .:_\|,-]*)(\[.*\])(.*)", "\\1\\9\\3\\2:\\4", edit2)
            edit4 = re.sub (" ","_", edit3)
##            print (edit4)
##            print (line + "line")
            new.write(edit4)
    import os
    #this ensures that the function passes on a full directory-level name of the file in question
    #probably not necessary inside everything() functions that already go to the dir in question,
    #but it doesn't hurt to keep it.
    filelocation = os.getcwd()+"/"+writeto
    print("Shortened names successfully, new file at "+writeto)
    #returns the name of the newly created shortened file
    return filelocation


## RUNPFAM should take an input file in .fasta format, run it through pfam, and create a pfam-output file
## should except the return from shorten(): runpfam(shorten(filein))
## if filein in a different directory, make sure to add /home/abigail/Documents/Summons/ or whatever to filein's name
def runpfam (filein):
##    print("starting, file:"+filein)
    import os
##    if os.path.isfile(filein) == True:
####        print ("The export file is at"+os.getcwd())
##    else:
##        print("Can't find filein")
    #creates a name for output file
    if ".fasta" in filein:
        fileout = str(filein[:-6])+"Pfam.fasta"
##        print("Will export as:"+fileout)
    else:
        print("Please use a .fasta file input.")
    #changes directories to run the perl pfam script correctly
    owd = os.getcwd()
##    print("CWD is:"+owd)
    os.chdir("/home/abigail/Downloads/PfamScan")
    print("will Local pfam work? Input is "+filein)
    # this runs the pfam_scan script from terminal, using perl.
    os.system("perl pfam_scan.pl -fasta "+filein+" -dir /home/abigail/Downloads/PfamData/ -outfile "+fileout)
## something to test if the output was actually created correctly
    print("Attempting to run pfam...")  
    if os.path.isfile(fileout) == True:
        print("Success! The export file is at"+os.getcwd())
        os.system("mv fileout "+owd)
##        print("tried to move file back to: "+owd)
    else:
        print("looked in:"+os.getcwd())
        print("no file here?")
    # moves program back to looking in specified or original directory
    os.chdir(owd)
##    print("back to"+os.getcwd())
    #checks that the created file also was moved back to where it should be
    if os.path.isfile(fileout) == True:
        print ("Success! The export file was moved to"+os.getcwd())
##    print fileout
    return fileout

## consider returning fileout with complete directory information instead?
 #consider figuring out how to add pfam_scan to perl path file.
  
#PFAMSPLT takes a file of shortened names, and splits it into chunks manageable by pfam server online
##            for now, just splits (FILEIN) into chunks of (SIZE) sequences, saved in sequential files
####            eg test.fasta splits and saves as test1.fasta, test2.fasta etc.
##            MAKE SURE YOU ARE IN SAME DIRECTORY AS FILEIN BEFORE RUNNING.
##            ONLY RUN ON .TXT or .FASTA files,  -- now auto-recognizes. -- no longer relevent
def pfamsplit (filein, size):
    #opens the file, lets you know its running
    original = open(filein)
    print("Attempting to make files of length "+size+" sequences")
    #tick counts how many sequences have been written to a single file
    tick = 0
    #num represents the number of files that have been created, starting at 1
    num = 1
    #this ensures that whatever you put it, will put out .fasta files
    if ".txt" in filein:
        writeto = str(filein[:-4])+"1.fasta"
    if ".fasta" in filein:
        writeto = str(filein[:-6])+"1.fasta"
    else:
        print ("error, file not in .fasta or .txt format")
    new = open (writeto, "w")
    #So that you know how many files you will need to upload to pfam server online, and what they are called.
    print("Writing file to: "+writeto)
    for line in original:
        if ">" in line:
            tick +=1
        #specifies when and how to make a new file
        if int(tick) > int(size):
            num +=1
            if ".txt" in filein:
                writeto = str(filein[:-4])+str(num)+".fasta"
            if ".fasta" in filein:
                writeto = str(filein[:-6])+str(num)+".fasta"
            print("Writing file to: "+writeto)
            new = open(writeto, "w")
            tick = 0
##            print (writeto)
        new.write(line)
    #instructions for running the split files through pfam online
    print("Please take the above files and run through Pfam(http://pfam.xfam.org/search#tabview=tab1)")
    print("When finished (may take a while), copy the information (in gmail, use \"see original\") into a .txt document")
    print("Save it as filein#Pfam.fasta.")
##    raw_input("test?")
    #only say "y" if it is done and you saved it correctly.
    a = raw_input("Have you saved all Pfam files? Type y if so ")
    print (a)
    if a == "y":
##        print (filein)
##        print(filein[:-6]+"Pfam.fasta")
        return filein[:-6]+"Pfam.fasta"
    else:
        #tells you what to do if you messed up/decided to exit
        print("That's not valid input")
        print ("Run CombVet(fasta, pfam, domain1, domain2, directory) when you're ready")
        quit()
        
##        print (tick)
##import os
##os.chdir("C:/Users/Abby/Documents/Summer2015/SOD/GetEverything")
##pfamsplit("2Top10000SODshort.fasta",2500)
##
        #COMBINEPFAM to be used after pfam split/manual save
        #combines multiple files of type name1Pfam.txt into one large file
        #returns the name of the large file
        #as input, give it "namePfam.fasta" (no numbers, though all your pfam-output files SHOULD have numbers (name1Pfam.fasta)

def combinepfam(pfamfile):
    print("Starting combine")
    import os
    i = 1
    f = 0
##    print(pfamfile)
    #I don't remember why this is here, but it isn't hurting anyone.
    if ".fasta" in pfamfile:
        f = 1
    #otherwise the number of characters cut off when renaming the file is wrong.
    else:
        print("Please provide all files as .fasta")
        return None
    #creates name to open first pfam-output file.
    checkfile = pfamfile[:-10]+str(i)+"Pfam.fasta"
##    print (checkfile+"checkfile")
##    print (checkfile)
##    print(os.getcwd())
    #creates output combined pfam file name.
    newfile = pfamfile[:-10]+"PfamCombined.fasta"
    #opens the new file to write to
    with open(newfile, "w") as new:
##        print("opened new file")
##        print(os.path.isfile(checkfile))
        #this will be false when it tries to open, say, the fifth file but you only have four.
        while os.path.isfile(checkfile) == True:
            print("Copying "+checkfile)
            check = open(checkfile)
            for line in check:
                new.write(line)
##            print("Wrote them all")
            #this makes it create a new file to look for of increment one higher than the last it found.
            i += 1
            checkfile = pfamfile[:-10]+str(i)+"Pfam.fasta"
##            print (checkfile)
    print("The pfam files have been combined and saved as "+newfile)
    return newfile

## SIMPLIFYPFAM takes a pfam file, removes all the junk at the top/bottom, and uses regular
## expressions to reformat it to keep just the sequence ID and identified domain.
def simplifypfam(pfamfile):
    import re
    original = open (pfamfile)
    outfile = pfamfile[:-6]+"Simple.fasta"
## editing the pfam document with regex to leave only id and domain name    
    with open (outfile, "w") as new:
            for line in original:
                if ">" in line:
                    edit = ""
                elif "Received:" in line:
                    edit = ""
                elif "[" in line:
                    edit = re.sub ("([A-z]*)(\|)(gi:[0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)([0-9]*)(\s*)([0-9A-Z.]*)(\s*)([0-9A-z]*)(\s*)(.*)",
                                "\\1\\2\\3 \\15", line)
                else:
                    edit = ""
                #changed this to match the proper regex to leave only ID and Domain
                new.write(edit)
    print ("The Pfam file has been simplified and saved as "+outfile) 
    return outfile
## eturns the name of the outfile. consider adding proper directory.
##simplifypfam("/home/abigail/Documents/Summons/test66Pfam.txt")

# VERIFYDOMAIN takes input a simplified pfam file + domain to look for, and gives a
# list of GI numbers that
# have that domain.
def verifydomain (inputfile, inputdomain):
    #opens file and initiates list
    print ("Now making a list of all sequences in "+inputfile+"that have domain "+inputdomain)
    orig = open (inputfile)
    #makes empty list
    nameswithdomain = []
    #line-by-line search - if has proper domain, adds gi num to list
    for line in orig:
    #ignores first line or lines of /n
        name,domain = line.split(" ")
##        print (domain[:-1])
##        print (inputdomain)
        if domain[:-1] == inputdomain:
##            print ("same")
            junk, number = name.split("gi:")
##            print (number)
            nameswithdomain.append(number)
    #returns list of gi nums that have the domain
    if nameswithdomain == []:
        print("Error, no sequences found with domain: "+inputdomain)
    else:
        return nameswithdomain


## VETSEQS : combines several functions above:
    #give it domains to look for and a pfam file, and it will run SIMPIFY, run VERIFYDOMAIN
    # for each domain provided, and make a list of all gi#'s that have both domains.
def vetseqs(pfamfile, domain1, domain2):
    #runs the simplify function, and sets a to the name of the new file
    print("Starting Vet Sequences")
    print("Attempting to simplify "+pfamfile)
    a = simplifypfam(pfamfile)
    hasD1 = verifydomain(str(a), domain1)
##    print (hasD1)
##    print("the above is D1")
    hasD2 = verifydomain(str(a), domain2)
##    print (hasD2)
##    print ("the above is D2")
    hasBoth = []
    for number in hasD1:
        if number in hasD2:
            hasBoth.append(number)
##    print(hasBoth)
    return hasBoth

#SHORTPFAMVET will shorten, runpfam, vetseqs, and give you a .fasta file of vetted sequences.
def ShortPfamVet(filein, domain1, domain2):
    shfasta = shorten(filein)
    hasBoth = vetseqs(runpfam(shfasta), domain1, domain2)
    outputfile = shfasta[:-6]+"Vetted.fasta"
    origfasta = open(shfasta)
    with open(outputfile, "w") as new:
        write = 0
        for line in origfasta:
            if ">" in line:
                write = 0
                junk, num = line.split("gi:")
                newn = num[:-1]
                if newn in hasBoth:
                    write = 1
                    new.write (line)
            elif write == 1:
                new.write (line)
    import os        
    print ("Done, exported as "+outputfile+" in location: "+os.getcwd())
    return outputfile

#EverythingLocal will run ShortPfamVet, but from the correct specified
#directory to keep all your generated files together
def everythinglocal(filein, domain1, domain2, directory):
    print "Running Everything with Local Pfam"
    import os
    os.chdir(directory)
    return ShortPfamVet(filein, domain1, domain2)

#SHORTSPLIT goes to directory, and runs shorten and split on a fasta file.
def shortsplit(filein, num, directory):
    print "Running Shorten and Split"
    import os
    os.chdir(directory)
    pfamsplit(shorten(filein), num)
    
#CombVet is what you do after you have a short fasta file and saved pfam files from online,
#and need to run all the vetting stuff.
#Idea is 1. SHORTSPLIT 2.manual upload/saving 3.COMBVET (will be combined in later fxn)
#fasta is the shortened fasta file you should have saved
#pfam is the pfam file you saved, with no numbers.
#domains are the strings of domains you want to match
#directory is the directory in which you fasta and pfam files are saved in.
def CombVet(fasta, pfam, domain1, domain2, directory):
    print "Running Combine and Vet"
    import os
    os.chdir(directory)
    hasBoth = vetseqs(combinepfam(pfam),domain1,domain2)
##    print ("list of both ")
##    print(hasBoth)
    outputfile = fasta[:-6]+"Vetted.fasta"
    origfasta = open(fasta)
##    print("fasta"+fasta)
    with open(outputfile, "w") as new:
##        new.write("test")
        write = 0
        for line in origfasta:
            if ">" in line:
##                print (line)
                write = 0
                junk, num = line.split("gi:")
##                print (num)
                noline = num[:-1]
##                print num
##                print noline
                if noline in hasBoth:
##                    print (num)
                    write = 1
                    new.write(line)
            elif write == 1:
                new.write (line)
    import os        
    print ("Done, exported as "+outputfile+" in location: "+os.getcwd())
    return outputfile

#everythinglocal("1Top10000SOD", "Sod_Fe_N", "Sod_Fe_C", "/home/abigail/Documents/Summons/GetEverything")
#this should work on anything that is straight from NCBI.
#need to do stuff to make it work with pre-shortened .fastas, so I should email myself the old one.

# CombVet("1Top10000SODShort.fasta","1Top10000SODShortPfam.fasta", "Sod_Fe_N", "Sod_Fe_C", "/home/abigail/Documents/Summons/GetEverything")

# only import a file saved as derp.fasta
# else everything breaks atm

##EVERYTHINGNOTLOCAL runs everything. goes to directory to keep stuff together, shortens,
##splits, allows for manual pfam, joins pfam files, vets for two domains,
##spits out a vetted .fasta file
def everythingnotlocal(filein, splitnum, domain1, domain2, directory):
    import os
    os.chdir(directory)
    a = shorten(filein)
    return CombVet(a, pfamsplit(a, splitnum), domain1, domain2, directory)


##OVERALL -
##DOWNLOAD FROM NCBI
##run everythinglocal or everythingnotlocal
##run clustalO (look up how)
##run fasttree (look up how)

#import BioGetAll
#BioGetAll.run() is UI for all of these function definitions. woot
