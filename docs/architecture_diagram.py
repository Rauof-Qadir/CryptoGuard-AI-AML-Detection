from graphviz import Digraph


dot = Digraph(
    "AML Architecture"
)


dot.node(
    "A",
    "Blockchain Transactions"
)


dot.node(
    "B",
    "Kafka Stream"
)


dot.node(
    "C",
    "Feature Engineering"
)


dot.node(
    "D",
    "Fraud ML Model"
)


dot.node(
    "E",
    "Risk Scoring"
)


dot.node(
    "F",
    "Investigation Dashboard"
)



dot.edges(
[
("A","B"),
("B","C"),
("C","D"),
("D","E"),
("E","F")
]
)



dot.render(
"AML_System_Architecture",
format="png"
)