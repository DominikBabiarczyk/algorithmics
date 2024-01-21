1. Wprowadzenie

Problem dokładnego dopasowania dwóch grafów stanowi w istocie pytanie o to, czy są one względem siebie izomorficzne. Jest to specjalny przypadek problemu izomorfizmu podgrafu, który stanowi NP-zupełny problem decyzyjny określony w następujący sposób: dla danych grafów G i P sprawdzić, czy istnieje podgraf G izomorficzny z P.

Wyrażając to jeszcze inaczej - chodzi o to, aby jakiś podgraf G miał identyczną liczbę wierzchołków i układ krawędzi jak wzorzec P.
2. Cel ćwiczenia

implementacja algorytmu Ullmana do weryfikacji dopasowania dwóch grafów (izomorfizm podgrafów),

analiza wpływu dodanie pewnych heurystyk na sposób działania algorytmu,

zadanie dodatkowe - dopasowanie geometryczne grafów (przykładowa aplikacja w biometrii).


3.  Dopasowanie grafów (izomorficzne) - algorytm Ullmana

Izomorfizm grafu P i któregoś podgrafu grafu G możemy opisać w postaci macierzy M - |VP|x|VG|, gdzie każdy wiersz zawiera dokładnie jedną wartość 1, a każda kolumna co najwyżej jedną wartość 1. Ustawiamy mij jako 1, wtedy i tylko wtedy, gdy vj∈ G odpowiada vi∈ P. Wtedy P = M(MG)T, gdzie P i G oznaczają (tu) “klasyczne” macierze sąsiedztwa.

Podsumowując: jeśli spełnione jest wskazane równanie macierzowe P = M(MG)T to znaleźliśmy izomorfizm.

Idea algorytmu - systematycznie przeglądamy możliwe warianty M i sprawdzamy, czy opisują one izomorfizm.

  
Idee przyspieszające obliczenia (chcielibyśmy zamienić chociaż część  1 na 0 w M):
3.1. Macierz M0
Przyspieszenie algorytmu można uzyskać przez wykluczenie z góry przypadków, które na pewno nie dają izomorfizmu. Można stworzyć macierz (nazwijmy ją  M0), która zawiera 1 w miejscu (i,j), jeśli wierchołek vi  grafu P może odpowiadać wierzchołkowi vj grafu G w jakimś izomorfizmie. Zera odpowiadają przypadkom wykluczającym izomorfizm.

Przykładowo możemy rozważać stopień wierzchołka (deg) :

Czyli jeśli dany wierzchołek w G będzie miał mniej krawędzi niż odpowiadajacy mu wierzchołek w P, to na pewno nie będzie elementem izomorfizmu. Tworząc dodatkowe warunki możemy przyspieszyć obliczenia.
Wykorzystanie M0 polega  na sprawdzeniu, czy dany element c, który chcemy ustawić na 1, ma w M0 wartość 1. Oznacza to, że jest to dopuszczalna (zgodnie z warunkami początkowymi) konfiguracja.


3.2. Prune

Możemy wykorzystać prostą obserwację. Jeśli p ∈ VP ma sąsiadów należących do p1, ..., pl ∈ P i mapujemy go do pewnego wierzchołka g ∈ VG, to też powinniśmy móc zmapować  p1, ..., pl do sąsiadów g.
A więc jeżeli w macierzy M występuje 1 mówiąca, że p jest mapowany do g to trzeba sprawdzić czy istnieje sąsiad wierzchołka p, który nie jest zmapowany do żadnego sąsiada wierzchołka g. Jeżeli istnieje taki sąsiad to, to 1 w macierzy M jest niepoprawne i możemy je ustawić na 0.

Ta zmiana może uniemożliwić kolejne mapowania, zatem powinniśmy realizować iteracje dopóki nic się nie zmieni.
Jeśli w ten sposób usuniemy wszystkie 1 z całego wiersza to wiemy, że ta wersja M już nie opisze izomorfizmu


4. Implementacja/realizacja

używamy reprezentacji w postaci macierzy sąsiedztwa wykorzystując kod stworzony w ramach ćwiczenia "Klasyczne implementacje grafu",

jedyne co nam będzie potrzebne, oprócz standardowych funkcjonalności, to dostęp (pobranie) macierzy sąsiedztwa,

wczytujemy poniższe grafy (warto je sobie narysować). Proszę zadbać o to, aby macierz sąsiedztwa była symetryczna,


graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]


pobieramy z grafów macierze sąsiedztwa i konwertujemy je do postaci tablic numpy

