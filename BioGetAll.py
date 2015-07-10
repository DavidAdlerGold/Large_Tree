def run():
    #interface to run shorten/pfam/vet sequences
    import VetFastaWithPfam
    type(VetFastaWithPfam)
    a = raw_input("Would you like to Vet a Fasta file through Pfam? y?")
    if a == "y":
        print("Don't try to use local if you aren't on the computer named Lancel")
        b = raw_input("Type \"local\" to use local install of Pfam, \"server\" to use the online server, or \"no\" to see more options")
        if b == "server":
            d = raw_input("What is the input .fasta file called?")
            e = raw_input("How many sequences per split file?")
            f = raw_input("What is the first domain to vet for?")
            g = raw_input("What is the second domain to vet for?")
            h = raw_input("What is the directory that the .fasta is in? (Should be /home/abigail/Documents etc")
            ans = VetFastaWithPfam.everythingnotlocal(d,e,f,g,h)
        elif b == "local":
            d = raw_input("What is the input .fasta file called?")
            f = raw_input("What is the first domain to vet for?")
            g = raw_input("What is the second domain to vet for?")
            h = raw_input("What is the directory that the .fasta is in? (Should be /home/abigail/Documents etc")
            ans = VetFastaWithPfam.everythinglocal(d,f,g,h)
        else:
            print ("More options: ")
            c = raw_input("Do you want to run CombVet? y/n?")
            if c == "y":
                d = raw_input("What is the input .fasta file called?")
                print("your pfam file should be saved like name#Pfam.fasta")
                e = raw_input("What is the pfam file called, without the number?")
                f = raw_input("What is the first domain to vet for?")
                g = raw_input("What is the second domain to vet for?")
                h = raw_input("What is the directory that the .fasta is in? (Should be /home/abigail/Documents etc")
                ans = VetFastaWithPfam.CombVet(d, e, f, g, h)
            else:
                print("Ok, quitting")
                quit()

    print("ok, moving on")
                          
    aa = raw_input("Would you like to run clustalO (default settings)? y?")
    if aa == "y":
        import os
        if a == "y":
            bb = raw_input("Would you like to run the Vetted file you just made? y?")
            if bb == "y":
                cc = h
                dd = raw_input("What should the output file be called? (give only name.fasta)")
                os.system("clustalo -i "+ans+" -o "+cc+"/"+dd+" -v")
                print("Should have exported clustalo alignment to "+dd)
        else:
            print ("OK. When inputing file name, please provide the whole directory/name.fasta")
            ee = raw_input("What is the input .fasta file called? Give /dir/etc/name.fasta" )
            cc = raw_input("What directory should I put the output file in?")
            dd = raw_input("What should the output file be called?")
            os.system("clustalo -i "+ee+" -o "+cc+"/"+dd+" -v")
            print("Should have exported clustalo alignment to "+cc+"/"+dd)
    else:
        print("Ok, not using clustalo")

    aaa=raw_input("Would you like to run fasttree (default settings)? y?")
    if aaa == "y":         
        import os
        if aa == "y":
            ccc = raw_input("Would you like to run fasttree on the file you just aligned? y?")
            if ccc == "y":
                loloops = raw_input("Do you have unallowed characters ( []():,'. ) in your sequence IDs? (if you just made it now, type \"y\")?")
                if loloops == "y":
                    orig = open(cc+"/"+dd)
                    import re
                    newfile = cc+"/"+dd[:-6]+"Edited.fasta"
                    with open(newfile) as new:
                        for line in orig:
                            if "gi:" in line:
                                edit = re.sub ("[\[\]:,'.()]", "", line)
                                new.write(edit)
                            else:
                                new.write(line)
                    os.system("fasttree "+newfile+" > "+dd+"Tree.newick")
                    print("Ok, your tree is now at "+dd+"Tree.newick")
                    print("Please use a tree-viewing program to open it!")
                else:
                    os.system("fasttree "+dd+" > "+dd+"Tree.newick")
                    print("Ok, your tree is now at "+dd+"Tree.newick")
                    print("Please use a tree-viewing program to open it!")
        else:
            place = raw_input("What file should we use? (include /dir/file.fasta) ")
            loloops = raw_input("Do you have unallowed characters ( []():,'. ) in your sequence IDs? (if you just made it now, type \"y\")?")
            if loloops == "y":
                import re
                orig = open(place)
                newfile = place[:-6]+"Edited.fasta"
                with open(newfile, "w") as new:
                    for line in orig:
                        if "gi:" in line:
                            edit = re.sub ("[\[\]:,'.()]", "", line)
                            new.write(edit)
                        else:
                            new.write(line)
                print("Created file without unallowed characters at "+newfile)
                print("Going to run: fasttree "+newfile+" > "+place[:-6]+"Tree.newick")
                os.system("fasttree "+newfile+" > "+place[:-6]+"Tree.newick")
                print("Ok, your tree is now at "+place[:-6]+"Tree.newick")
                print("Please use a tree-viewing program to open it!")
            else: 
                os.system("fasttree "+place+" > "+place[:-6]+"Tree.newick")
                print("Ok, your tree is now at "+place[:-6]+"Tree.newick")
                print("Please use a tree-viewing program to open it!")
    else:
        print("Ok, not making a tree. Bye!")
