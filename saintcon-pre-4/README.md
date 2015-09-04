# SAINTCON 2015 PRE-4

```
-- CIPHERTEXT --
AEBRVHWWMQHURVWFFIKVYFUCDG
To Decrypt this Message, you will need to learn how a US President encrypted messages while in Paris France.

The PSK sequence you need to know is:
5,24,4,20,23,2,11,22,19,15,10,18,16,1,14,3,25,9,6,12,26,7,13,17,21,8
```

## Solve

Began with the obvious of throwing the ciphertext into [quipquip](http://www.quipquip.com) for easy pickings, no dice. Actually opened up the pdf to see a 2x2 grid of letters and then a circle at the bottom the size of a paper towel roll. 

![2x2 grid](tumblers.png)

This immediately sparked the memory of the Da Vinci Code cryptex. 

![Cryptex](http://www.google.com/imgres?imgurl=http://farm1.static.flickr.com/44/151655818_75f56d721d.jpg&imgrefurl=http://www.photoree.com/topic/gallery/cryptex/1&h=318&w=500&tbnid=_EUISJpJGfJ2tM:&docid=Ce3ANWyj37N7yM&ei=6pbpVcn0K4-dyASRuoH4Dw&tbm=isch&ved=0CD0QMygLMAtqFQoTCMmRvNi43ccCFY8OkgodEV0A_w)

I began doing some awkward transformations of shifting each letter in the cipher text a number in the PSK:

```
A >> 5
E >> 24
B >> 4
R >> 20
... ect
```

Realizing this was a terrible idea, went back to the PDF to realize that there are numbers at the top of the 2x2 grid. It then became obvious that the PSK given is the order of the tumblers needed to solve the ciphertext.

The solution script does the following:
* Extracts each individual tumbler
* Arranges the tumblers in order based on the PSK
* Rotates each tumbler to match the ciphertext
* Prints every resulting line

Upon execution, we are given the following result:

```
AEBRVHWWMQHURVWFFIKVYFUCDG
XCDSNUMEXWPMMLNGHMNXOYGVET
KXVDCRBLWOURKYSBVPDJAMFBUW
MJZZIICYVMDNHTYMZXUDIIZFHK
BQNMFJJJSUJFYFPQKYOYTNWJKB
SBFTPZVDUHWLGUJYQEQWEWIONA
PFXQTQPXBCFQEWLSTSYOQSSRVL
HTTPHCSAINTCONORGJEFFERSON <--- Looks like a web page
IVKHZKAUGJNIIMFPMTRBDHTIPV
TMQUXWZOEDGBXCGUWQPEBBMNAD
OYUWSYENFLIJNJKTCBZAPJAZRE
GAEXRPRKHKMHQDXDRAJTSOXXQX
WKPKOXDCDVVPDKCOPDLRCPPYSP
RLHGWVLFAIEVJZILSZWPXVHMXI
FHSVQMKQKYOWVPQAJOTCVQDPBS
LZYOAEOVNRQYBBDZDRXNRKBAFM
UDLAKSURJPADLSBXLUBQLZCUYF
YUICLLGSPFKGTGUNBGSUJAVQGO
NPMIGTYTOTBKFETKYVILUUEWMQ
EIOEUNNMZGZZWRMVAKCINDYLCH
DGAJJDTHLSXSAXVJOFFZMTKHIY
JOGLEGQIRAYOCAECNHHSZGODJJ
ZNWFBBFPCXCTSQZHECVGKCQTLZ
VSRBMAHGQZSAZIHEILAHWRJGWC
CWJYDOIZYBLEPHAWUNMMHXLETR
QRCNYFXBTERXUORIXWGKGLNKZU
```

Checking out the website:

```
PROVE YOU SOLVED IT!
DM TWEET @SAINTCON: The Ciphertext three positions below the Plaintext
If you hate Twitter, an email to tj@saintcon.org will work too.

SOLVED BY: NOBODY YET
```

I don't think I was the first, but it was a great challenge nonetheless! Thanks to @saintcon for the pre-challenge and looking forward to more puzzles in the future.
