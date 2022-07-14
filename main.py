import json
from pathlib import Path
from urllib.parse import unquote, urlsplit, urljoin

import requests
from environs import Env


def get_file_name_from_url(url: str) -> str:
    return Path(unquote(urlsplit(url).path)).name


def download_image(images_path: Path, image_url: str) -> Path:
    img_response = requests.get(image_url)
    img_response.raise_for_status()
    file_path = images_path.joinpath(
        get_file_name_from_url(image_url)
    )
    with open(file_path, 'wb') as file:
        file.write(img_response.content)
    return file_path


def get_comic_metadata(comic_url: str) -> dict:
    response = requests.get(
        urljoin(comic_url, 'info.0.json')
    )
    response.raise_for_status()
    return response.json()


def main():
    env = Env()
    env.read_env()
    vk_app_client_id: int = env.int('VK_APP_CLIENT_ID')
    vk_app_access_token: str = env('VK_APP_ACCESS_TOKEN')
    images_path = Path('images')
    images_path.mkdir(parents=True, exist_ok=True)
    comic_url = 'https://xkcd.com/353/'
    comic_metadata = get_comic_metadata(comic_url)
    image_url: str = comic_metadata['img']
    author_comment: str = comic_metadata['alt']
    download_image(images_path, image_url)
    print(author_comment)

    vk_api_url = 'https://api.vk.com/method/'
    vk_api_version = '5.131'
    groups_get_url = urljoin(vk_api_url, 'groups.get')
    groups_get_params = {
        'extended': True,
        'access_token': vk_app_access_token,
        'v': vk_api_version
    }
    groups_get_response = requests.get(
        url=groups_get_url,
        params=groups_get_params
    )
    groups_get_response.raise_for_status()
    print(
        json.dumps(
            groups_get_response.json(),
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
