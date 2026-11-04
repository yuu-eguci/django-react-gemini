django-react-gemini ♊
===

🐍 ⚛️ 🐳 🇳 Python 3.14 + Django 6.1 + Yarn + React + Nginx + Docker + GitHub Actions + Ruff + CI/CD | React も使いてーし、 Django も使いてーけど、サーバはふたつも使いたくねーから、 Nginx を使って Django と React を同ドメインで配信しよーぜ。あと Docker は当然使うぜ。

## ステータス

- Docker: 対応!
- Python 3.14 / Django 6.1 / Django REST framework 3.18 / MySQL 8.4
- Node.js 24 / React 19.3 / Vite 8 / TypeScript 6.0
- Linter: Ruff 0.17 / ESLint 10
- Test: Django test runner / Vitest 5
- CI: GitHub Actions (main への push と PR)

## コイツのいいところ

- Docker 環境 + Django + React (frontend) + MySQL + Nginx がひとつのリポジトリに詰まっててシンプルだよ。
    - まあいいことばかりじゃないけど。
- `docker compose up` で Django と MySQL のコンテナが立ち上がります。 React は Django と同じコンテナ内で起動します。
- 開発環境:
    - Django runserver (8000) -> docker-compose portforward (8001) -> localhost:8001
    - React yarn dev (5173) -> docker-compose portforward (5001) -> localhost:5001
- Ubuntu 環境:
    - Django Dockerfile gunicorn (8000) -> docker-compose portforward (8001) -> nginx (80) -> domain:80
    - React yarn build -> frontend-react/dist -> nginx (80) -> domain:80 で配信します。

### Django エリアのいいところ

- 開発環境用、本番環境用の settings が分かれてるよ。
- 当然 Pipenv で管理できてるよ。
- コンソールと、 ./logs/ へのロギングができてるよ。ロギングの日時は UTC と JST を選べる。
- View 、 middleware 、例外ハンドラ、 settings のユニットテストがあります。 DB 無しで実行できます。
- ひさしぶりに来て、 "view どんなふうに書くんだっけ?" ってなったときのため views に view のベースを書いてるよ。
    - async の view もあります。 ASGI で動かす場合は、以下の設定が必要です。
    - uvicorn (asgi サーバ) を pip install
    - gunicorn が内蔵の wsgi サーバのみならず uvicorn を動かせるように設定する
    - そうすると gunicorn が uvicorn を worker として動かして、
    - uvicorn は asgi サーバとして django を配信します。
- GitHub Actions で Ruff (lint / format) 、 Django test 、 ESLint 、 Vitest 、 i18n の抽出漏れチェック、型チェック + build を実行します。
- プロジェクト内部のモジュールをインポートするときは、つねに相対インポートを使ってる (3rd party との区別のため) よ。

### React エリアのいいところ

- `vite-tsconfig-paths` とか `react-router-dom` とか `react-i18next` とか導入済み。
- "さあオリジナリティ出していくぜ、" のひとつ前の段階まで揃えてある。
    - これ以上をやると、オリジナリティを出していくときの邪魔になる。

### Nginx エリアのいいところ

- Apache ではない (笑)

### いいことばかりじゃないところ

- 1アプリケーションにつき1 docker container を使うと、 VSCode 開発のときに devcontainer をキレイに使えたりして利点がある。ひとつの container に複数アプリケーションが入っていると、その利点を利用することが不可。

## runserver と yarn dev で起動するところまで

```bash
# NOTE: Create containers -> Django のほう
#       を実行するだけで開始できます。

# Create containers
cp ./local.env ./.env; cp ./webapp-container/Dockerfile.local ./webapp-container/Dockerfile;
docker compose up -d; docker compose exec webapp-service bash

# Get into webapp-service
# NOTE: It's a good practice to have separate terminals for Django and React for easier debugging and log tracking.
docker compose exec webapp-service bash
# Check↓
python -V
# --> Python 3.14.10
pipenv --version
# --> pipenv, version 2026.10.5
yarn -v
# --> 1.22.22

(cd ./frontend-react; yarn list react)
# --> └─ react@19.3.1

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
time pipenv run ruff format --check .
time pipenv run python manage.py test --failfast --parallel --settings=config.settings_test

# run 無し: watch mode
# run 有り: いつもの
(cd ./frontend-react; time yarn test run)
(cd ./frontend-react; time yarn lint)
(cd ./frontend-react; time yarn build)
```

```bash
# i18n commands.
(cd ./frontend-react; yarn i18next-cli extract)
```
