import os
from datetime import datetime

from fpdf import FPDF

from django.conf import settings


class PDF(FPDF):
    utils_path = os.path.join(settings.BASE_DIR, "utils/")

    def cell_(self, pdf_: FPDF, w=None, h=None, txt="", border=0, ln=0, align="", fill=False, link="",
              center=False, markdown=False, i_font=False, font="PTSans", type_="", size=14, move=False,
              m_w=10, m_h=None, m_ln=0):
        if i_font:
            pdf_.set_font(font, type_, size)
        if move:
            pdf_.cell(m_w, m_h, ln=m_ln)
        pdf_.cell(w, h, txt, border, ln, align, fill, link)


def height(data):
    # temp = max([len(i) for i in data])
    norm = max([len(i.split('\n')) for i in data])
    if norm in [1, 2]:
        return 7
    else:
        return 3.5 * norm
    # if temp < 40:
    #     return 10
    # elif temp // 2 < 40:
    #     return 20
    # else:
    #     return 20


def add_header(pdf_: PDF, logo_path):
    pdf_.add_page()
    pdf_.image(f'{logo_path}/images/logo.png', 10, 5, 40, 18)
    pdf_.set_fill_color(0, 0, 0)
    pdf_.cell_(pdf_, 191, 0.5, border=1, fill=True, ln=1, move=True, m_w=1, m_h=15, m_ln=1)
    pdf_.cell(1, 5, ln=1)


font_color = []


