import wx
from zuev_g.lab1 import *

CONN_STR = "host='localhost' dbname='postgres' user='postgres' password='postgres'"
# CONN_STR = "host='10.22.31.252' dbname='rpr' user='zuev_g' password='efb3de92'"


# --- GUI ---

class TourApp(wx.App):
    def OnInit(self):
        frame = TourFrame(None, title="Управление турами")
        self.SetTopWindow(frame)
        frame.Show()
        return True


class TourFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(TourFrame, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Кнопки
        btn_tour_info = wx.Button(panel, label="Информация о туре")
        btn_hotels = wx.Button(panel, label="Отели с 5 звездами")
        btn_pricelist = wx.Button(panel, label="Прайс-лист на дату")
        btn_hotel_data = wx.Button(panel, label="Данные об отеле по id")
        btn_add_tour = wx.Button(panel, label="Добавить тур")
        btn_delete_tour = wx.Button(panel, label="Удалить тур")
        btn_change_transport = wx.Button(panel, label="Изменить транспорт тура")
        btn_search_tours = wx.Button(panel, label="Поиск туров")

        # Привязка событий к кнопкам
        btn_tour_info.Bind(wx.EVT_BUTTON, self.OnTourInfo)
        btn_hotels.Bind(wx.EVT_BUTTON, self.OnFiveStarHotels)
        btn_pricelist.Bind(wx.EVT_BUTTON, self.OnPricelist)
        btn_hotel_data.Bind(wx.EVT_BUTTON, self.OnHotelData)
        btn_add_tour.Bind(wx.EVT_BUTTON, self.OnAddTour)
        btn_delete_tour.Bind(wx.EVT_BUTTON, self.OnDeleteTour)
        btn_change_transport.Bind(wx.EVT_BUTTON, self.OnChangeTransport)
        btn_search_tours.Bind(wx.EVT_BUTTON, self.OnSearchTours)

        # Добавление кнопок в вертикальный layout
        vbox.Add(btn_tour_info, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_hotels, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_pricelist, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_hotel_data, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_add_tour, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_delete_tour, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_change_transport, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btn_search_tours, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)
        self.SetSize((300, 400))
        self.Centre()

    def OnTourInfo(self, event):
        dlg = wx.TextEntryDialog(self, "Введите ID тура:")
        if dlg.ShowModal() == wx.ID_OK:
            tour_id = dlg.GetValue()
            try:
                tour_id = int(tour_id)
                tour_info = get_tour_info(tour_id)
                if tour_info:
                    wx.MessageBox(f"Название: {tour_info[0]}\nТип: {tour_info[1]}", "Информация о туре",
                                  wx.OK)
                else:
                    wx.MessageBox("Тур не найден.", "Информация о туре", wx.OK)
            except ValueError:
                wx.MessageBox("Неверный ID тура. Введите число.", "Ошибка", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def OnFiveStarHotels(self, event):
        hotels = get_five_star_hotels()
        if hotels:
            hotel_list = "\n".join([f"{h[1]} ({h[2]} звезд)" for h in hotels])
            wx.MessageBox(hotel_list, "Отели с 5 звездами", wx.OK)
        else:
            wx.MessageBox("Отели не найдены.", "Отели с 5 звездами", wx.OK)

    def OnPricelist(self, event):
        dlg = wx.TextEntryDialog(self, "Введите дату в формате YYYY-MM-DD:")
        if dlg.ShowModal() == wx.ID_OK:
            date_str = dlg.GetValue()
            pricelist = get_pricelist_on_date(date_str)
            if pricelist:
                pricelist_str = "\n".join([f"Тур: {p[0]}, Цена: {str(p[1])}" for p in [pricelist]])
                wx.MessageBox(pricelist_str, "Прайс-лист", wx.OK)
            else:
                wx.MessageBox("Прайс-лист не найден на эту дату.", "Прайс-лист", wx.OK)
        dlg.Destroy()

    def OnHotelData(self, event):
        dlg = wx.TextEntryDialog(self, "Введите id:")
        if dlg.ShowModal() == wx.ID_OK:
            date_str = dlg.GetValue()
            data = hotel_data(date_str)
            if data:
                wx.MessageBox(str(data[0]), "Данные об отеле", wx.OK)
            else:
                wx.MessageBox("Данные не найдены.", "Данные об отеле", wx.OK)
        dlg.Destroy()

    def OnAddTour(self, event):
        dlg = AddTourDialog(self, title="Добавить новый тур")
        dlg.ShowModal()
        dlg.Destroy()

    def OnDeleteTour(self, event):
        dlg = wx.TextEntryDialog(self, "Введите ID тура для удаления:")
        if dlg.ShowModal() == wx.ID_OK:
            tour_id = dlg.GetValue()
            try:
                tour_id = int(tour_id)
                delete_tour(tour_id)
            except ValueError:
                wx.MessageBox("Неверный ID тура. Введите число.", "Ошибка", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def OnChangeTransport(self, event):
        dlg = ChangeTransportDialog(self, title="Изменить транспорт тура")
        dlg.ShowModal()
        dlg.Destroy()

    def OnSearchTours(self, event):
        dlg = wx.TextEntryDialog(self, "Введите фразу для поиска:")
        if dlg.ShowModal() == wx.ID_OK:
            phrase = dlg.GetValue()
            tours = search_tours_by_phrase(phrase)
            if tours:
                tours_str = "\n".join([f"ID: {t[0]}, Название: {t[1]}" for t in tours])
                wx.MessageBox(tours_str, "Результаты поиска", wx.OK)
            else:
                wx.MessageBox("Туры не найдены.", "Результаты поиска", wx.OK)
        dlg.Destroy()


class AddTourDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(AddTourDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((300, 300))
        self.SetTitle("Добавить новый тур")

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Поля ввода
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="Название тура:")
        hbox1.Add(name_label, proportion=0, flag=wx.RIGHT, border=8)
        self.name_entry = wx.TextCtrl(panel)
        hbox1.Add(self.name_entry, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        type_label = wx.StaticText(panel, label="Тип тура:")
        hbox2.Add(type_label, proportion=0, flag=wx.RIGHT, border=8)
        self.type_entry = wx.TextCtrl(panel)
        hbox2.Add(self.type_entry, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        duration_label = wx.StaticText(panel, label="Длительность (дни):")
        hbox3.Add(duration_label, proportion=0, flag=wx.RIGHT, border=8)
        self.duration_entry = wx.TextCtrl(panel)
        hbox3.Add(self.duration_entry, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        transportation_label = wx.StaticText(panel, label="Транспорт:")
        hbox4.Add(transportation_label, proportion=0, flag=wx.RIGHT, border=8)
        self.transportation_entry = wx.TextCtrl(panel)
        hbox4.Add(self.transportation_entry, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        departure_label = wx.StaticText(panel, label="Пункт отправления:")
        hbox5.Add(departure_label, proportion=0, flag=wx.RIGHT, border=8)
        self.departure_entry = wx.TextCtrl(panel)
        hbox5.Add(self.departure_entry, proportion=1)
        vbox.Add(hbox5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        destination_label = wx.StaticText(panel, label="ID места назначения:")
        hbox6.Add(destination_label, proportion=0, flag=wx.RIGHT, border=8)
        self.destination_entry = wx.TextCtrl(panel)
        hbox6.Add(self.destination_entry, proportion=1)
        vbox.Add(hbox6, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Кнопки
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(panel, label="OK")
        closeButton = wx.Button(panel, label="Отмена")
        hbox7.Add(okButton, proportion=1, flag=wx.RIGHT, border=5)
        hbox7.Add(closeButton, proportion=1)
        vbox.Add(hbox7, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnOK(self, event):
        tour_name = self.name_entry.GetValue()
        tour_type = self.type_entry.GetValue()
        duration = self.duration_entry.GetValue()
        transportation = self.transportation_entry.GetValue()
        departure_point = self.departure_entry.GetValue()
        destination_id = self.destination_entry.GetValue()

        try:
            duration = int(duration)
            destination_id = int(destination_id)

            add_tour(tour_name, tour_type, duration, transportation, departure_point, destination_id)
            self.Destroy()

        except ValueError:
            wx.MessageBox("Длительность и ID места назначения должны быть числами.", "Ошибка", wx.OK | wx.ICON_ERROR)

    def OnCancel(self, event):
        self.Destroy()


class ChangeTransportDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(ChangeTransportDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle("Изменить транспорт тура")

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Поля ввода
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        tour_id_label = wx.StaticText(panel, label="ID тура:")
        hbox1.Add(tour_id_label, proportion=0, flag=wx.RIGHT, border=8)
        self.tour_id_entry = wx.TextCtrl(panel)
        hbox1.Add(self.tour_id_entry, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        transport_label = wx.StaticText(panel, label="Новый транспорт:")
        hbox2.Add(transport_label, proportion=0, flag=wx.RIGHT, border=8)
        self.transport_entry = wx.TextCtrl(panel)
        hbox2.Add(self.transport_entry, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Кнопки
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(panel, label="OK")
        closeButton = wx.Button(panel, label="Отмена")
        hbox3.Add(okButton, proportion=1, flag=wx.RIGHT, border=5)
        hbox3.Add(closeButton, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnOK(self, event):
        tour_id = self.tour_id_entry.GetValue()
        new_transportation = self.transport_entry.GetValue()
        try:
            tour_id = int(tour_id)
            change_transport(tour_id, new_transportation)
            self.Destroy()
        except ValueError:
            wx.MessageBox("ID тура должно быть числом.", "Ошибка", wx.OK | wx.ICON_ERROR)

    def OnCancel(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = TourApp()
    app.MainLoop()
