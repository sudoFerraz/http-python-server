ó
7«ùWc           @   s5  d  Z  d d l Z d d l Z d d l Z d d l Z d d l Z d Z d Z d Z d Z	 d Z
 e Z d   Z d	   Z d
   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d d d     YZ d d d     YZ e d  Z  d S(    s  HTTP server with file tree Sistemas Distribuidos 2016-2 UFU.

 ____   ____  _________________  _________________      _____
|    | |    |/                 \/                 \ ___|\    |    | |    |\______     ______/\______     ______/|    |\    |    |_|    |   \( /    /  )/      \( /    /  )/   |    | |    |
|    .-.    |    ' |   |   '        ' |   |   '    |    |/____/|
|    | |    |      |   |              |   |        |    ||    ||
|    | |    |     /   //             /   //        |    ||____|/
|____| |____|    /___//             /___//         |____|
|    | |    |   |`   |             |`   |          |    |
|____| |____|   |____|             |____|          |____|
  \(     )/       \(                 \(              \(
   '     '         '                  '               '
iÿÿÿÿNt   GETt   PUTt   POSTt   DELETEt   HEADc          C   s   d }  t  t j d  } t j t j t j  } | j t j t j d  | j	 |  | f  d | GHd GH| j
 d  x t |  q{ Wd S(   s   Funcao principal para conexao.t    i   s   Servidor rodando na porta %ds   Aguardando conexaoi
   N(   t   intt   syst   argvt   sockett   AF_INETt   SOCK_STREAMt
   setsockoptt
   SOL_SOCKETt   SO_REUSEADDRt   bindt   listent   Conexao(   t   hostt   portt   s(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   main    s    	c         C   s    d t  |  GHd } d } x, | |  j d  7} | GH| | k r Pq q Wt |  \ } } } | GH| GH| GHt | | |  } |  j |  | GH|  j   d S(   s-   Abrindo conexao com cliente quando conectado.s   Conectado com o cliente %ss   

R   i   N(   t   strt   recvt   Parsingt   metodo_handlert   sendt   close(   t   sockclientet   addrclientet   ct   messaget   metodot   caminhoSplitadot   corpot	   resultado(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR   2   s     c         C   sÆ   |  t  k r( t |  } t |  } | S|  t k rG t | |  } | S|  t k rr t |  } t | |  } | S|  t k r t |  } t |  } | S|  t	 k rÂ t |  } t
 |  } | Sd S(   s<   Definindo qual metodo e qual handler usar, retorna mensagem.N(   t   gett   acha_objetot   Get_Handlert   postt   Post_Handlert   putt   Put_Handlert   deletet   Delete_Handlert   headert   Header_Handler(   R    t   caminhoR"   t   objetot   resposta(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR   J   s&    c         C   sN  t  } t |   d k r, |  d d k r, t  S|  d d k rxM t d t t  j  d  D]0 } |  d t  j | j k rX t  j | } qX qX Wxs t d t |   d  D]V } xM t d t | j  d  D]0 } |  | | j | j k rÇ | j | } qÇ qÇ Wq¥ Wn  |  t |   d | j k r)d } d S|  t |   d | j k rJ| Sd S(   s+   Procura o objeto no qual o caminho termina.i   i    R   N(   t   roott   lent   ranget   filhost   nomet   None(   R/   t   nodot   it   j(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR%   b   s     """c         C   sx   |  j  d  } |  j  d  } | d } | d j  d  } | d j  d  } | d j  d  } | d } | | | f S(   sB   Faz parsing e separa uma lista para o metodo e caminhos splitados.s   
s   

i   i    s    HTTPs    /t   /(   t   split(   R   t   linhast   datat   linhas2t   linhas3R/   R    (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR   v   s    

c         C   s   |  j  d d  }  |  S(   s   Coloca mensagem em plaintext.s   
t    (   t   replace(   t   mensagem(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   traduz   s    c         C   sõ   d t  |   d } d t  | j  d d t  | j  d d t  | j  d } |  t k rn | | 7} n  | j d
 k r d | _ n  d t  t | j   } d	 t  | j  } |  t k rÎ | | 7} n  |  t	 k rñ | | 7} | | 7} n  | S(   s   Definindo a mensagem 200 OK.s	   HTTP/1.1 s    200 OK
s	   Version: s   
s
   Creation: s   Modification: R7   s   Content_Length: s   

N(
   R   t   versiont   createdt   modifiedR+   R>   R7   R3   R-   R$   (   R    R0   t   msgt   msg2R"   t   dados(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt	   msg200_OK   s    A
c         C   s^   d } |  t  k rZ | d t | j  d d t | j  d d t | j  d 7} n  | S(   s,   Definindo mensagem de acesso nao autorizado.s   HTTP/1.1 403 Forbiddens
   
Version: s   
s
   Creation: s   Modification: (   R'   R   RE   RF   RG   (   R    R0   RH   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   msg403_Forbidden   s
    Ec          C   s
   d }  |  S(   s    Definindo mensagem 201, Created.sÇ   HTTP/1.1 201 Created
Content-Type: text/html
Connection: Closed


        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>201 Created</title>
        </head><body>
        </body></html>(    (   RH   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   msg201_Created¦   s    c          C   s
   d }  |  S(   s   Definindo mensagem 204.sÍ   HTTP/1.1 204 No content
Content-Type: text/html
Connection: Closed


        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>204 No content</title>
        </head><body>
        </body></html>(    (   RH   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   msg_204NoContent±   s    c          C   s
   d }  |  S(   s   Definindo mensagem 400.s   HTTP/1.1 400 Bad request(    (   RH   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   msg_400BadRequest¼   s    c          C   s
   d }  |  S(   s   Definindo mensagem.s   HTTP/1.1 404 Not Found(    (   RH   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   msg_404NotFoundÂ   s    c         C   s+   |  d k r t   } n t t |   } | S(   s   Manejamento do GET.N(   R7   RP   RK   R$   (   R0   RC   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR&   È   s    c         C   s  t  } t |   d k r5 |  d d k r5 t   } | S|  d d k rß x t d t |   d  D]z } xN t d t | j  d  D]1 } |  | | j | j k r | j | } Pq q W| } |  | | j k r^ | } Pq^ q^ Wn  |  | | j k rt t |  } | St |  |  } | j	 |  | }	 xG t | d t |   d  D]) }
 t |  |
  } |	 j	 |  | }	 qEW| |	 _
 t t |  } | S(   s   Manejamento do POST(cria).i   i    R   (   R2   R3   RO   R4   R5   R6   RL   R'   t
   Fileservert   insereR>   RK   (   R/   RJ   R8   R   R9   R:   t   posRH   t   novonodot   ptnodot   k(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR(   Ò   s6    "	"#
	c         C   s;   |  d k r t t |   } n |  j   t t |   } | S(   s   Manejamento do DELETE.N(   R7   RL   R+   t
   remove_arqRK   (   R0   RC   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR,   ö   s
    
c         C   sI   |  d k r t t |   } n' | |  _ |  j d 7_ t t |   } | S(   s#   Manejamento do PUT(modifica dados).i   N(   R7   RL   R)   R>   RE   RK   (   R0   RJ   RC   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR*      s    	c         C   s+   |  d k r t   } n t t |   } | S(   s   Manejamento do Header.N(   R7   RP   RK   R-   (   R0   RC   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR.     s    t   controle_globalc           B   s   e  Z d  Z d   Z RS(   s'   Lista com todos os arquivos ja criados.c         C   s   g  |  _  d S(   s   Inicializa a lista global.N(   t   criados(   t   selfR6   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   __init__  s    (   t   __name__t
   __module__t   __doc__R[   (    (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyRX     s   RQ   c           B   sM   e  Z d  Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z	 RS(   s,   Definindo estrutura do servidor de arquivos.c         C   sm   | |  _  g  |  _ g  |  _ d |  _ d |  _ d |  _ t t j    |  _	 t t j    |  _
 d |  _ d S(   s5   Inicializando um arquivo na arvore(diretorio tambem).R   i    N(   R6   R5   t
   nomefilhosR7   R>   t   pait   nomepaiR   t   timeRF   RG   RE   (   RZ   R6   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyR[     s    						c         C   s0   |  j  j |  |  j j | j  |  | _ d S(   s)   Inserir na lista de arquivos subjacentes.N(   R5   t   appendR_   R6   R`   (   RZ   t   filho(    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyRR   +  s    c         C   s'   | j  j |   | j j |  j  d S(   s    Insere arquivo dentro de um pai.N(   R5   Rc   R_   R6   (   RZ   R`   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   insere_dentro1  s    c         C   s"   | |  _  t t j    |  _ d S(   s"   Insere dados dentro de um arquivo.N(   R>   R   Rb   RG   (   RZ   R>   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   insere_dados6  s    	c         C   sR   |  j  j | j   |  j  j |  |  j j | j  t t j    |  _ ~ d S(   s   Remove um arquivo do diretorio.N(   R5   t   extendt   removeR_   R6   R   Rb   RG   (   RZ   Rd   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   remove_filho;  s
    c         C   s^   |  j  j j |  j  |  j  j j |   |  j  j j |  j  t t j    |  j  _ ~  d S(   s#   Remove o proprio arquivo que chama.N(	   R`   R5   Rg   Rh   R_   R6   R   Rb   RG   (   RZ   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyRW   C  s
    c         C   s   |  j  S(   s&   Devolve os dados guardados no arquivo.(   R>   (   RZ   (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt	   get_dadosK  s    (
   R\   R]   R^   R[   RR   Re   Rf   Ri   RW   Rj   (    (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyRQ     s   						R;   (    (    (!   R^   R	   R   Rb   t   stringt   reR$   R)   R'   R+   R-   t   typet   __metaclass__R   R   R   R%   R   RD   RK   RL   RM   RN   RO   RP   R&   R(   R,   R*   R.   RX   RQ   R2   (    (    (    s5   /home/rh1n0/projects/http-python-server/httpserver.pyt   <module>   s>   								
					
	$	
			3