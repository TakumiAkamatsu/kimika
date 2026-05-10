# Kimika

> Recipe-driven software for computational chemistry and computational biochemistry,
> with a Streamlit-based UI as the primary interface.

このドキュメントは、Kimika プロジェクトの設計思想・構成・実装方針を Claude Code に伝えるための仕様書です。実装作業を行う際は、本ドキュメントの方針に従ってください。

---

## 1. プロジェクト概要

### 1.1 名前の由来

**Kimika**（キミカ）は、バスク語およびタガログ語で「化学（chemistry）」を意味する実在の語。イタリア語 *chimica*（および中世ラテン語 *chymia*、古代ギリシャ語 *χημεία*）の系譜に属する。

### 1.2 目的

- 計算化学・計算生物化学のシミュレーションを統合的に扱える研究用ソフトウェア
- 将来的には生体分子レベルからの細胞シミュレーションまでをカバーすることを長期的なゴールとする
- 当面は通常の計算化学のシミュレーションが可能な範囲から開始する

### 1.3 形態

- **ライブラリではなくソフトウェア**。espnet のように、レシピ駆動で実験条件を管理して実行する形態
- ただし espnet と異なり、**YAML を直接書く負担を軽減するため、Streamlit ベースの UI から設定可能とする**

---

## 2. 基本設計方針

### 2.1 計算エンジン

- **既存ソフトのラッパー型統合環境**として実装する
- 自前で QM/MD のコアアルゴリズムは実装しない
- ラップ対象は **オープンソースのみ**（Gaussian 等の商用ソフトは対象外）
- 主な対象：PySCF、OpenMM、RDKit、ASE、MDAnalysis 等

### 2.2 対応プラットフォーム

- **Linux / macOS のみを公式サポート**
- **Windows はサポート対象外**（Windows ネイティブ・WSL いずれも保証しない）
- 理由：PySCF が Windows ネイティブをサポートしないため。また開発・利用環境を Linux/macOS に統一することで設計が単純になる

### 2.3 パッケージ管理

- **uv** で管理する（pip ではない）
- 依存追加は `uv add <package>` で行う
- 重い計算エンジンは **optional dependencies (extras)** として分離する
- 例：`uv pip install kimika[qm,md]` のように選択的にインストール可能とする

### 2.4 Python バージョン

- 下限は **3.11**、上限は **3.13**（依存関係の対応状況に応じて拡張）

### 2.5 Psi4 について

- Psi4 は uv（pip）ではインストールできない（conda 配布のみ）
- そのため、**Psi4 サポートは現時点では諦める**
- 将来 QCEngine 経由でサポートする可能性は残すが、初期実装では対象外

---

## 3. リポジトリ構成

### 3.1 リポジトリ粒度

**シングルリポジトリ**（モノレポ）。コアコード、UI、CLI、公式レシピカタログをすべて一つのリポジトリで管理。

### 3.2 espnet の問題意識と解決方針

espnet を使った経験から、**「コードと実験データが混ざる」問題は構造的に避ける**ことを最重要設計方針とする。

- Kimika 本体のリポジトリには **コードと公式レシピカタログのみ** を含める
- ユーザーの実験データ・実験プロジェクトは **完全に別ディレクトリで管理する** ことを前提とする
- `kimika init <project_name>` コマンドでテンプレートからユーザーワークスペースを生成する

### 3.3 ディレクトリ構成

