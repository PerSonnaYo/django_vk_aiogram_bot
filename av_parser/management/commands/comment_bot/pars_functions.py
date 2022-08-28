import logging
import time
import vk
from aiogram.types import CallbackQuery, Message,\
    InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pars_name(urlname, API):
    # try:
    #     if isinstance(urlname, list):
    #         urlname = str(urlname[0])
    # except:
    #     x = 0
    # if 'Администрация' in urlname:
    #     urlname = urlname.split('[')[1]
    #     urlname = '[' + urlname
    if 'https' in urlname or 'vk.com' in urlname:  # если вставлена ссылка
        id = urlname.split('/')[-1]
        if id[-1] == ' ':
            id = id[:-1]
        while True:
            try:
                fio = API.users.get(user_ids=id)
                break
            except:
                time.sleep(1)
                continue
        n = fio[0]["first_name"]
        f = fio[0]["last_name"]
        fio = n + ' ' + f
        saler = urlname
    elif(urlname[0] == 'i'):
        bb = urlname.split('|')
        fio = bb[-1]
        saler = f"https://vk.com/{bb[0]}"
    else:
        fio  = urlname
        saler = f"https://vk.com"
    return (fio, saler)

def pars_discription(text):#безопасно
    try:
        description = text.split('Описание:')[1]
        description = description.split('Антиснайпер:')[0]
        if not re.search(r'[^\W\d]', description):
            description = 'Coin'
    except:
        try:
            description = text.split('Лот:')[1]
            description = description.split('\n')[0]
            if not re.search(r'[^\W\d]', description):
                description = 'Coin'
        except:
            description = 'Coin'
    return description

def pars_photo(post):#безопасно
    try:
        foto = post['attachments']
        url_photo1 = foto[0]['photo']['sizes'][8]['url']  # первое фото
        try:
            url_photo2 = foto[1]['photo']['sizes'][8]['url']  # второе фото
        except:
            url_photo2 = 'https://a.d-cd.net/K5QQNtmo-k-AYNo5jDMn0BfYcIQ-960.jpg'
    except:
        url_photo1 = 'https://a.d-cd.net/K5QQNtmo-k-AYNo5jDMn0BfYcIQ-960.jpg'
        url_photo2 = 'https://a.d-cd.net/K5QQNtmo-k-AYNo5jDMn0BfYcIQ-960.jpg'
    return (url_photo1, url_photo2)

def make_kb(url_post, fio):
    u1 = f'ski${url_post}'#до 64 символов
    u2 = f'sta${url_post}'
    u3 = f'sto${url_post}'
    u4 = f'bla${fio}'
    menu_kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(text="Пропустить", callback_data=u1),
        InlineKeyboardButton(text="Ставка", callback_data=u2),
        InlineKeyboardButton(text="Изменить прошлую ставку", callback_data=u3),
        InlineKeyboardButton(text="В черный список", callback_data=u4)
    )
    return menu_kb

def pars_post(text):#безопасно
    try:
        post_price = re.findall(r'стоимость пересылки: (.*?)\nОплата', text)[0]
    except:
        try:
            post_price = re.findall(r'стоимость пересылки: (.*?)', text)[0]
            if post_price == '':
                post_price = re.findall(r'стоимость пересылки: (.*?)Оплата', text)[0]
        except:
            try:
                post_price = re.findall(r'\nПересыл (.*?)\n', text)[0]
            except:
                post_price = '250 rub'
    return (post_price)

def start_pars(text):
    match = re.findall(r'ОКОНЧАНИЕ: (\d+\.\d+\.\d+) года', text)  # вычленяем дату
    if len(match) == 0:
        match = re.findall(r'Окончание: (\d+\.\d+\.\d+) г', text)  # вычленяем дату
    return match

def patern_vk(text, word):
    first = text.split('Владелец')
    second = first[1].split(word)[0]
    logger.info(f'TTparsing for {second} 99TT')
    url_pattern = r'https://[\S]+'
    try:
        urls = re.findall(url_pattern, second)[0]
        if ')' in urls:
            urls = urls.split(')')[0]#такие ситуации "http\\vk.com\fdfdef)"
    except:
        try:
            url_pattern1 = r'vk.com/[\S]+'
            urls = re.findall(url_pattern1, second)[0]
            if ')' in urls:
                urls = urls.split(')')[0]#такие ситуации "http\\vk.com\fdfdef)"
        except:
            try:
                urls = second.split('[')[1]
                urls = urls.split(']')[0]
            except:
                urls = second.strip(' ')
    return urls

def pre_pars_name(text):
    if 'Начало' in text and 'Старт' not in text and 'Гарант' not in text:
        url = patern_vk(text, 'Начало')
    elif 'Гарант' in text:
        url = patern_vk(text, 'Гарант')
    else:
        url = patern_vk(text, 'Старт')
#     match = re.findall(r': (.*?)\nСтарт', text)
#    # print(match)
#     if len(match) == 0:
#         match = re.findall(r':(.*?)\nСтарт', text)
#     #print(match)
#     if len(match) == 0:
#         match = re.findall(r'Владелец (.*?)\nСтарт', text)
#     #print(match)
#     if len(match) == 0 and "\n \nНачало" in text:
#         first = text.split('Владелец: ')
#         second = first[1].split('\n \nНачало')[0]
#         third = second.split('\n')[1]
#         if third == ' ':
#             third = second.split('\n \n')[1][:-1]
#         match = third
#    # print(match)
#     if len(match) == 0:
#         first = text.split('Владелец: ')
#         #print(first)
#         second = first[1].split('\n \nСтарт')[0]
#         third = second.split('\n\n')[-1]
#         if third == ' ':
#             third = second.split('\n \n')[1]
#         match = third
#     #print(match)
    logger.info(f'TTparsing for {url} 99TT')
    return url

def pars_step(toxt):#безопасно
    try:
        s = int(re.findall(r'Шаг: (\d+)', toxt)[0])  # Шаг торгов
    except:
        try:
            s = int(re.findall(r'Шаг - (\d+)', toxt)[0])  # Шаг торгов
        except:
            s = 50
    return s
