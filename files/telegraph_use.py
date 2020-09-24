from telegraph import Telegraph
import requests
import os
import time

telegraph = Telegraph(access_token='8efd824783cea0f0dcf74b885b2c643f56dcb037a71ee09914698d1e1e80')
# telegraph.create_account(short_name='Ivan',
#                          author_name='Ivan Garmashev',
#                          author_url='https://t.me/PUTEEEN',
#                          # replace_token='08a09f327cd39c4b23ea76f904c27a9ca223ad0ad641259baaf1164507e4',
#                          )
directory = 'C:/Users/ivang/PycharmProjects/Tg_channel/media/'  # directory of photo


def create_site(name):
    list_files = os.listdir(directory)
    photo_html = ''
    for i in list_files:
        print(i)
        with open(directory + i, 'rb') as f:  # upload photo to server
            file_name = i.rpartition('.jpg')[0]
            caption = file_name.replace(name[0], '@')
            photo_html = photo_html + '<p><figure><img src="' + (
                requests.post(
                    'https://telegra.ph/upload',
                    files={'1': ('1', f, 'image/jpg')}  # image/gif, image/jpeg, image/jpg, image/png, video/mp4
                ).json()[0]['src']
            ) + '"/><pre><figcaption>' + caption + '</figcaption></pre></figure></p>'
    response = telegraph.create_page(
        name,
        html_content=photo_html,
        author_name='Ivan Garmashev',
        author_url='https://t.me/PUTEEEN',
    )
    print(photo_html)
    link = 'https://telegra.ph/{}'.format(response['path'])
    print(link)
    return link


def delete_media():
    c = os.listdir(directory)
    for x in c:
        os.remove(directory + x)


# print(telegraph.get_account_info())
# print(telegraph.get_access_token())
# print(telegraph.get_page_list())
# telegraph.edit_page(path='Photo-09-18-28',
#                     title='Редактированный пост',
#                     author_name='Редактированный автор',
#                     # author_url='Редактированная ссылка',
#                     html_content='<p>Редактированный текст<br/></p>',)
# create_site(name='Название поста')
# create_site()
# create_site()
# print(telegraph.get_page('Photo-09-18-13'))
