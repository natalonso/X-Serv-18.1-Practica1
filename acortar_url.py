#!/usr/bin/python3

import webapp

dic_url = {

}

formulario = """
    <form action="" method="POST">
    Servidor de url:<br>
    <input type="text" name="Introduce una url:" value="google.es"><br>
    <input type="submit" value="Enviar">
    </form>"""

class contentApp(webapp.webApp):

    def parse(self,request):
        #ultimo elemento del split se referencia con -1, si añado un uno quiere decir que hago el split solo una vez

        if len(request) > 0:
            metodo = request.split()[0]
            recurso = request.split()[1]
            peticion = request
            return (metodo, recurso, peticion)

        else:
            metodo = 0
            recurso = 0
            peticion = 0
            return (metodo, recurso, peticion)

    def process(self, parsedRequest): #parsedRequest es una tupla(metodo,recurso, peticion)

        metodo, recurso, peticion = parsedRequest
        if (metodo == 0 and recurso == 0 and peticion == 0):
            return ("200 OK", "<html>ente fantasma!!!!</html>")

        print("CONTENIDO DEL DICCIONARIO HASTA EL MOMENTO: " + str(dic_url))

        if metodo == "POST":
            cuerpo = peticion.split('\r\n\r\n', 1)[1].split('=')[1]
            if len(cuerpo) == 0: #no hay query string, mando mensaje de ERROR
                return ("200 OK", "<html>DEBE RELLENAR EL CAMPO" + formulario +
                        "CONTENIDO DEL DICCIONARIO HASTA EL MOMENTO: " + str(dic_url) + "</html>")
            else: #hay qs por tanto envio un html con dos ENLACES


                for clave,valor in dic_url.items():

                    if cuerpo == valor:
                        return ("200 OK", "<html><body><h1>URL ORIGINAL y URL ACORTADA: <br> URL ORIGINAL: " +
                            "<a href='https://" + str(cuerpo) + "'>"+ str(cuerpo)+ "</a><br> URL ACORTADA: " +
                            "<a href='https://" + str(cuerpo) + "'>"+ str(clave)+ "</a></h1></body></html>")

                self.contador = self.contador + 1
                dic_url[self.contador] = cuerpo
                #GUARDO LA NUEVA URL EN EL DICCIONARIO Y EN EL ARCHIVO SI NO ESTABA YA
                diccionario = open('/home/alumnos/nalonso/Documentos/saro/X-Serv-18.1-Practica1/diccionario.txt',
                                    mode='a', encoding='utf-8')
                diccionario.write(str(self.contador) + ":" + str(cuerpo) + "\n")
                diccionario.close()

                return ("200 OK", "<html><body><h1>URL ORIGINAL y URL ACORTADA: <br> URL ORIGINAL: " +
                        "<a href='https://" + str(cuerpo) + "'>"+ str(cuerpo)+ "</a><br> URL ACORTADA: " +
                        "<a href='https://" + str(cuerpo) + "'>"+ str(self.contador)+ "</a></h1></body></html>")

        elif metodo == "GET":
            if recurso == "/":
                return ("200 OK", "<html>Resource not found yet!<br>" + formulario +
                        "CONTENIDO DEL DICCIONARIO HASTA EL MOMENTO: " + str(dic_url) + "</html>")
            elif recurso == "/favicon.ico":
                return ("200 OK", "<html>NOT FOUND</html>")
            else:
                url = recurso.split("/")[1]
                try:
                    redireccion = dic_url[int(url)]
                    return ("200 OK","<html>REDIRECCIONO<meta http-equiv="+'refresh'+ " content="+'1'+";url=" + 'https://'
                            + str(redireccion) +"/></html>")
                except ValueError:
                    return ("200 OK", "<html>RECURSO NO ENCONTRADO</html>")
                except KeyError:
                    return ("200 OK", "<html>RECURSO NO ENCONTRADO</html>")
        else:
                return ("200 OK", "<html>RECURSO NO VALIDO</html>")

    def __init__(self, hostname, port):

        self.contador = -1
        diccionario = open('/home/alumnos/nalonso/Documentos/saro/X-Serv-18.1-Practica1/diccionario.txt',
                            mode='r', encoding='utf-8')

        for url in diccionario.readlines():
            self.contador = self.contador + 1
            print("VALOR DEL CONTADOR: " + str(self.contador))
            print("LA LINEA ES: " + str(url))

            dic_url[self.contador] = url.split(":")[1].split("\n")[0]
            diccionario.close()
        super().__init__(hostname, port)

if __name__ == "__main__":
    testWebApp = contentApp("localhost", 4567)
