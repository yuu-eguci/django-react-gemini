django-react-gemini ♊
===

🐍 ⚛️ 🐳 🇳 Python 3.10 + Django v4 + Yarn + Nuxt v2 + Nginx + Docker + GitHub Actions + Ruff + CI/CD | Nuxt.js も使いてーし、 Django も使いてーけど、サーバはふたつも使いたくねーから、 Nginx を使って Django と Nuxt.js を同ドメインで配信しよーぜ。あと Docker は当然使うぜ。

- python + django + yarn + nuxt + nginx なんつー container を用意して、
- 開発環境では runserver (8000 -> 8081) と yarn dev (3000 -> 3001) で開発して、
- 実働環境では
    - nuxt は yarn generate で静的サイトにして、 nginx (8080/ -> 8081) で配信して、
    - django は nginx と gunicorn (8081/api/ -> 8080 -> 8000) で配信するよ!

![](docs/(2023-08-05)overall-view.png)

## コイツのいいところ

- Docker 環境 + Django + Nuxt.js (frontend) + MySQL がひとつのリポジトリに詰まっててシンプルだよ。
    - まあいいことばかりじゃないけど。
- up で3つ一気に立ち上がるよ。

Django エリアのいいところ

- 開発環境用、本番環境用の settings が分かれてるよ。
- 当然 Pipenv で管理できてるよ。
- コンソールと、 ./logs/ へのロギングができてるよ。ロギングの日時は UTC と JST を選べる。
- ユニットテストの基礎もちゃんとあるよ。
- ひさしぶりに来て、 "view どんなふうに書くんだっけ?" ってなったときのため views に view のベースを書いてるよ。
    - 最近、 async の view も足しといたよ。ただ動かすにはこれ↓が必要かも
    - uvicorn (asgi サーバ) を pip install
    - gunicorn が内蔵の wsgi サーバのみならず uvicorn を動かせるように設定する
    - そうすると gunicorn が uvicorn を worker として動かして、
    - uvicorn は asgi サーバとして django を配信してくれる!
- GitHub Actions で ruff, test がちゃんと走るよ。
- プロジェクト内部のモジュールをインポートするときは、つねに相対インポートを使ってる (3rd party との区別のため) よ。

Nuxt.js エリアのいいところ

- GitHub Actions で eslint, test がちゃんと走るよ。

Nginx エリアのいいところ

いいことばかりじゃないところ

- 1アプリケーションにつき1 docker container を使うと、 VSCode 開発のときに devcontainer をキレイに使えたりして利点がある。ひとつの container に複数アプリケーションが入っていると、その利点を利用することが不可。

## runserver と yarn dev で起動するところまで

```bash
# NOTE: (2025-03-04) 久しぶりに clone してみたけど、マジで
#       Create containers -> Django のほう
#       をサッサと打つだけで開始できた。イイぞ。

# Create containers
cp ./local.env ./.env; docker compose up -d; docker compose exec webapp-service bash

# Get into webapp-service
# NOTE: It's a good practice to have separate terminals for Django and Nuxt.js for easier debugging and log tracking.
docker compose exec webapp-service bash
# Check↓
python -V
# --> Python 3.12.9
pipenv --version
# --> pipenv, version 2024.4.1
yarn -v
# --> 1.22.22

(cd ./frontend-react; yarn list react)
# --> └─ react@19.0.0

# Django のほう。
# NOTE: PIPENV_VENV_IN_PROJECT は env で設定してある。
pipenv sync --dev
pipenv run python manage.py migrate
pipenv run python manage.py runserver 0.0.0.0:8000
# --> http://localhost:8001/ でアクセス。

# React のほう。
(cd ./frontend-react; yarn install)
(cd ./frontend-react; yarn dev --host)
# --> http://localhost:5001/ でアクセス。
```

```bash
# Test commands.
time pipenv run ruff check .
time pipenv run python manage.py test --failfast --parallel --settings=config.settings_test

# Currently unavailable.
# (cd ./frontend-react; time yarn test .)
# (cd ./frontend-react; time yarn lint)
```

```bash
# i18n commands.
(cd ./frontend-react; yarn run i18next "./src/App.tsx" "./src/**/*.tsx" --config "./i18next-parser.config.js")
```
