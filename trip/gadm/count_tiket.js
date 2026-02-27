// 计算 tiket 数据库下所有集合按 _id 去重后的数据量
const db = db.getSiblingDB("tiket");
const colls = db.getCollectionNames();
let total = 0;

colls.forEach(name => {
    const count = db.getCollection(name).estimatedDocumentCount();
    print(name + ": " + count);
    total += count;
});

print("--------------------");
print("总计: " + total);
