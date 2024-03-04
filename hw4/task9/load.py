import argparse
import asyncio
from run_multiprocessing import run as m_run
from run_threading import run as t_run
from run_async import main as a_run
from load_images import run as s_run

parser = argparse.ArgumentParser(prog='Download image from URL',
                                 description='Application is downloading all images from html page to URL-link',
                                 epilog='Enter url is necessary')
parser.add_argument('-u', metavar='URL', type=str,
                    help='enter URL-link',
                    default='https://ya.ru')
parser.add_argument('-m', metavar='method of loading', type=str,
                    help='t - threading\n m - multiprocessing\n a - asynchronized\n s - synchronized',
                    default='s')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.m == 't':
        t_run(args.u)
    elif args.m == 'm':
        m_run(args.u)
    elif args.m == 'a':
        asyncio.run(a_run(args.u))
    else:
        s_run(args.u)