```
kimika/
├── kimika/                          # コアパッケージ（pip install kimika）
│   ├── __init__.py
│   ├── _version.py
│   │
│   ├── schemas/                     # Pydantic スキーマ定義（中核）
│   │   ├── base.py                 # 共通基底スキーマ
│   │   ├── recipe.py               # トップレベルレシピスキーマ
│   │   ├── system.py               # 分子系・周期系の記述
│   │   ├── tasks/                  # タスク別スキーマ
│   │   │   ├── qm.py
│   │   │   ├── md.py
│   │   │   ├── docking.py
│   │   │   └── ...
│   │   ├── engines/                # エンジン別の設定スキーマ
│   │   │   ├── pyscf.py
│   │   │   ├── ase.py
│   │   │   ├── openmm.py
│   │   │   └── rdkit.py
│   │   └── tracking.py             # MLflow 連携用スキーマ
│   │
│   ├── tasks/                       # タスク実装（QM・MD等の「やりたいこと」）
│   │   ├── base.py                 # Task 抽象基底クラス
│   │   ├── qm.py
│   │   ├── md.py
│   │   ├── docking.py
│   │   └── registry.py
│   │
│   ├── engines/                     # 既存ソフトのラッパー（「実装手段」）
│   │   ├── base.py                 # Engine 抽象基底クラス
│   │   ├── pyscf_engine.py
│   │   ├── ase_engine.py
│   │   ├── openmm_engine.py
│   │   ├── rdkit_engine.py
│   │   └── registry.py
│   │
│   ├── recipes/                     # レシピのロード・実行
│   │   ├── loader.py               # YAML → Pydantic モデル
│   │   ├── validator.py
│   │   └── runner.py               # レシピ実行のオーケストレーション
│   │
│   ├── workspace/                   # ユーザーワークスペース管理
│   │   ├── init.py                 # `kimika init` の実装
│   │   ├── layout.py               # 推奨ディレクトリ構造の定義
│   │   ├── templates/              # init で展開されるテンプレート
│   │   │   └── default/
│   │   │       ├── recipe.yaml
│   │   │       ├── inputs/.gitkeep
│   │   │       ├── results/.gitkeep
│   │   │       └── README.md
│   │   └── project.py              # KimikaProject クラス
│   │
│   ├── tracking/                    # 実験追跡（MLflow ラッパー）
│   │   ├── mlflow_backend.py
│   │   ├── logger.py
│   │   └── artifacts.py
│   │
│   ├── io/                          # 入出力（分子ファイル等）
│   │   ├── readers.py              # XYZ, PDB, SDF, MOL2, GRO 等
│   │   ├── writers.py
│   │   └── trajectory.py
│   │
│   ├── ui/                          # Streamlit UI（主要インターフェース）
│   │   ├── app.py                  # メインエントリ
│   │   ├── pages/                  # マルチページ構成
│   │   │   ├── 01_home.py
│   │   │   ├── 02_recipe_builder.py
│   │   │   ├── 03_runner.py
│   │   │   ├── 04_results_viewer.py
│   │   │   └── 05_experiment_browser.py
│   │   ├── components/             # 再利用可能 UI コンポーネント
│   │   │   ├── recipe_form.py
│   │   │   ├── molecule_viewer.py
│   │   │   ├── progress.py
│   │   │   └── ...
│   │   ├── state.py                # Streamlit セッション状態管理
│   │   └── schema_to_form.py       # Pydantic → Streamlit フォーム変換
│   │
│   ├── cli/                         # CLI（補助的）
│   │   ├── main.py                 # kimika エントリポイント
│   │   └── commands/
│   │       ├── init.py             # kimika init
│   │       ├── run.py              # kimika run recipe.yaml
│   │       ├── ui.py               # kimika ui (Streamlit 起動)
│   │       ├── validate.py         # kimika validate recipe.yaml
│   │       ├── catalog.py          # kimika catalog (公式レシピ一覧)
│   │       └── config.py           # kimika config (show/set/get)
│   │
│   └── utils/
│       ├── logging.py
│       ├── paths.py
│       ├── config.py               # 設定ファイル・環境変数・デフォルト値の統合
│       └── hash.py
│
├── recipes/                         # 公式レシピカタログ
│   ├── README.md
│   ├── qm/
│   │   ├── water_dft/
│   │   │   ├── recipe.yaml
│   │   │   ├── inputs/water.xyz
│   │   │   └── README.md
│   │   ├── benzene_mp2/
│   │   └── ...
│   ├── md/
│   │   └── alanine_dipeptide_amber/
│   ├── docking/
│   └── ...
│
├── examples/                        # クイックスタート用最小例
│   ├── 01_quickstart_qm/
│   ├── 02_quickstart_md/
│   └── 03_streamlit_walkthrough.md
│
├── tests/
│   ├── unit/
│   │   ├── test_schemas.py
│   │   ├── test_engines/
│   │   ├── test_tasks/
│   │   └── test_recipes.py
│   ├── integration/
│   ├── recipes/                    # recipes/ 全件を CI で実行
│   └── ui/
│
├── docs/
│   ├── index.md
│   ├── getting_started.md
│   ├── concepts/
│   ├── tutorials/
│   ├── reference/
│   └── developer/
│
├── .github/workflows/
│
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

### 3.4 ユーザーワークスペース（Kimika リポジトリ外）

ユーザーは自分の研究ディレクトリで実験を管理する。Kimika 本体のリポジトリにはユーザーデータは一切含めない。

**デフォルトのワークスペースルートは `~/.kimika/`**。`kimika init <project_name>` を引数なしで実行した場合、このディレクトリ下にプロジェクトが作成される。

```
~/.kimika/                          # ワークスペースルート（デフォルト）
├── .mlruns/                       # MLflow tracking ストア（デフォルト）
├── proj_water_basis_set/          # 個別プロジェクト
│   ├── recipe.yaml
│   ├── inputs/
│   │   └── water.xyz
│   ├── results/
│   │   ├── run_001/
│   │   └── run_002/
│   ├── analysis/
│   └── .kimika                   # Kimika プロジェクトのマーカー
└── proj_protein_md/
```

### 3.5 設定システム

ワークスペースの場所などをユーザーが変更できるよう、設定ファイルと環境変数による上書きをサポートする。

#### 設定ファイル

XDG Base Directory 仕様に従い、`~/.config/kimika/config.toml` をユーザー設定ファイルとする。

```toml
# ~/.config/kimika/config.toml
[workspace]
root = "~/.kimika"                  # デフォルト値

