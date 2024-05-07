## グラフ理論

### エッジプロパティ

エッジプロパティは別の型を指定しているプロパティのこと。

```edge property(1対1)
type Supplier {
    id: ID!
    name: String!
    address: String!
    contactNumber: String!
    email: String!
}

type Ingredient {
    id: ID!
    name: String!
    supplier: Supplier! # エッジを使ってIngredient型とSupplier型を接続
    description: [String!]
    lastUpdated: Datetime!
}
```