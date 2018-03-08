#!/usr/bin/python3

import webapp

dic_url = {
}
contador = -1

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
        global contador
        metodo, recurso, peticion = parsedRequest
        if (metodo == 0 and recurso == 0 and peticion == 0):
            return ("200 OK", "<html>ente fantasma!!!!</html>")


        if metodo == "POST":
            cuerpo = peticion.split('\r\n\r\n', 1)[1].split('=')[1]

            if len(cuerpo) == 0: #no hay query stringo, mando mensaje de ERROR
                return ("200 OK", "<html>DEBE RELLENAR EL CAMPO" + formulario +  "CONTENIDO DEL DICCIONARIO HASTA EL MOMENTO: " + str(dic_url) + "</html>")

            else: #hay qs por tanto envio un html con dos ENLACES
                contador = contador + 1
                dic_url[contador] = cuerpo
                return ("200 OK", "<html><body><h1>URL ORIGINAL y URL ACORTADA: <br> URL ORIGINAL: " +
                "<a href='https://" + str(cuerpo) + "'>"+ str(cuerpo)+ "</a><br> URL ACORTADA: " +
                "<a href='https://" + str(cuerpo) + "'>"+ str(contador)+ "</a></h1></body></html>")
        else:  #metodo == "GET":
            if recurso == "/":
                return ("200 OK", "<html>Resource not found yet!<br>" + formulario +  "CONTENIDO DEL DICCIONARIO HASTA EL MOMENTO: " + str(dic_url) + "</html>")
            elif recurso == "/favicon.ico":
                return ("200 OK", "<html>NOT FOUND</html>")
            else:
                url = recurso.split("/")[1]
                try:
                    redireccion = dic_url[int(url)]
                    return ("200 OK","<html>REDIRECCIONO<meta http-equiv="+'refresh'+ " content="+'1'+";url=" + 'https://' + str(redireccion) +"/></html>")
                except ValueError:
                    return ("200 OK", "<html>RECURSO NO ENCONTRADO</html>")
                except KeyError:
                    return ("200 OK", "<html>RECURSO NO ENCONTRADO</html>")


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 4567)
