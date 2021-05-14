# Diegimas

1. Atsisiunčiame **VirtualBox** programą iš [čia](https://www.virtualbox.org/wiki/Downloads). Būtina, jeigu Windows 10 Home. Sudiegiame, visą laiką spausdami next.
2. Atsisiųskime **Multipass** iš [čia](https://multipass.run/).
3. Per Microsoft Store susidiekime **Windows Terminal** (nebūtina, bet patogiau).

# Multipass

Multipass yra Canonical sukurtas įrankis greitai ir paprastai kurti Ubuntu Server virtualias mašinas Windows, Linux ir Mac kompiuteriuose. 

Patikrinkime, kokias turime tinklo sąsajas:

```bash
PS C:\Users\jotau> multipass networks
Name      Type      Description
Ethernet  ethernet  Realtek PCIe GbE Family Controller
```

Sukurkime virtualią mašiną, nurodę, kokią tinklo sąsają naudoti:
```bash
multipass launch --network Ethernet
```

Patikrinkime vitrualiųjų mašinų sąrašą:

```bash
PS C:\Users\jotau> multipass list
Name                    State             IPv4             Image
tight-dane              Running           192.168.1.132    Ubuntu 20.04 LTS
```

Prisijunkime prie mūsų virtualios mašinos:

```
multipass shell tight-dane
```

atsidarykime SSH konfigūracijų failą:
```
sudo nano /etc/ssh/sshd_config
```

klaviatūros rodyklių pagalba skrolinkime žemyn, iki surasime eilutę **PasswordAuthentication no**. Pakeiskime no į yes ir išsaugokime (CTRL+O -> Enter), išeikime iš redaktoriaus (CTRL+X -> Enter). Perkraukime SSH serverį:

```
sudo systemctl restart ssh
```

sukurkime vartotoją:

```
ubuntu@tight-dane:~$ sudo adduser jt
Adding user `jt' ...
Adding new group `jt' (1001) ...
Adding new user `jt' (1001) with group `jt' ...
Creating home directory `/home/jt' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for jt
Enter the new value, or press ENTER for the default
        Full Name []: jotautas
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] y
```
Pridėkime sukurtą vartotoją prie sudo grupės:
```
ubuntu@tight-dane:~$ sudo adduser jt sudo
Adding user `jt' to group `sudo' ...
Adding user jt to group sudo
Done.
ubuntu@tight-dane:~$
```

su ctrl+d atsijunkime nuo VM'o. Pabandykime iš windows powershell prisijungti per ssh:

```
PS C:\Users\jotau> ssh jt@192.168.1.132
The authenticity of host '192.168.1.132 (192.168.1.132)' can't be established.
ECDSA key fingerprint is SHA256:aX/uNK7alVpT/QknsrHsYaqKMg8Kg0TGsUd9cxkn8ag.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.132' (ECDSA) to the list of known hosts.
jt@192.168.1.132's password:
```

Dabar turime sistemą labai panašią į tokią, kokią turėtumėm išsinuomavę Ubuntu serverį iš hostingo paslaugų tiekėjo.

TODO: Kitos naudingos Multipass funkcijos - start, stop, info, delete, purge. 



