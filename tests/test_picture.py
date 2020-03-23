from context import gif


def gif_test():
    url = 'http://cl.de33.xyz/htm_mob/2003/7/3857500.html'
    dir_path = '/tmp'
    page = gif.Page(url)
    page.parse()
    # for i, img in enumerate(page.imgs):
    #     print(i, img)
    page.download(dir_path)


if __name__ == "__main__":
    gif_test()
