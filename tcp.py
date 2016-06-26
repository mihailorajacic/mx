import  argparse, socket

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Slusam na: ', sock.getsockname())
    while True:
        print('Cekam na novu konekciju')
        sc, sockname = sock.accept()
        print('Prihvatio sam konekciju od: ', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        message = sc.recvfrom(1024)
        print('  Dolazna poruka je:', repr(message), "i njena duzina je: " , len(message) )
        sc.sendall(b'Dovidjenja klijent! ')
        sc.close()
        print('  Odgovor je poslat i soket je zatvoren')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Klijentu je dodeljeno soket ime: ', sock.getsockname())
    poruka=47*'a'
    duzina=len(poruka)

    maksVel=15
    brojPoruka=duzina//maksVel+1
    print("Broj poruka je: " , brojPoruka)
    for i in (0,brojPoruka-1):
        poruka1=poruka[i*maksVel:(i+1)*maksVel]
        print(poruka1)
        b = bytearray()
        b.extend(map(ord, poruka1))
        sock.sendto(b, (host, port))

    reply = sock.recv(1024)
    print('Server kaze: ', repr(reply))
    sock.close()

if __name__ == '__main__':
    choices = {'klijent': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)