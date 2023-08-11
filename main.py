import argparse
from logic import Logic


def init_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='ITS')
    parser.add_argument('config', type=str)
    parser.add_argument('command',
                        choices=[
                            'start',
                            'video_to_img',
                            'videos_to_imgs',
                            'new_json',
                            'check_imgs',
                            'copy_check_imgs',
                            'view_imgs',
                            "run"
                        ])
    parser.add_argument('--size', nargs='+',
                        help='Resize img', default=['544', '320'])

    return parser.parse_args()


if __name__ == '__main__':
    arg = init_arg()

    logic = Logic(arg.config)
    match arg.command:
        case "start":
            logic.start()
        case "video_to_img":
            logic.video_to_img()
        case 'view_imgs':
            size = [int(x) for x in arg.size]
            logic.view_imgs(size)
        case "videos_to_imgs":
            logic.videos_to_imgs()
        case "check_imgs":
            logic.check_imgs()
        case 'copy_check_imgs':
            logic.copy_check_imgs()
        case "update_config":
            logic.new_json()
        case "run":
            size = [int(x) for x in arg.size]
            logic.run(size)
        