[ui]
default_page = "home"

[mlflow]
tracking_uri = "file:~/.kimika/.mlruns"
```

#### 設定値の優先順位

1. **環境変数**（最優先）
   - `KIMIKA_WORKSPACE_ROOT`
   - `KIMIKA_MLFLOW_URI` 等
2. **設定ファイル** `~/.config/kimika/config.toml`
3. **デフォルト値**（`~/.kimika/`）

#### 関連 CLI コマンド

```bash
# デフォルトのワークスペース（~/.kimika/）にプロジェクト作成
kimika init proj_water_dft

# 別の場所に作りたい場合
kimika init proj_water_dft --path ./

# ワークスペース・設定の確認
kimika config show

# 設定の変更
kimika config set workspace.root ~/research/kimika
```

#### MLflow との連携

- デフォルトの MLflow tracking URI は `~/.kimika/.mlruns`（ワークスペースルート直下）
- すべてのプロジェクトの実験を **横断的に一つのダッシュボードで閲覧可能**
- プロジェクト個別に分離したい場合は、各レシピの `tracking` セクションで個別の URI を指定可能

#### Streamlit UI からのワークスペース利用

Streamlit UI は起動時にワークスペースルートを読み込み、そこに含まれるプロジェクト（`.kimika` マーカーがあるディレクトリ）を一覧表示する。これにより、UI 中心の利用フローでも「自分のプロジェクトをまとめて管理する場所」が明確になる。

---

## 4. アーキテクチャの中核設計

### 4.1 Pydantic スキーマがすべての中心

レシピ・タスク設定・エンジン設定をすべて Pydantic v2 のモデルで定義する。これがスキーマ・バリデーション・UI フォーム生成・ドキュメント生成の単一情報源（single source of truth）となる。

派生して以下が自動生成される：

- レシピ YAML のバリデーション
- Streamlit UI のフォーム（`streamlit-pydantic` ベース）
- CLI のヘルプ・バリデーション
- ドキュメントのスキーマリファレンス

### 4.2 Tasks と Engines の分離

- **Task**：「QM 計算をする」「MD 実行をする」という *やりたいこと*
- **Engine**：「PySCF を使う」「OpenMM を使う」という *実装手段*

両者を分離することで、同じタスクを異なるエンジンで実行できる構造とする。`registry.py` でプラグイン的に登録する形を採用する。

### 4.3 ワークスペースとカタログの分離

- **公式レシピカタログ**（`recipes/`）：Kimika リポジトリに含める。テンプレートとして参照される。CI で実行テストを行う
- **ユーザーワークスペース**（リポジトリ外）：`kimika init` で生成。テンプレートをコピーして編集する形でユーザーが利用する
- **公式レシピを直接編集することはしない**。これを規約として徹底する

### 4.4 インターフェースの優先順位

1. **Streamlit UI が主要インターフェース**（`kimika ui` で起動）
2. **CLI は補助的**（`kimika run`, `kimika init`, `kimika validate`, `kimika catalog`, `kimika config`）
3. **Python API は内部利用と上級ユーザー向け**

### 4.5 ワークスペースと設定システム

- **デフォルトワークスペース**：`~/.kimika/`
- **設定ファイル**：`~/.config/kimika/config.toml`（XDG 準拠）
- **環境変数による上書き**をサポート（`KIMIKA_WORKSPACE_ROOT` 等）
- 詳細はセクション 3.5 を参照

---

## 5. 使用ライブラリ方針

### 5.1 採用方針

- **計算エンジンはすべてコア依存に統合する**（extras では分離しない）
- 理由：研究で使っていれば QM・MD・化学情報処理・生体分子処理は結局すべて必要になるため、extras で分離するメリットよりも `uv add kimika` 一発で完結するメリットの方が大きい
- 機械学習ポテンシャル（torch, e3nn 等）は **現段階では含めない**。将来必要になった段階で再検討する
- 開発依存（`[dev]`）のみ extras として分離する
- すべて PyPI 配布のもの（`uv add` で解決可能）

### 5.2 コア依存（すべて必須）

#### 基盤・スキーマ・UI

| カテゴリ | ライブラリ | 用途 |
|---------|-----------|------|
| スキーマ | `pydantic` (v2) | レシピのスキーマ定義・検証 |
| YAML | `ruamel.yaml` | コメント保持の YAML 処理 |
| CLI | `typer` | CLI フレームワーク |
| ロギング | `loguru` | 構造化ロギング |
| 出力 | `rich` | カラフルな出力・プログレスバー |
| 数値計算 | `numpy`, `scipy`, `pandas` | 基本的な科学計算 |
| UI | `streamlit` | UI フレームワーク（主要インターフェース） |
| UI | `streamlit-pydantic` | Pydantic からのフォーム自動生成（足りない部分は独自実装で補強） |
| 可視化 | `stmol` または `py3Dmol` | 分子可視化（Streamlit 統合） |
| 可視化 | `plotly` | インタラクティブグラフ |
| 実験追跡 | `mlflow` | 実験追跡 |

#### 計算エンジン・科学計算ライブラリ

| カテゴリ | ライブラリ | 用途 |
|---------|-----------|------|
| 量子化学 | `pyscf` | 主要 QM エンジン |
| 量子化学 | `qcengine`, `qcelemental` | QM 抽象化層（将来の他エンジン対応の準備） |
| 量子化学 | `geometric` | 構造最適化 |
| 量子化学 | `basis-set-exchange` | 基底関数セット |
| 分子動力学 | `openmm` | 主要 MD エンジン |
| 分子動力学 | `openmmforcefields` | AMBER/CHARMM 力場 |
| 分子動力学 | `mdanalysis` | トラジェクトリ解析 |
| 分子動力学 | `mdtraj` | トラジェクトリ I/O |
| 化学情報処理 | `rdkit` | 化学構造処理・記述子 |
| 原子操作（補助） | `ase` | 補助的に使用。**抽象化は Kimika 独自で実装し、ASE に依存しすぎない** |
| 生体分子 | `biopython` | 配列・構造処理 |
| 生体分子 | `prody` | 構造解析 |

### 5.3 `[dev]` extras（開発時のみ）

| カテゴリ | ライブラリ | 用途 |
|---------|-----------|------|
| リンター・フォーマッタ | `ruff` | 高速 linter + formatter |
| 型チェッカ | `mypy` | 静的型検査 |
| テスト | `pytest`, `pytest-cov`, `pytest-xdist`, `hypothesis` | テストフレームワーク・並列実行・プロパティテスト |
| ドキュメント | `mkdocs-material`, `mkdocstrings[python]` | ドキュメント生成 |
| pre-commit | `pre-commit` | コミット前の自動チェック |

### 5.4 インストール方法

```bash
# 通常利用
uv add kimika

