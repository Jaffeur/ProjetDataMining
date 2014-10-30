with open("Produits_Monoprix_RIDE.txt", "a") as f_w:


    for i in range(len(rayons_5)):
        line = rayons_5[i]
        line.rstrip()
        print line
        f_w.write(line.encode('utf-8') + "\n")

f_w.close
