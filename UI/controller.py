

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = None
        self._stato = None

    def handleCalcola(self, e):
        errore = False
        try:
            self._anno = int(self._view._txtAnno.value)
        except ValueError:
            self._view.create_alert("Inserire un anno valido")
            errore = True

        if not errore and (self._anno<1816 or self._anno>2016):
            self._view.create_alert("L'anno deve essere compreso tra 1816 e 2016")
            errore = True

        if not errore:
            self._view._txt_result.controls.clear()
            numCC,dizio = self._model.addEdgeGraphYear(self._anno)
            self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
            self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {numCC} componenti connesse"))
            self._view._txt_result.controls.append(ft.Text("Di seguito dettaglio sui nodi:"))
            for key,val in dizio.items():
                self._view._txt_result.controls.append(ft.Text(f"{key.StateNme} -- {val}"))
            self.contry=sorted(self._model._grafo.nodes)
            for c in self.contry:
                self._view._ddStato.options.append(ft.dropdown.Option(text=c.StateNme,
                                                                      data=c,
                                                                      on_click=self.readStato))
            self._view._ddStato.disabled=False
            self._view._btnCalcolaRaggiungibili.disabled = False
            self._view.update_page()

    def handleRaggiungibili(self,e):
        self._view._txt_result.controls.clear()
        n = self._model.cercaRaggiungibili(self._stato)
        self._view._txt_result.controls.append(ft.Text(f"Da {self._stato} sono raggiungibili {len(n)} stati"))
        for i in n:
            self._view._txt_result.controls.append(ft.Text(f"{i}"))
        self._view.update_page()


    def readStato(self,e):
        if e.control.data is None:
            self._stato = None
        else:
            self._stato = e.control.data
        print(self._stato)