# 開発者向け
uv sync --extra dev
```

`uv add kimika` 一発で計算化学・計算生物化学に必要な機能が一通り揃う。研究者は extras を意識する必要がない。

---

## 6. レシピフォーマット

### 6.1 構造例

```yaml
version: "1.0"

project:
  name: "water_basis_set_study"
  description: "Compare DFT energies of H2O across basis sets"
  tags: ["qm", "dft", "basis-set"]

system:
  type: "molecule"
  source:
    format: "xyz"
    path: "inputs/water.xyz"
  charge: 0
  multiplicity: 1

task:
  type: "qm.single_point"
  engine: "pyscf"
  parameters:
    method: "B3LYP"
    basis: "6-31G*"
    convergence:
      energy: 1.0e-6
      density: 1.0e-5

tracking:
  backend: "mlflow"
  experiment_name: "water_basis_set_study"
  log_artifacts: true

output:
  results_dir: "results"
  save_wavefunction: false
```

### 6.2 対応する Pydantic スキーマ（概念例）

```python
# kimika/schemas/recipe.py
from pydantic import BaseModel
from .system import SystemConfig
from .tasks import TaskConfig
from .tracking import TrackingConfig

class ProjectInfo(BaseModel):
    name: str
    description: str = ""
    tags: list[str] = []

class OutputConfig(BaseModel):
    results_dir: str = "results"
    save_wavefunction: bool = False

class Recipe(BaseModel):
    version: str
    project: ProjectInfo
    system: SystemConfig
    task: TaskConfig
    tracking: TrackingConfig
    output: OutputConfig