tworzymy macierz numpy M o rozmiarze wynikającym z liczby wierzchołków grafów G i P

implementację zasadniczego algorytmu zacznijmy od napisania funkcji, która wygeneruje wszystkie możliwe warianty macierzy M. Jedno wywołanie tej funkcji generuje jedną jedynkę w jednym wierszu macierzy M. Funkcja jest rekurencyjna.
Będziemy potrzebowali listę używanych kolumn. Może to być np. tablica o rozmiarze równym liczbie kolumn macierzy M wypełniona początkowo wartościami False.
Pseudokod takiej funkcji:
ullman(aktualny_wiersz, macierz_M):
    jeżeli aktualny_wiersz == liczba_wierszy:
         wypisz M
         return
    dla każdej kolumny c:
         jeżeli kolumna c jest  nieużywana (czyli False w liście używanych):
              oznacz kolumnę c jako używaną
              wypełnij aktualny_wiersz macierzy_M zerami i wstaw 1 do c-tego elementu wiersza
              wywołaj rekurencyjnie ullman dla następnego wiersza
              oznacz kolumnę c jako nieużywaną

Sprawdź działanie funkcji dla małej macierzy (np. 2x3) - czy wypisuje ona wszystkie poprawne warianty M

Jeżeli wszystko działa poprawnie to rozbuduj funkcję o sprawdzanie izomorfizmu. Zamiast wypisywania macierzy M sprawdź czy podane poprzednio równanie macierzowe jest spełnione (będzie to wymagało przekazania do funkcji dodatkowych parametrów - macierzy sąsiedztwa sprawdzanych grafów). Jeżeli tak to dołącz znalezioną macierz M do listy poprawnych wariantów (izomorfizmów).

dodajemy zliczenie liczby wywołań rekurencji. Schemat:

no_recursion = ullman(......, no_recursion)

            no_recursion = no_recursion +1

            ….

            return no_recursion

sprawdzamy czy nasz kod działa i czy znajdujemy izomorfizmy,

    Poniżej, dla ułatwienia testowania, zamieszona została jedna z macierzy M, dla której powinni Państwo uzyskać izomorfizm (dla wierrzołków dodawanych alfabetycznie):
 [[0. 0. 0. 1. 0. 0.]                                                           
 [0. 0. 1. 0. 0. 0.]                                                            
 [0. 0. 0. 0. 1. 0.]]
    To samo, ale dla wierzchołków dodawanych razem z krawędziami: 
 [[0. 0. 0. 1. 0. 0.]
 [0. 0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 0. 1.]]

implementujemy wersję 2.0  uwzględniającą macierz M0. Tworzymy macierz M0 przed wywołaniem funkcji ullman i wykorzystujemy w tej funkcji do tego, aby wstawiać 1 w wierszu M  jeżeli o odpowiadającym miejscu  M0 też jest 1 (jak nie to bierzemy następną nieużywaną kolumnę). Sprawdzamy czy wynik działania funkcji ullman jest nadal poprawny oraz czy spadła liczba iteracji.

w wersji 3.0 dodajemy funkcję prune. Ma być  ona wołana przed pętlą w funkcji ullman. W dodatku musi ona być zawołana nie dla oryginalnej macierzy M ale dla jej kopii. Także operacje w pętli powinny operować na kopii macierzy M (czyli przed pętlą robimy kopię, przekazujemy ją do prune i w pętli zamieniamy odwołania do M na odwołania do jej kopii.

Pseudokod funkcji prune:

do
    for all (i,j) where M is 1:
          for all neighbours x of vi in P:
                 if there is no neighbour y of vj st. M(x,y)=1
                       M(i,j) =0

while M was changed

czyli:
Dla każdego elementu ‘1’ w M pobieramy listę sąsiadów P i G. Następnie sprawdzamy, czy każdy sąsiad P (oznaczony x) ma “jakiegoś” odpowiednika w G (oznaczony y), który jest uwzględniony w macierzy M tj. M(x,y) = 1. Jeśli taki nie występuje, to znaczy, że “wejściowe” wierzchołki i i j nie mogą stanowić elementu izomorfizmu (wtedy ustawiamy M[i,j] = 0).

Po wprowadzeniu funkcji prune do funkcji ullman sprawdzamy czy wynik działania funkcji ullman jest nadal poprawny oraz czy spadła liczba iteracji.


Program finalnie powinien jedynie wypisywać w trzech wierszach po parze liczb: liczbę znalezionych izomorfizmów oraz liczbę wywołań rekurencyjnych - te trzy wiersze mają zawierać wyniki algorytmu w wersji 1.0, 2.0 i 3.0


