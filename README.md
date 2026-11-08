# SocialMediaDownloadMaubot

Share social media content directly in your Matrix room with this [Maubot](https://github.com/maubot/maubot) plugin! Just paste a link, and it will download and post the content for everyone to see.

Currently supported social media platforms:
  - Reddit
  - Instagram (Might not work anymore because Instagram has massively restricted anonymous access.)
  - YouTube
  - TikTok
  - Bluesky

Choose what to download by configuring the plugin.

## Installation

Download the latest `.mbp` from the Releases section and add it as a plugin in
the Maubot Manager. Instaloader is bundled in the plugin package, so it does not
need to be installed in the Maubot environment.

## Building

Build a self-contained plugin package from the repository root. Each build bumps
the plugin version in `maubot.yaml` and writes
`build/SocialMediaDown-vMAJOR.MINOR.PATCH.mbp` (for example
`SocialMediaDown-v1.1.2.mbp`). The patch segment increases by one on every
build (`1.1.0` → `1.1.1` → `1.1.2`); after patch `99` the middle number
increases and patch resets to `0` (`1.1.99` → `1.2.0`).

```shell
./scripts/build-mbp.sh
```

On Windows (PowerShell):

```powershell
.\scripts\build-mbp.ps1
```

Pass `--no-bump` to build without changing `maubot.yaml`, or pass a custom output
path as an additional argument. Commit `maubot.yaml` after a release build if you
want the repository version to stay in sync.

The build installs the version pinned in `requirements.txt` into a temporary
directory and creates the `.mbp` archive without storing third-party source in
the repository. The `build/` directory is listed in `.gitignore`.

---

# Описание на русском

Делитесь контентом из соцсетей прямо в Matrix-комнате с помощью этого плагина
для [Maubot](https://github.com/maubot/maubot)! Вставьте ссылку — бот скачает
материал и отправит его в чат для всех участников.

Поддерживаемые платформы:
  - Reddit
  - Instagram (может перестать работать: Instagram сильно ограничил анонимный доступ)
  - YouTube
  - TikTok
  - Bluesky

Что именно скачивать, настраивается в конфигурации плагина.

## Установка

Скачайте последний `.mbp` из раздела Releases и добавьте плагин в Maubot Manager.
Instaloader уже включён в пакет плагина, отдельно ставить его в окружение Maubot
не нужно.

## Сборка

Из корня репозитория можно собрать автономный пакет плагина. При каждой сборке
версия в `maubot.yaml` увеличивается, а артефакт сохраняется в
`build/SocialMediaDown-vMAJOR.MINOR.PATCH.mbp` (например,
`SocialMediaDown-v1.1.2.mbp`). Третье число (patch) растёт на 1 при каждой сборке
(`1.1.0` → `1.1.1` → `1.1.2`); после `99` увеличивается среднее число, а patch
сбрасывается в `0` (`1.1.99` → `1.2.0`).

Linux/macOS:

```shell
./scripts/build-mbp.sh
```

Windows (PowerShell):

```powershell
.\scripts\build-mbp.ps1
```

Флаг `--no-bump` собирает пакет без изменения `maubot.yaml`; можно также указать
свой путь к выходному файлу. После релизной сборки закоммитьте `maubot.yaml`, если
нужно, чтобы версия в репозитории совпадала с собранным пакетом.

Сборка ставит зависимости из `requirements.txt` во временную папку и упаковывает
`.mbp` без хранения стороннего кода в репозитории. Каталог `build/` указан в
`.gitignore`.
