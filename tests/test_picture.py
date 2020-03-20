from context import gif


def gif_test():
    url = 'https://cb.333a.ml/htm_mob/2001/7/3790414.html'
    dir_path = '/tmp'
    page = gif.Page(url)
    for i, img in enumerate(page.imgs):
        print(i, img)
    # page.download(dir_path)


if __name__ == "__main__":
    gif_test()
