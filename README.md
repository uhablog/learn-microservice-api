# 実践マイクロサービスAPIを実装してみた

このリポジトリは書籍「実践マイクロサービスAPI」の内容を実際に自分で実装してみたものになります。

## 全体を通して大切だと感じたポイント

- リクエスト・レスポンスのデータを検証する

以下各章の重要ポイントのメモです。

## CH02

- リクエストのパラメータの検証を行うのは大切
- レスポンスの検証は大切
- FastAPIではresponse_modeにスキーマを指定することで、レスポンスの検証が可能
- FastAPIはpydanticを使って、検証モデルの作成ができる
- FastAPIは自動でSwaggerUIを生成する

## CH03

### マイクロサービスの設計原則

1. サービスごとのデータベースの原則
2. 疎結合の原則
3. 単一責任の原則

#### 1. サービスごとのデータベースの原則

サービスごとに特定のデータセットを持っており、他のサービスからはAPIを介す事によってのみデータにアクセスすることができる。

必ずしも絶対にデータベースが分かれていないわけではなく、テーブルが分かれていたり、NoSQLであれば、コレクションが分かれていれば良い。別のサービスのデータにアクセスするのはAPIを介してのみということが大事。

#### 2. 疎結合の原則

- あるサービスは他のサービスから完全に独立した状態で、動作する
- あるサービスの変更は他のサービスに影響を与えない。あるサービスを変更するために、他のサービスを変更しなければならないという状態は設計を見直す必要があることを示している。

#### 3. 単一責任の原則

サービスをビジネスケイパビリティかサブドメインに基づいて分解を行い、それに従って一つのサービスが一つの責務を負う様にしていく。

### ビジネスケイパビリティによるサービスの分解

実際の企業に存在しているグループ・チームごとにサービスを構築する。
例えば、顧客管理チームがあるなら、顧客管理サービスを作成し、厨房チームがあるなら、厨房チームを作成する。

### サブドメインによるサービスの分割

サブドメインによるサービスの分割では、サービスの流れをフローに落とし、それぞれのフローがどのサービスに含まれるか考えていくことで、分割を行う。

### ビジネスケイパビリティとサブドメインによる分割どちらが良い？

理想はどちらの側でも検討を行い、比較してみること。

ただどちらかしかできない場合は、サブドメインによる分割がより良い手段となり得る。

ビジネスケイパビリティでは組織の再編やそもそも組織構造に原因がある場合があるから。

## CH07

### ヘキサゴナルアーキテクチャ

- コアとなるビジネスロジックが存在しており、外部とのやりとりをするためにアダプタと呼ばれるものをコアのビジネスロジックにアタッチする
- 例えばクライアントとやり取りをする際には、WebAPIインターフェースをアダプタとしてビジネスロジックにアタッチする
- 他にもデータベースとやり取りをする際には、データ層をアダプタとしてビジネスロジックにアタッチする
- コアビジネスロジックとアダプタの関係を確立するために、依存性逆転の原則を適応する

### 依存性逆転の原則

- 高レベルのモジュールは低レベルの詳細に依存するべきではなく、インターフェースに依存ずるべき
- データを保存するときには、インターフェースを通じて保存したい
- インターフェースに依存することで、詳細を理解する必要がなくなる
- SQLデータベース、NoSQLデータベース、キャッシュストアのどれを使うとしても、インターフェースは同じものを使用する
- インターフェースなどの抽象化は詳細に依存するべきではなく、詳細が抽象化に依存するべきである。
- 最初にインターフェースを考え、そのインターフェースに対して低レベルの詳細を構築する
- コアのビジネスロジックがインターフェースを提供し、データ層やAPI層はそのインターフェースに依存する

### Repositoryパターンとは？