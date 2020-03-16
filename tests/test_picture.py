from context import gif


def gif_test():
    url = 'http://cl.330f.tk/htm_mob/2002/7/3822632.html'
    dir_path = '/tmp'
    page = gif.Page(url)
    page.download(dir_path)


if __name__ == "__main__":
    gif_test()
