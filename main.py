import argparse
from logic import Logic


def init_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='ITS')
    parser.add_argument('config', type=str, default="")
    parser.add_argument('command',
                        choices=[
                            'start',
                            'video_to_img',
                            'videos_to_imgs',
                            'new_json',
                            'check_imgs',
                            'copy_check_imgs',
                            'view_imgs',
                        ])
    parser.add_argument('-d', '--dst', type=str, default=".")
    parser.add_argument('-s', '--src', type=str, default=".")
    parser.add_argument('--path_check', type=str, default=".")
    parser.add_argument('--size', nargs='+', help='Resize img', default=['544', '320'])

    parser.add_argument('--rec', type=bool, default=False)
    parser.add_argument('--view_config', type=str, default="")

    return parser.parse_args()


if __name__ == '__main__':
    arg = init_arg()
    if len(arg.config) == 0:
        raise ValueError("not config")

    logic = Logic(arg.config)
    match arg.command:
        case "start":
            logic.start()
        case "video_to_img":
            logic.video_to_img()
        case "videos_to_imgs":
            logic.videos_to_imgs(arg.dst, arg.view_config)
        case "new_json":
            logic.new_json(arg.src, arg.dst)
        case "check_imgs":
            logic.check_imgs(arg.src, arg.dst, arg.rec)
        case 'copy_check_imgs':
            logic.copy_check_imgs(arg.path_check, arg.src, arg.dst)
        case 'view_imgs':
            size = [int(x) for x in arg.size]
            logic.view_imgs(size)
