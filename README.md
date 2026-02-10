#Reffery (pracovní název hry)
#Základní idea
Strategy hra, hráč si vytvoří stranu a vede stát. Dělá ekonomická rozhodnutí (může svou zemi zbankrotovat) či diplomatická rozhodnutí (může svou zemi mezinárodně zničit). Cílem je vydržet ve vládě 4 roky a vyhrát následující volby. 

#Implementace
Hráč na začátku hry “postaví” svou stranu - z názorů, ekonomických priorit. Algoritmus spočítá, kolik by taková strana dostala hlasů a degeneruje ostatní strany. Hráč postupuje po skriptované dějové lince doplněné o různé eventy (ty se vytvoří na bázi počátečního inputu a následujících kroků). Každá hra je jiná - podle toho co hráč na začátku nakliká se mění celé dějství hry.  

#Interface 
Obrazovka rozdělena na 3 zóny - hlavní (zde všechny formuláře, tlačítka, posuvníky apod. + popis aktuálnímu dění), informační (zde se hráč dozvídá o důsledcích jeho kroků, forma světového zpravodajství), mapa (mapa státu, ve kterém se odehrává hra, pro zvětšení estetického dojmu a prohloubení zážitku ze hry, možnost ji rozkliknout a ukázat větší mapu kontinentu - zde zvýraznění přátelé a nepřátele a jejich názor k tvému státu). // ukázka cca grafického rozhraní (spíš myšlenka grafického rozhraní)

#Knihovny
pygame
