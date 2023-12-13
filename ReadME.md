# Objetivos

## Objetivo principal
Avaliar o impacto da democratização das APIs e modelos LLM (Large Language Model) no desenvolvimento de projetos voltados a modelos de linguagem. Analisar a evolução e a "saúde" dos projetos com dados do Github ao longo do tempo.

## Objetivo secundário

Responder como está a taxa de mortalidade de algum dos projetos LLMs que tiveram momento de destaque no passado.


# Metodologia

Pontos a serem avaliados:

Atividade de desenvolvimento nos repositórios
    • Número de commits [x]
    • Número de pull requests [x]
    • Latência de PRs [x]
    • Número de comentários [x]
    • Número de novos contribuidores [x]
    • Taxa de contribuição de core developers [?]


- Possiveis outros pontos a serem avaliados:
    • Número de issues [x]
    • Número de stars [x]
    • Número de forks [x]
    • Número de watchers [?]
    

# Dados

## Seleção dos repositórios

Query no github
````
NOT game NOT survey NOT list (LLM AND "AI AGENT" OR NLP) license:mit license:apache-2.0 stars:>1000 fork:>1000 created:2020-06-01..2022-11-20
````

## Listagem de repositorios

langchain-ai/langchain: Link
PaddlePaddle/PaddleNLP: Link
nebuly-ai/nebuly: Link
microsoft/torchscale: Link
postgresml/postgresml: Link
run-llama/llama_index: Link
argilla-io/argilla: Link
bigscience-workshop/petals: Link
neuml/txtai: Link
intel/intel-extension-for-transformers: Link
uptrain-ai/uptrain
skypilot-org/skypilot
lancedb/lance
swirlai/swirl-search