def get_pdf(data: dict):
    pdf = PDF('P', 'mm', 'A4')

    utils_path = pdf.utils_path
    pdf.add_page()
    pdf.add_font('PTSans', '', f'{str(utils_path)}fonts/PTSans-Regular.ttf', uni=True)
    pdf.add_font('PTSans', 'B', f'{str(utils_path)}fonts/PTSans-Bold.ttf', uni=True)

    pdf.image(f'{str(utils_path)}/images/logo.png', 10, 5, 40, 18)
    pdf.cell_(pdf, 70, 4, ' MEDDEV TEAM WORK', i_font=True, type_="B", size=7, move=True, m_w=42)
    pdf.cell_(pdf, 70, 4, 'Используем реагенты и оборудования компаний', ln=1, move=True, m_w=25)
    pdf.cell_(pdf, 70, 3, 'Адрес: https://t.me//n_ulugbekk', i_font=True, type_="", size=7, move=True, m_w=42)

    pdf.image(f'{str(utils_path)}/images/3.png', 152, 14, 50, 11)
    pdf.cell(1, 3, ln=1)

    pdf.cell_(pdf, 70, 3, 'Тел:(93) 563 55 09 ', ln=1, move=True, m_w=42)
    pdf.cell_(pdf, 70, 3, 'Эл.почта: dorilarimuz@mail.ru', ln=1, move=True, m_w=42)

    pdf.cell_(pdf, 191, 0.5, border=1, fill=True, ln=1, move=True, m_w=1, m_h=10, m_ln=1)

    # set patient information
    # pdf.cell_(pdf, 13, 15, "ФИО:", i_font=True, type_="B", size=14)
    # pdf.cell_(pdf, 80, 15, "Абдурахматов Мирзохид", i_font=True, type_="", size=14)
    # pdf.cell_(pdf, 35, 6, "Год рождения:", i_font=True, type_="B", size=14)
    # pdf.cell_(pdf, 60, 6, "2001", i_font=True, type_="", size=14, ln=1)
    # p_i = data.pop('patient_id')
    # gender = "Мужчина" if p_i["gender"] == "male" else "Женщина"
    pdf.cell_(pdf, 13, 15, "ФИО", i_font=True, type_="B", size=14)
    pdf.cell_(pdf, 80, 15, f"{data['p_name']}", i_font=True, type_="", size=14)
    pdf.cell_(pdf, 27, 15, "ФИО Врача", i_font=True, type_="B", size=14)
    pdf.cell_(pdf, 80, 15, f"{data['d_name']}", i_font=True, type_="", size=14, ln=1)

    pdf.cell_(pdf, 15, 6, "Дата", i_font=True, type_="B", size=14)
    pdf.cell_(pdf, 78, 6, "05.06.2022", i_font=True, type_="", size=14)
    pdf.cell_(pdf, 40, 6, "Должность врача", i_font=True, type_="B", size=14)
    pdf.cell_(pdf, 60, 6, f"{data['d_type']}", i_font=True, type_="", size=14)

    pdf.cell_(pdf, 191, 0, border=1, fill=True, ln=1, move=True, m_w=1, m_h=10, m_ln=1)
    #
    # pdf.cell_(pdf, 69, 17, "Дата и время взятия образца:", i_font=True, type_="B", size=14)
    # pdf.cell_(pdf, 50, 17, f"{datetime.fromisoformat(p_i['timestamp'].split('.')[0]).strftime('%d.%m.%Y %H-%M-%S')}", i_font=True, type_="", size=14, ln=1)
    pdf.cell_(pdf, 80, 15, "Название", align="L")
    pdf.cell_(pdf, 64, 15, "Применение", align="L", ln=1)
    # pdf.cell_(pdf, 47, 15, "Результат", align="L", ln=1)
    pdf.cell(191, 0.5, '_ ' * 57, ln=1)
    pdf.cell(10, ln=1)

    pdf.set_fill_color(245, 255, 243)
    some_val = data["data"]
    for i in some_val:
        line_height = height(i)
        pdf.set_font('PTSans', '', 11)
        pdf.multi_cell(80, line_height, i[0], max_line_height=pdf.font_size, ln=3, fill=True)
        pdf.set_font('PTSans', '', 9)
        pdf.multi_cell(64, line_height, i[1], max_line_height=pdf.font_size, align="L", ln=3,
                       fill=True)
        pdf.set_font('PTSans', '', 9)
        pdf.multi_cell(47, line_height, "", max_line_height=pdf.font_size, ln=3, fill=True)
        pdf.ln(line_height)
        pdf.cell(10, 2, ln=1)

    # for iter_, j in enumerate(data['results'].items()):
    #     l_h = 35
    #     i, j = j
    #     if not Category.objects.get(name=i).is_continuous:
    #     # if i in ["УЗИ", "Консультации Врачей", "Услуги Гинеколога"]:
    #         continue
    #     for row in data:
    #         l_h += height(row)
    #         l_h += 1
    #     y = pdf.y
    #     temp = y+l_h
    #     if temp >= 290:
    #         add_header(pdf, utils_path)
    #         # print("WOINFE")
    #         # h = 297-y-25
    #         # print(h)
    #         # pdf.cell(50, h, ln=1)
    #     else:
    #         pdf.cell(1, 5, ln=1)
    #         if iter_ > 0:
    #             add_header(pdf, utils_path)
    #     set_fill_color(pdf, i)
    #
    #     # pdf.set_font('PTSans', 'B', 14)
    #     pdf.set_text_color(255, 255, 255)
    #
    #     pdf.cell_(pdf, 191, 10, i, align="C", fill=True, ln=1, i_font=True, type_="B")
    #
    #     pdf.set_text_color(31, 26, 23)
    #
    #     pdf.cell_(pdf, 80, 15, "Название/показатель", align="L")
    #     pdf.cell_(pdf, 64, 15, "Норма", align="L")
    #     pdf.cell_(pdf, 47, 15, "Результат", align="L", ln=1)
    #     # pdf.cell(10, ln=1)
    #
    #     pdf.set_fill_color(245, 255, 243)
    #     for col in j:
    #         for row in col:
    #             line_height = height([row["param_id"]["name"], row["param_id"]["norm"], row["res"]])
    #             pdf.set_font('PTSans', '', 11)
    #             pdf.multi_cell(80, line_height, row["param_id"]["name"], max_line_height=pdf.font_size, ln=3, fill=True)
    #             pdf.set_font('PTSans', '', 9)
    #             pdf.multi_cell(64, line_height, row["param_id"]["norm"], max_line_height=pdf.font_size, align="L", ln=3,
    #                            fill=True)
    #             pdf.set_font('PTSans', '', 9)
    #             pdf.multi_cell(47, line_height, row["res"], max_line_height=pdf.font_size, ln=3, fill=True)
    #             pdf.ln(line_height)
    #             pdf.cell(10, 2, ln=1)
    #             if pdf.y + 30 >= 295:
    #                 add_header(pdf, utils_path)
    #                 pdf.set_fill_color(245, 255, 243)
    pdf.set_font('PTSans', '', 10)
    pdf.set_y(240)
    pdf.cell(1, 1, ln=1)
    pdf.cell(10, 5)
    pdf.image(f'{data["qr_url"]}', 75, 210, 60, 60)
    # pdf.multi_cell(170, 5, "Интерпретацию полученных результатов "
    #                         "проводит врач в совокупности с данными анамнеза, клиническими данными и "
    #                         "результатами других диагностических исследований. ", ln=1)
    # pdf.cell(190, 12, ln=1)
    # pdf.cell(70, 10)
    # pdf.cell_(pdf, 63, 10, "Заведующая лабораторией:", i_font=True, type_="B", size=14)
    # pdf.cell_(pdf, 50, 10, "Ишанходжаева Д.", i_font=True, type_="", size=14)
    # output_path = os.path.join(settings.BASE_DIR, 'media/temp.pdf')#.format(file_name[0], file_name[1], file_name[2]))
    pdf.output(data["opath"])
    # pdf.output("D:/temp.pdf")
    return data["opath"]