```

---

## 7. ユーザーフロー

1. ユーザーが `uv add kimika` でインストール（計算化学・計算生物化学に必要なライブラリが一通り揃う）
2. `kimika ui` で Streamlit UI を起動（メインの操作方法）
3. UI で：
   - 新規プロジェクト作成（内部で `kimika init` を呼ぶ）
   - 公式レシピカタログから選択 or ゼロから設定
   - Pydantic スキーマから自動生成されたフォームで設定
   - 設定内容が `recipe.yaml` に保存される
   - 実行ボタンで計算開始
   - MLflow と連携した結果ビューワで確認
4. CLI 補助：`kimika run recipe.yaml`、`kimika validate recipe.yaml` 等
5. 結果は MLflow + ローカル `results/` に保存され、再実行・再現可能

---

## 8. 実装方針（Claude Code への指示）

### 8.1 開発時のガイドライン

- **Python 3.11+ の機能を積極的に使う**（`X | Y` 型ヒント、`Self`、`match` 等）
- **型ヒントはすべての public API に必須**。strict mypy を通す
- **Pydantic v2 の機能を活用**（`model_validator`、`Annotated`、`Field` 等）
- **docstring は Google スタイル**（`mkdocstrings` で自動生成可能）
- **テストファースト**：新機能は対応するテストとセットで実装する

### 8.2 コードスタイル

- **`ruff` でリント・フォーマット**
- **行長は 100 文字**
- インポート順は ruff の isort ルールに従う

### 8.3 依存関係の追加

- 新しい依存を追加するときは必ず `uv add` を使う
- 計算エンジン・科学計算ライブラリ系の依存は **コア依存** に追加する
- 開発専用のもの（テスト・リント・ドキュメント等）は `[dev]` extras に追加する：`uv add --dev <package>`

### 8.4 実装の優先順位

実装の順序は以下を推奨する（必要に応じて調整可）：

1. **基盤**：プロジェクト初期化、`pyproject.toml`、ディレクトリ構造の作成
2. **設定システム**：`kimika/utils/config.py` で設定ファイル・環境変数・デフォルト値を統合的に扱う仕組み
3. **スキーマ**：`kimika/schemas/` の最小実装（`Recipe`, `SystemConfig`, `TaskConfig` 等）
4. **ワークスペース管理**：`kimika/workspace/` の実装（デフォルト `~/.kimika/`、`kimika init` でテンプレート展開）
5. **CLI 骨格**：`kimika` コマンドのエントリポイントと最小サブコマンド（`init`, `validate`, `config`）
6. **エンジンとタスクの抽象基底**：`Task`, `Engine` の基底クラスと registry
7. **PySCF エンジン + QM 単点計算タスク**：最初の動く実装
8. **レシピランナー**：YAML を読み込んでタスクを実行する流れ
9. **MLflow 連携**：基本的な実験追跡（デフォルト URI は `<workspace_root>/.mlruns`）
10. **Streamlit UI**：最小ページ（home, recipe builder, runner, results viewer）。`home` ページではワークスペース内のプロジェクト一覧を表示
11. **公式レシピカタログ**：最初の数件（H2O DFT 等）
12. **テスト・ドキュメント整備**

### 8.5 進め方

- 各段階で **動く最小実装** を優先し、抽象化や汎用化は後回しにする
- 「将来の細胞シミュレーションへの拡張」は意識するが、初期実装に過剰な抽象化を持ち込まない
- ユーザーが「コードと実験データの分離」を体感できる構造を最優先で確立する

---

## 9. 将来のロードマップ（参考）

### 短期

- 計算化学のシミュレーション（QM、MD、ドッキング等）の一通りのカバー
- Streamlit UI の充実

### 中期

- 機械学習ポテンシャルの統合
- 高度な解析機能（自由エネルギー計算等）

### 長期

- 計算生物化学への拡張
- 生体分子レベルからの細胞シミュレーション

---

## 10. 重要な原則のまとめ

1. **コードと実験データを構造的に分離する**（espnet で発生した問題を回避）
2. **Pydantic スキーマを設計の中心に据える**（UI・バリデーション・ドキュメントの単一情報源）
3. **Tasks と Engines を分離する**（やりたいこと vs 実装手段）
4. **Streamlit UI を主要インターフェースとし、CLI は補助とする**
5. **既存ソフトのラッパーに徹し、車輪の再発明をしない**
6. **オープンソースのみをサポート対象とする**
7. **Linux / macOS のみを公式サポートとする**
8. **uv で管理し、計算エンジンを含むすべての必須機能をコア依存に統合する**（`uv add kimika` 一発で完結する）
