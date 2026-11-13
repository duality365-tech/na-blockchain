# Graph Report - na-blockchain  (2026-11-13)

## Corpus Check
- 6 files · ~902 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 23 nodes · 26 edges · 6 communities (0 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b0c66cc5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- BlockchainNA
- CLAUDE.md
- .claude/CLAUDE.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `BlockchainNA` - 8 edges
2. `Calcule le solde actuel d'un portefeuille.` - 1 edges
3. `Création de nouveaux NA (Seulement possible avant le verrouillage).` - 1 edges
4. `Effectue une transaction entre deux utilisateurs.` - 1 edges
5. `Réajuste le compte du créateur à 5% max et verrouille le système.` - 1 edges
6. `Valide et enregistre les transactions dans un nouveau bloc.` - 1 edges
7. `graphify` - 1 edges
8. `graphify` - 1 edges
9. `na-blockchain` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (6 total, 6 thin omitted)

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BlockchainNA` connect `BlockchainNA` to `.get_balance`, `na_blockchain.py`?**
  _High betweenness centrality (0.344) - this node is a cross-community bridge._