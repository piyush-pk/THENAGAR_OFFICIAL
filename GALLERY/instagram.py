# importing Modules
import requests as r
import webbrowser


class Instgram:
    @staticmethod
    def get_media():
        items = {
            'urls':[],
            'comments':[],
            'caption':[],
        }


        # Account Details
        token = 'EAAHhZBEu1vmYBAO5bUnPZBV7PB8h0iJDZAm32kpJvJYYkuvFAsaIvQcOFQrxPslYuSlU7JcZCzRkvWdhoivlRZAdudInc4lRtFPpxjoy61JWok2u5tWCuJWDuqvaYk36ZAFDOf3wCfib4k01WAZAxxrany0iVoi7c0xXvAVN75yZBp1ZC6poKrGVJ9UWqx15Mo7AZD'
        ig_id = '17841408105501465'

        # Urls
        profile_url = f'https://graph.facebook.com/v3.2/{ig_id}?fields=id,media&access_token={token}'
        # comment_url = f'https://graph.facebook.com/v10.0/{post['id']}?fields=like_count,caption,comments_count,media_product_type,media_type,media_url,owner,shortcode,timestamp,comments&access_token={token}'
        # replies_url = f'https://graph.facebook.com/v10.0/17866658201305886?fields=id,username,replies,like_count&access_token={token}'


        # Requests
        profile_data = r.get(profile_url).json()
        posts = profile_data['media']['data']

        for post in posts:
            try:
                comment_url = f'https://graph.facebook.com/v10.0/{post["id"]}?fields=like_count,caption,comments_count,media_product_type,media_type,media_url,owner,shortcode,timestamp,comments&access_token={token}'
                data = r.get(comment_url).json()
                items['urls'].append(data['media_url'])          
                comments = [comment['text'] for comment in data['comments']['data']]
                items['comments'].append(comments)
                items['caption'].append(data['caption'])
                # print(items['caption'])
            except:
                pass
        return items

