<div align="center">

# Kwik-E-Mart Universe

![Kwik-E-Mart](https://static.wikia.nocookie.net/simpsons/images/d/da/800px-Kwik-E-Mart.png)

Self-contained Spark pipelines, one folder each, all set in Apu's Kwik-E-Mart.

</div>

## Inspiration

[Kwik-E-Mart](https://simpsons.fandom.com/wiki/Kwik-E-Mart) is Apu Nahasapeemapetilon's convenience store in Springfield, from The Simpsons.  
Both pocs live in that universe and use the same Simpsons cast (same 20 names, hardcoded in each generator),  
so their data can be joined later by name. Nothing in the code enforces this link.

| Poc | Stack | What it does |
|---|---|---|
| [`kwik-e-chain`](kwik-e-chain/README.md) | Scala 2.13, sbt, Delta Lake | DonutCoin ledger, a "chain" riff on the store: validates each transfer and routes it to success, error and debug tables |
| [`kwik-e-mart`](kwik-e-mart/README.md) | PySpark, uv, Delta Lake | The store's daily sales: renames columns, parses dates and prices, drops bad rows |

**PS.:** This is an unofficial fan project for learning Spark, not affiliated with or endorsed by Fox/Disney.
